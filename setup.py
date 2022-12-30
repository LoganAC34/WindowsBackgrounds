import os
import shutil

import PyInstaller.__main__

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_name = dir_path.split('\\')[-1]
dst = 'C:/Temp/'+ dir_name + '/'
shutil.copytree(dir_path, dst)

# Shuffle order script
PyInstaller.__main__.run([
    dir_path + r'\ShuffleOrder.py',
    '-F',
])

# Main script
PyInstaller.__main__.run([
    dir_path + r'\ChangeBackground.py',
    '-F',
    '--hidden-import', 'PYTHONCOM',
    #'--debug=imports',
    '--add-data', dir_path + r'\db_template.db;.',
    '--add-data', dir_path + r'\CopyBackgrounds.py;.',
    '--add-data', dir_path + r'\dist\ShuffleOrder.exe;.'
])

shutil.rmtree(dst)