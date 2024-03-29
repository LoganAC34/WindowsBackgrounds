# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Tue Jul 18 16:37:08 2023
#

import wx

from Project.bin.wxglade.FrameMainApp import *


class MainApp(FrameMainApp):
    def __init__(self, *args, **kwds):
        FrameMainApp.__init__(self, *args, **kwds)
        profileNum = self.profile_new()
        children = self.notebook_1.GetChildren()[0] # Figure out a way to populate list with paths from some source like xml or whatever
        self.list_ctrl_filePaths.Append(["./Backgrounds"])
        self.Layout()

    def on_resize(self, event):
        width = self.GetSize()[0] - 156
        self.list_ctrl_filePaths.SetColumnWidth(0, width)
        self.Layout()

    def profile_new(self, event=None):
        profile = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(profile, "Profile1")

        """ Paste below here and remove all "self." except for notebook and custom methods in binds"""
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        list_ctrl_filePaths = wx.ListCtrl(profile, wx.ID_ANY,
                                               style=wx.LC_AUTOARRANGE | wx.LC_EDIT_LABELS | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_SORT_DESCENDING | wx.LC_VRULES)
        list_ctrl_filePaths.AppendColumn("Path", format=wx.LIST_FORMAT_LEFT, width=-1)
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
        profileNum = self.notebook_1.GetPageCount() - 1
        self.notebook_1.ChangeSelection(profileNum)

        profile.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.window_tab_changed, self.notebook_1)
        profile.Bind(wx.EVT_BUTTON, self.profile_rename, button_profile_rename)
        profile.Bind(wx.EVT_BUTTON, self.profile_new, button_profile_new)
        profile.Bind(wx.EVT_BUTTON, self.profile_delete, button_profile_delete)
        profile.Bind(wx.EVT_BUTTON, self.path_add, button_path_add)
        profile.Bind(wx.EVT_BUTTON, self.path_delete, button_path_remove)
        profile.Bind(wx.EVT_BUTTON, self.window_apply, button_apply)
        profile.Bind(wx.EVT_BUTTON, self.window_cancel, button_cancel)

        return profileNum

    def profile_rename(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'profile_rename' not implemented!")
        event.Skip()

    def profile_delete(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'profile_delete' not implemented!")
        event.Skip()

    def path_add(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'path_add' not implemented!")
        event.Skip()

    def path_delete(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'path_delete' not implemented!")
        event.Skip()

    def window_apply(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'window_apply' not implemented!")
        event.Skip()

    def window_cancel(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'window_cancel' not implemented!")
        event.Skip()

    def on_resize(self, event):  # wxGlade: TabTemplate.<event_handler>
        print("Event handler 'on_resize' not implemented!")
        event.Skip()
