# Get exe location
import os
import sys

class GlobalVars(object):
    # TODO: Update version number
    # TODO: Update changelog
    # MAJOR version when you make incompatible API changes
    # MINOR version when you add functionality in a backwards compatible manner
    # PATCH version when you make backwards compatible bug fixes
    version_number = 'v2.0'

    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        print('Frozen')
        # noinspection PyProtectedMember
        exe = sys._MEIPASS + '\\'
        app_path = sys.executable
        relative = os.path.dirname(sys.executable) + '\\'
        debug = False
    else:
        # we are running in a normal Python environment
        print('Not frozen')
        exe = os.path.abspath('./') + '\\'
        app_path = os.path.abspath('../../Testing/Local_Instant_Messenger.exe')
        relative = '\\'.join(exe.split('\\')[:-2]) + '\\'
        debug = True

    cfgFile_path = os.path.join(relative, 'profiles.cfg')  # Config file
