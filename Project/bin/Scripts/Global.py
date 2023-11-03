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
        app_dir = os.path.abspath('./Project') + '\\'
        exe = os.path.join(app_dir, 'bin') + '\\'
        app_path = os.path.join(app_dir, 'Testing\\Local_Instant_Messenger.exe')
        relative = os.path.join(app_dir, 'Testing') + '\\'
        debug = True

    windowsBackground_path = os.path.join(relative, 'Windows Backgrounds')
    cfgFile_path = os.path.join(relative, 'profiles.cfg')  # Config file path
    dbFile_path = os.path.join(relative, 'backgrounds.db')  # Database file path
    dbTemplateFile_path = os.path.join(exe, 'Resources', 'db_template.db')  # Database file path
    dbTableTemplate = 'template'
