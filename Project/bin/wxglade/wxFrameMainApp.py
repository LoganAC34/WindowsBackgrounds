# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Fri Nov  3 14:43:28 2023
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
"""
This file is also a template to copy the tab format from.
Copy from first panel to last button bind and then after pasting into function, delete all "self." except ones
refer to custom functions or notebook.
"""
# end wxGlade


class wxFrameMainApp(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxFrameMainApp.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((512, 491))
        self.SetTitle("Background Folder Paths")

        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.Layout()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.window_tab_changed, self.notebook_1)
        self.Bind(wx.EVT_CLOSE, self.onButton_window_cancel, self)
        self.Bind(wx.EVT_SIZE, self.on_resize, self)
        # end wxGlade

    def window_tab_changed(self, event):  # wxGlade: wxFrameMainApp.<event_handler>
        print("Event handler 'window_tab_changed' not implemented!")
        event.Skip()

    def onButton_window_cancel(self, event):  # wxGlade: wxFrameMainApp.<event_handler>
        print("Event handler 'onButton_window_cancel' not implemented!")
        event.Skip()

    def on_resize(self, event):  # wxGlade: wxFrameMainApp.<event_handler>
        print("Event handler 'on_resize' not implemented!")
        event.Skip()

# end of class wxFrameMainApp
