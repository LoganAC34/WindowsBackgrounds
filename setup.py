import os
import shutil

import PyInstaller.__main__

dir_PyCharm = os.path.abspath('../')
dir_path = os.path.abspath('./bin')
build = os.path.join(dir_PyCharm, 'build\\')

dir_name = os.path.basename(os.path.abspath('../'))
dst = os.path.join('C:/Temp', dir_name)
if os.path.isdir(dst):
    shutil.rmtree(dst)
shutil.copytree(dir_path, dst)

# Shuffle order script
PyInstaller.__main__.run([
    dst + 'ShuffleOrder.py',
    '--distpath', dst,
    '--workpath', build,
    '--specpath', build,
    #'--noconsole',
    '-F'

])

# Main script
PyInstaller.__main__.run([
    dst + 'ChangeBackground.py',
    '-n', 'Background_Changer',
    '--icon', os.path.join(dir_path, 'Background_Changer.ico'),
    '--distpath', dir_path,
    '--workpath', build,
    '--specpath', build,
    #'--noconsole',
    '--hidden-import', 'PYTHONCOM',
    '-F'
    #'--debug=imports',
    #'--add-data', dst + 'db_template.db;.',
    #'--add-data', dst + 'CopyBackgrounds.py;.',
    #'--add-data', dst + 'Settings_template.cfg;.',
    #'--add-data', dst + 'ShuffleOrder.exe;.'
])

shutil.rmtree(dst)
