# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Wed Jul 26 11:04:49 2023
#

import wx




class _992990114_wxFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((512, 491))
        self.SetTitle("Background Folder Paths")

        self.notebook_1 = wx.Notebook(self, -1, style=wx.NB_FLAT | wx.NB_TOP)

        self.Profile1 = wx.Panel(self.notebook_1, -1)
        self.notebook_1.AddPage(self.Profile1, "Profile1")

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.list_ctrl_filePaths = wx.ListCtrl(self.Profile1, -1, style=wx.LC_AUTOARRANGE | wx.LC_HRULES | wx.LC_REPORT | wx.LC_SORT_DESCENDING | wx.LC_VRULES)
        self.list_ctrl_filePaths.AppendColumn("Path", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_filePaths.InsertItem(0, "")
        sizer_1.Add(self.list_ctrl_filePaths, 1, wx.ALL | wx.EXPAND, 15)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 0, wx.BOTTOM | wx.EXPAND | wx.RIGHT | wx.TOP, 15)

        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.Profile1, wx.ID_ANY, "Profile"), wx.VERTICAL)
        sizer_2.Add(sizer_5, 0, wx.EXPAND, 0)

        self.button_profile_rename = wx.Button(self.Profile1, -1, "Rename")
        self.button_profile_rename.SetMinSize((75, 30))
        sizer_5.Add(self.button_profile_rename, 0, 0, 15)

        self.button_profile_new = wx.Button(self.Profile1, wx.ID_NEW, "")
        self.button_profile_new.SetMinSize((75, 30))
        sizer_5.Add(self.button_profile_new, 0, wx.TOP, 15)

        self.button_profile_delete = wx.Button(self.Profile1, wx.ID_DELETE, "")
        self.button_profile_delete.SetMinSize((75, 30))
        sizer_5.Add(self.button_profile_delete, 0, wx.TOP, 15)

        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self.Profile1, wx.ID_ANY, "Paths"), wx.VERTICAL)
        sizer_2.Add(sizer_6, 0, wx.EXPAND | wx.TOP, 15)

        self.button_path_add = wx.Button(self.Profile1, wx.ID_ADD, "")
        self.button_path_add.SetMinSize((75, 30))
        sizer_6.Add(self.button_path_add, 0, 0, 15)

        self.button_path_remove = wx.Button(self.Profile1, wx.ID_REMOVE, "")
        self.button_path_remove.SetMinSize((75, 30))
        sizer_6.Add(self.button_path_remove, 0, wx.TOP, 15)

        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_7, 1, wx.EXPAND, 0)

        sizer_7.Add((0, 0), 0, 0, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_3, 0, wx.LEFT | wx.RIGHT, 6)

        self.button_apply = wx.Button(self.Profile1, wx.ID_APPLY, "")
        self.button_apply.SetMinSize((75, 30))
        sizer_3.Add(self.button_apply, 0, wx.TOP, 15)

        self.button_cancel = wx.Button(self.Profile1, wx.ID_CANCEL, "")
        self.button_cancel.SetMinSize((75, 30))
        sizer_3.Add(self.button_cancel, 0, wx.TOP, 15)

        self.Profile1.SetSizer(sizer_1)

        self.Layout()

        try:
            self.Bind(wx.EVT_BUTTON, self.profile_rename, self.button_profile_rename)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")
        try:
            self.Bind(wx.EVT_BUTTON, self.profile_new, self.button_profile_new)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")
        try:
            self.Bind(wx.EVT_BUTTON, self.profile_delete, self.button_profile_delete)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")
        try:
            self.Bind(wx.EVT_BUTTON, self.path_add, self.button_path_add)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")
        try:
            self.Bind(wx.EVT_BUTTON, self.path_delete, self.button_path_remove)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")
        try:
            self.Bind(wx.EVT_BUTTON, self.window_apply, self.button_apply)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")
        try:
            self.Bind(wx.EVT_BUTTON, self.window_cancel, self.button_cancel)
        except:
            print("could not bind event wx.EVT_BUTTON - ignoring error for preview")

    def profile_rename(self, event):
        print("Event handler 'profile_rename' not implemented!")
        event.Skip()

    def profile_new(self, event):
        print("Event handler 'profile_new' not implemented!")
        event.Skip()

    def profile_delete(self, event):
        print("Event handler 'profile_delete' not implemented!")
        event.Skip()

    def path_add(self, event):
        print("Event handler 'path_add' not implemented!")
        event.Skip()

    def path_delete(self, event):
        print("Event handler 'path_delete' not implemented!")
        event.Skip()

    def window_apply(self, event):
        print("Event handler 'window_apply' not implemented!")
        event.Skip()

    def window_cancel(self, event):
        print("Event handler 'window_cancel' not implemented!")
        event.Skip()

