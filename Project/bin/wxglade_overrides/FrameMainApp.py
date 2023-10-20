import configparser

from Project.bin.Scripts import Config
from Project.bin.Scripts.Global import GlobalVars
from Project.bin.wxglade.wxFrameMainApp import *
from Project.bin.wxglade_overrides import RenameDialog


class MainApp(wxFrameMainApp):
    def __init__(self, *args, **kwds):
        wxFrameMainApp.__init__(self, *args, **kwds)
        cfgFile_path = GlobalVars.cfgFile_path
        self.RenameWindow = None

        self.on_start()

        # Figure out a way to populate list with paths from some source like xml or whatever
        self.profile_getPaths_config()
        self.on_resize(None)

    def on_start(self, event=None):
        profile_count = Config.get_profile_count()

        for x in range(0, profile_count):
            self.onButton_profile_new()

        profile_tabs = self.notebook_1.GetChildren()
        for tab in profile_tabs:
            profile_name = tab.Label()
            Config.get_profile_paths(profile_name)

    def on_resize(self, event):
        # Update column width
        profileNum = self.notebook_1.GetSelection()
        children = self.notebook_1.GetChildren()[profileNum]
        for item in children.GetChildren():
            if item.Name == 'listCtrl':
                width = self.GetSize()[0] - 156
                item.SetColumnWidth(0, width)
                self.Layout()
                break
        self.Layout()
        self.Refresh()

    def onButton_profile_new(self, event=None):
        profileNum = self.notebook_1.GetPageCount()

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

        list_ctrl_filePaths = wx.ListCtrl(profile, wx.ID_ANY,
                                               style=wx.LC_AUTOARRANGE | wx.LC_EDIT_LABELS | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_SORT_DESCENDING | wx.LC_VRULES)
        list_ctrl_filePaths.AppendColumn("Path", format=wx.LIST_FORMAT_LEFT, width=-1)
        list_ctrl_filePaths.Append(['./Downloads'])
        sizer_1.Add(list_ctrl_filePaths, 1, wx.ALL | wx.EXPAND, 15)

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
        profile.Bind(wx.EVT_BUTTON, self.onButton_profile_rename, button_profile_rename)
        profile.Bind(wx.EVT_BUTTON, self.onButton_profile_new, button_profile_new)
        profile.Bind(wx.EVT_BUTTON, self.onButton_profile_delete, button_profile_delete)
        profile.Bind(wx.EVT_BUTTON, self.onButton_path_add, button_path_add)
        profile.Bind(wx.EVT_BUTTON, self.onButton_path_delete, button_path_remove)
        profile.Bind(wx.EVT_BUTTON, self.onButton_window_apply, button_apply)
        profile.Bind(wx.EVT_BUTTON, self.onButton_window_cancel, button_cancel)

        """End paste here. DO NOT OVERRIDE CODE BELOW"""
        self.notebook_1.ChangeSelection(profileNum)

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

    def onButton_profile_delete(self, event):  # wxGlade: TabTemplate.<event_handler>
        #print("Event handler 'profile_delete' not implemented!")
        if self.notebook_1.GetPageCount() > 1:
            tabNum = self.notebook_1.GetSelection()
            self.notebook_1.DeletePage(tabNum)
            self.on_resize(event)

    def onButton_path_add(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'onButton_path_add' not implemented!")
        event.Skip()

    def onButton_path_delete(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'onButton_path_delete' not implemented!")

    def onButton_window_apply(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'onButton_window_apply' not implemented!")
        event.Skip()

    def onButton_window_cancel(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'onButton_window_cancel' not implemented!")
        event.Skip()


    def profile_rename(self, name_new):
        tabNum = self.notebook_1.GetSelection()
        self.notebook_1.SetPageText(tabNum, name_new)
        self.on_resize(None)


    def profile_getPaths_config(self, profile_name: str=None):
        def get_listCtrl(profile_num: int):
            """From profile_name number, get listCtrl"""
            profile_tab = self.notebook_1.GetChildren()[profile_num]
            for _item in profile_tab.GetChildren():
                if _item.Name == 'listCtrl':
                    return _item

        profileNum = self.notebook_1.GetSelection()  # Get current profile_name

        # Get profile_name number from name
        if profile_name:
            for x, item in enumerate(self.notebook_1.GetChildren()):
                if item.Label == profile_name:
                    profileNum = x

        if profileNum == -1:
            # Create profile_name if none exist (-1)
            profileNum = self.onButton_profile_new()
            list_ctrl = get_listCtrl(profileNum)

            # Get paths in profile_name listCtrl (default new profile_name paths)
            paths = []
            for x in range(0, list_ctrl.GetItemCount()):
                paths.append(list_ctrl.GetItemText(x, 0))

            return paths

        else:
            # Get existing profile_name paths from config file
            #list_ctrl = get_listCtrl(profileNum)

            # Get profile_name paths
            config = configparser.ConfigParser()
            config.read('example.ini')
