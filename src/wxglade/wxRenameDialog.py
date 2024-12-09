# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Fri Nov  3 14:43:28 2023
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxRenameDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxRenameDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("Rename")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, "Please enter a new name for the profile.")
        sizer_1.Add(label_1, 0, wx.ALL, 5)

        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_1.SetMaxLength(24)
        sizer_1.Add(self.text_ctrl_1, 0, wx.ALL | wx.EXPAND, 5)

        self.label_warning = wx.StaticText(self, wx.ID_ANY, "")
        sizer_1.Add(self.label_warning, 0, wx.ALL, 5)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        sizer_2.AddButton(self.button_CANCEL)

        self.button_APPLY = wx.Button(self, wx.ID_APPLY, "")
        sizer_2.AddButton(self.button_APPLY)

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetEscapeId(self.button_CANCEL.GetId())

        self.Layout()

        self.Bind(wx.EVT_TEXT, self.on_text, self.text_ctrl_1)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter, self.text_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.button_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.on_apply, self.button_APPLY)
        # end wxGlade

    def on_text(self, event):  # wxGlade: wxRenameDialog.<event_handler>
        print("Event handler 'on_text' not implemented!")
        event.Skip()

    def on_enter(self, event):  # wxGlade: wxRenameDialog.<event_handler>
        print("Event handler 'on_enter' not implemented!")
        event.Skip()

    def on_cancel(self, event):  # wxGlade: wxRenameDialog.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_apply(self, event):  # wxGlade: wxRenameDialog.<event_handler>
        print("Event handler 'on_apply' not implemented!")
        event.Skip()

# end of class wxRenameDialog
