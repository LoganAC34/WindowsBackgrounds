import os
import shutil
import sqlite3
from os import listdir
from os import mkdir
from os.path import isfile, join, exists

from PIL import Image
from pillow_heif import register_heif_opener

from Project.bin.Scripts import Config
from Project.bin.Scripts.Global import GlobalVars

# Relative and exe paths
exe = GlobalVars.exe
relative = GlobalVars.relative

def run(profile_name):
    windows_backgrounds = os.path.join(os.getenv('LOCALAPPDATA'),
                                       'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets')

    profile_options = Config.get_all_options_for_profile(profile_name)  # Get profile options
    profile_table = profile_options['database_id']  # Get profile table name

    # If backgrounds folder doesn't exist, create it
    if not exists(GlobalVars.windowsBackground_path) and profile_options['use_windows_backgrounds']:
        mkdir(GlobalVars.windowsBackground_path)

    print(GlobalVars.dbFile_path)

    conn = sqlite3.connect(GlobalVars.dbFile_path)
    cur = conn.cursor()

    def insert_background(path):
        register_heif_opener()
        try:
            with Image.open(path) as image:
                width, height = image.size
        except:
            pass

        path = path.replace(relative, '')

        orientation = 'Landscape'
        if width < height:
            orientation = 'Portrait'
        cur.execute(f'INSERT or IGNORE INTO "{profile_table}" (Orientation, Path) VALUES ("{orientation}", "{path}")')
        conn.commit()

    numFilesCopied = 0
    filesCopied = []
    if profile_options['use_windows_backgrounds']:
        # Iterate though each windows background and copy if it's actually a background (threshold is 720p)
        for file in listdir(windows_backgrounds):
            w_path = join(windows_backgrounds, file)

            # Get image dimensions
            if isfile(w_path):
                with Image.open(w_path) as img:
                    w, h = img.size

                # If higher than 720p and isn't already copied, copy
                dst = GlobalVars.windowsBackground_path + f'\\{file}.jpg'
                if ((w > 1280 and h > 720) or (w > 720 and h > 1280)) and not exists(dst):
                    shutil.copyfile(w_path, dst)
                    numFilesCopied += 1
                    filesCopied.append(file)
                    insert_background(dst)

    # Check if all backgrounds are added to database
    for background in listdir(GlobalVars.windowsBackground_path):
        s_path = join(GlobalVars.windowsBackground_path, background)
        insert_background(s_path)

    # Check if any backgrounds have been removed
    allBackgrounds = cur.execute(f'SELECT Path FROM {profile_table}')
    allBackgrounds = allBackgrounds.fetchall()
    for background in allBackgrounds:
        background_test = relative + background[0]
        if not exists(background_test):
            cur.execute(f'DELETE FROM "{profile_table}" WHERE Path = "{background[0]}"')
            conn.commit()

    # Print images copied
    print(str(numFilesCopied) + " new backgrounds saved.")
    allBackgrounds = cur.execute(f'SELECT Path FROM "{profile_table}"')
    allBackgrounds = allBackgrounds.fetchall()
    backgroundCount = len(allBackgrounds)
    print(str(backgroundCount) + " backgrounds total.")
    for x, file in enumerate(filesCopied):
        print(f"{str(x + 1)}: {file}.jpg")

# CopyBackgrounds.py executed as script
if __name__ == '__main__':
    run()
