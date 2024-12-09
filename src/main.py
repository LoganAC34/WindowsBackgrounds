#!/usr/src/env python3
# -*- coding: UTF-8 -*-
from optparse import OptionParser

from Scripts import ChangeBackground, ShuffleOrder
from wxglade_overrides.FrameMainApp import *


class MyApp(wx.App):
    def __init__(self):
        super().__init__()
        self.FrameMainApp = None

    def OnInit(self):
        self.FrameMainApp = MainApp(None, wx.ID_ANY, "")
        self.SetTopWindow(self.FrameMainApp)
        self.FrameMainApp.Show()
        return True


def run(options):
    if options.mode in [None, 'UI', 'Settings']:
        print('Opening settings UI')
        app = MyApp()
        app.MainLoop()
    elif options.mode == 'ChangeBackground' and options.profile:
        print('Changing background(s)')
        ChangeBackground.run(options.profile)
    elif options.mode == 'ShuffleOrder' and options.profile:
        print('Shuffling background order')
        ShuffleOrder.run(options.profile)
    elif options.mode in ['ShuffleOrder', 'ChangeBackground'] and not options.profile:
        parser.error(f'Mode "{options.mode}" requires a profile.')
    else:
        parser.error(f'Invalid mode value "{options.mode}"')


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-m', '--mode', dest='mode',
                      help="""Mode to run. Settings will display if argument left empty.
                      
                      ChangeBackground  - Changes background. (Needs profile attribute)
                      ShuffleOrder      - Shuffles background order. (Needs profile attribute)
                      UI OR Settings    - Shows settings UI
                      """)
    parser.add_option('-p', '--profile', dest='profile',
                      help="""Profile to use.""")
    (options, args) = parser.parse_args()

    run(options)
