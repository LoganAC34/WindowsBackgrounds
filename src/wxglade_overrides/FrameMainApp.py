import os
import shutil
import sqlite3
from os.path import exists

from Project.bin.Scripts import Config
from Project.bin.Scripts.Global import GlobalVars
from Project.bin.wxglade.wxFrameMainApp import *
from Project.bin.wxglade_overrides import RenameDialog
from Project.bin.wxglade_overrides import WarningDialog
from wx.lib.agw.multidirdialog import MultiDirDialog


class MainApp(wxFrameMainApp):
    def __init__(self, *args, **kwds):
        wxFrameMainApp.__init__(self, *args, **kwds)
        self.RenameWindow = None
        self.WarningDialog = None
        self.UnsavedChanges = False

        self.on_start()
        self.on_resize(None)

    def on_start(self, event=None):
        for x, profile_name in enumerate(Config.get_all_profiles()):
            self.onButton_profile_new(profile_name=profile_name)

            # Get path info
            profile_table = self.get_path_ListCTrl(x)
            profile_paths = Config.get_paths_for_profile(profile_name)
            for path in profile_paths:
                profile_table.Append([path])

            # Get checkbox info
            settings = Config.get_options_for_profile(profile_name)
            ui_options = {'use_windows_backgrounds': self.get_windows_background_checkbox,
                          'database_id': self.get_database_ID_att}
            for key, value in settings.items():
                checkbox_method = ui_options[key]  # Determine which method is needed to get UI element
                element = checkbox_method(x)  # Run method to get UI element
                if isinstance(element, wx.StaticText):
                    element.SetLabelText(value)
                elif isinstance(element, wx.CheckBox):
                    element.SetValue(value == 'True')  # Set UI element value from setting

        self.on_resize(event)

    def on_close(self):
        self.Destroy()

    def on_resize(self, event):
        def run():
            # Update column width
            paths_table = self.get_path_ListCTrl()
            width = self.GetSize()[0] - 156
            paths_table.SetColumnWidth(0, width)

            # Check paths
            count = paths_table.GetItemCount()
            for item in range(0, count):
                path = paths_table.GetItemText(item, 0)
                path = path.replace('.\\', GlobalVars.relative)
                path = os.path.abspath(path)
                if not os.path.exists(path):
                    # print('red')
                    paths_table.SetItemBackgroundColour(item, wx.Colour(255, 100, 100, 50))
                else:
                    # print('white')
                    paths_table.SetItemBackgroundColour(item, wx.Colour(255, 255, 255, 100))

            # Refresh window
            self.Layout()
            self.Update()
            self.Refresh()

        wx.CallAfter(run)

    def window_tab_changed(self, event):
        self.on_resize(event)

    # noinspection PyArgumentEqualDefault
    def onButton_profile_new(self, event=None, profile_name: str = None):
        profileNum = self.notebook_1.GetPageCount()
        new = False

        if not profile_name:  # Create new profile name if new
            new = True

            # Get profile name while not conflicting with an existing.
            x = 0
            while True:
                x += 1
                profile_name = f'User{x}'
                used_profile_names = []
                if profileNum > 0:
                    for item in range(0, profileNum):
                        tab_name = self.notebook_1.GetPageText(item)
                        used_profile_names.append(tab_name)

                if profile_name not in used_profile_names:
                    break

        profile = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(profile, profile_name)

        """ Paste below here and remove all "self." except for notebook and custom methods in binds"""

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

        database_ID = wx.StaticText(profile, wx.ID_ANY, "ID")
        database_ID.Hide()
        database_ID.SetName('database_id')

        checkbox_windowsBackgrounds = wx.CheckBox(profile, wx.ID_ANY, "Download Windows Backgrounds")
        sizer_4.Add(checkbox_windowsBackgrounds, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        list_ctrl_filePaths = wx.ListCtrl(profile, wx.ID_ANY,
                                          style=wx.LC_AUTOARRANGE | wx.LC_EDIT_LABELS | wx.LC_HRULES | wx.LC_NO_HEADER |
                                                wx.LC_REPORT | wx.LC_SORT_DESCENDING | wx.LC_VRULES)
        list_ctrl_filePaths.AppendColumn("Path", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_4.Add(list_ctrl_filePaths, 1, wx.ALL | wx.EXPAND, 15)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 0, wx.BOTTOM | wx.EXPAND | wx.RIGHT | wx.TOP, 15)

        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(profile, wx.ID_ANY, "Profile"), wx.VERTICAL)
        sizer_2.Add(sizer_5, 0, wx.EXPAND, 0)

        button_profile_rename = wx.Button(profile, wx.ID_ANY, "Rename")
        button_profile_rename.SetMinSize((75, 30))
        sizer_5.Add(button_profile_rename, 0, 0, 15)

        button_profile_new = wx.Button(profile, wx.ID_NEW, "")
        button_profile_new.SetMinSize((75, 30))
        sizer_5.Add(button_profile_new, 0, wx.TOP, 15)

        button_profile_delete = wx.Button(profile, wx.ID_DELETE, "")
        button_profile_delete.SetMinSize((75, 30))
        sizer_5.Add(button_profile_delete, 0, wx.TOP, 15)

        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(profile, wx.ID_ANY, "Paths"), wx.VERTICAL)
        sizer_2.Add(sizer_6, 0, wx.EXPAND | wx.TOP, 15)

        button_path_add = wx.Button(profile, wx.ID_ADD, "")
        button_path_add.SetMinSize((75, 30))
        sizer_6.Add(button_path_add, 0, 0, 15)

        button_path_remove = wx.Button(profile, wx.ID_REMOVE, "")
        button_path_remove.SetMinSize((75, 30))
        sizer_6.Add(button_path_remove, 0, wx.TOP, 15)

        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_7, 1, wx.EXPAND, 0)

        sizer_7.Add((0, 0), 0, 0, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_3, 0, wx.LEFT | wx.RIGHT, 6)

        button_apply = wx.Button(profile, wx.ID_APPLY, "")
        button_apply.SetMinSize((75, 30))
        sizer_3.Add(button_apply, 0, wx.TOP, 15)

        button_cancel = wx.Button(profile, wx.ID_CANCEL, "")
        button_cancel.SetMinSize((75, 30))
        sizer_3.Add(button_cancel, 0, wx.TOP, 15)

        profile.SetSizer(sizer_1)

        profile.Layout()

        profile.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.window_tab_changed, self.notebook_1)
        profile.Bind(wx.EVT_CHECKBOX, self.on_checkbox_windows_background, checkbox_windowsBackgrounds)
        profile.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.on_resize, list_ctrl_filePaths)
        profile.Bind(wx.EVT_BUTTON, self.onButton_profile_rename, button_profile_rename)
        profile.Bind(wx.EVT_BUTTON, self.onButton_profile_new, button_profile_new)
        profile.Bind(wx.EVT_BUTTON, self.onButton_profile_delete, button_profile_delete)
        profile.Bind(wx.EVT_BUTTON, self.onButton_path_add, button_path_add)
        profile.Bind(wx.EVT_BUTTON, self.onButton_path_delete, button_path_remove)
        profile.Bind(wx.EVT_BUTTON, self.onButton_window_apply, button_apply)
        profile.Bind(wx.EVT_BUTTON, self.onButton_window_cancel, button_cancel)
        profile.Bind(wx.EVT_SIZE, self.on_resize, self)

        """End paste here. DO NOT OVERRIDE CODE BELOW"""
        if new:
            self.UnsavedChanges = True
            list_ctrl_filePaths.Append(['.\\Backgrounds'])
        self.notebook_1.ChangeSelection(profileNum)
        self.on_resize(event)

        return profileNum

    def onButton_profile_rename(self, event):
        #print("Event handler 'profile_rename' not implemented!")
        profile_num = self.notebook_1.GetSelection()
        current_profile_name = self.notebook_1.GetPageText(profile_num)

        if not self.RenameWindow:
            self.RenameWindow = RenameDialog.RenameDialog(self, current_profile_name)
            self.RenameWindow.CentreOnParent()
            self.Disable()
            self.RenameWindow.Show()

        event.Skip()

    def onButton_profile_delete(self, event):
        #print("Event handler 'delete_unused_profiles' not implemented!")
        if self.notebook_1.GetPageCount() > 1:
            self.UnsavedChanges = True
            tabNum = self.notebook_1.GetSelection()
            self.notebook_1.DeletePage(tabNum)
            self.on_resize(event)

    def onButton_path_add(self, event, paths: list = None):
        # print("Event handler 'onButton_path_add' not implemented!")
        paths_table = self.get_path_ListCTrl()

        # Get all existing paths
        count = paths_table.GetItemCount()
        existing_paths = []
        for item in range(0, count):
            e_path = paths_table.GetItemText(item, 0)
            existing_paths.append(e_path)

        if not paths:
            paths = self.onMultiDir()  # Get user to pick directories

        if paths:
            for path in paths:
                path = path.replace(GlobalVars.relative, '.\\')  # Get reletive path
                if path not in existing_paths:
                    self.UnsavedChanges = True
                    paths_table.Append([path])

        event.Skip()

    def onButton_path_delete(self, event):
        #print("Event handler 'onButton_path_delete' not implemented!")
        self.UnsavedChanges = True
        paths_table = self.get_path_ListCTrl()

        count = paths_table.GetItemCount()
        items_to_delete = []
        for item in range(0, count):
            if paths_table.IsSelected(item):
                items_to_delete.append(item)

        items_to_delete.reverse()
        for item_to_delete in items_to_delete:
            #count = paths_table.GetItemCount()  # Could be used to
            #if count > 1:                       # keep one path left.
            paths_table.DeleteItem(item_to_delete)

        event.Skip()

    def onButton_window_apply(self, event):
        #print("Event handler 'onButton_window_apply' not implemented!")
        self.UnsavedChanges = False
        current_profiles = []
        for page in range(0, self.notebook_1.GetPageCount()):
            profile_name = self.notebook_1.GetPageText(page)
            current_profiles.append(profile_name)  # Keep track of current profile names to determine which to delete.
            paths_table = self.get_path_ListCTrl(page)

            # Get all paths
            count = paths_table.GetItemCount()
            options = {}
            for x, item in enumerate(range(0, count)):
                e_path = paths_table.GetItemText(item, 0)
                options[x] = e_path

            # Check box options
            options['use_windows_backgrounds'] = self.get_windows_background_checkbox(page).IsChecked()
            options['database_id'] = self.get_database_ID_att(page).GetLabelText()

            # If backgrounds DB doesn't exist, create new from template
            if not exists(GlobalVars.dbFile_path):
                shutil.copyfile(GlobalVars.dbTemplateFile_path, GlobalVars.dbFile_path)

            # ADD CODE TO CREATE NEW DB FROM TEMPLATE IF IT DOESN'T EXIST
            conn = sqlite3.connect(GlobalVars.dbFile_path)
            cursor = conn.cursor()

            # 1. Get the schema of the original table
            cursor.execute(f'PRAGMA table_info("{GlobalVars.dbTableTemplate}")')
            columns = cursor.fetchall()

            # 2. Create a new table with the same schema
            db_id = options['database_id']
            create_table_query = f'CREATE TABLE IF NOT EXISTS "{db_id}" ('
            create_table_query += ', '.join([f"{col[1]} {col[2]}" for col in columns])
            create_table_query += ')'
            cursor.execute(create_table_query)
            conn.commit()
            conn.close()

            Config.add_or_update_profile(profile_name, options)  # Save options

        Config.delete_unused_profiles(current_profiles)

        event.Skip()

    def onButton_window_cancel(self, event):  # wxGlade: TabTemplate.<event_handler>
        #print("Event handler 'onButton_window_cancel' not implemented!")
        if self.UnsavedChanges:
            title = f"Are you sure?"
            message = "Do you really want to cancel all changes made?"
            self.WarningDialog = WarningDialog.WarningDialog(self, 2, title, message, self.on_close)
            self.WarningDialog.CentreOnParent()
            self.Disable()
            self.WarningDialog.Show()
        else:
            self.on_close()
        #event.Skip()

    def on_checkbox_windows_background(self, event):
        #print("Event handler 'on_checkbox_windows_background' not implemented!")
        self.UnsavedChanges = True

    def profile_rename(self, name_new):
        self.UnsavedChanges = True
        tabNum = self.notebook_1.GetSelection()
        self.notebook_1.SetPageText(tabNum, name_new)
        self.on_resize(None)

    def onMultiDir(self):
        """
        Create and show the MultiDirDialog
        """
        defaultPath = os.path.join(GlobalVars.relative, 'Backgrounds')
        dlg = MultiDirDialog(self, title="Choose a directory:", defaultPath=defaultPath, agwStyle=wx.DD_MULTIPLE)
        paths = None
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        dlg.Destroy()
        return paths

    def get_path_ListCTrl(self, page: int = None):
        # Get paths table
        if page is None:
            profile_page = self.notebook_1.GetCurrentPage()
        else:
            profile_page = self.notebook_1.GetPage(page)

        for element in profile_page.GetChildren():
            if element.Name == 'listCtrl':
                return element

    def get_windows_background_checkbox(self, page: int = None):
        # Get paths table
        if page is None:
            profile_page = self.notebook_1.GetCurrentPage()
        else:
            profile_page = self.notebook_1.GetPage(page)

        for element in profile_page.GetChildren():
            if element.Label == 'Download Windows Backgrounds':
                return element

    def get_database_ID_att(self, page: int = None):
        # Get paths table
        if page is None:
            profile_page = self.notebook_1.GetCurrentPage()
        else:
            profile_page = self.notebook_1.GetPage(page)

        for element in profile_page.GetChildren():
            if element.Name == 'database_id':
                return element
