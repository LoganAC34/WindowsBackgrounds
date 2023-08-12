#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from wxglade_overrides.FrameMainApp import *


class MyApp(wx.App):
    def __init__(self):
        super().__init__(False, None, False, True)
        self.FrameMainApp = None

    def OnInit(self):
        self.FrameMainApp = MainApp(None, wx.ID_ANY, "")
        self.SetTopWindow(self.FrameMainApp)
        self.FrameMainApp.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
