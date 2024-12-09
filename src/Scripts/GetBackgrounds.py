import os
import shutil
from os import listdir
from os import mkdir
from os.path import isfile, exists

from PIL import Image
from pillow_heif import register_heif_opener

from Scripts import Config
from Scripts.Global import GlobalVars


def insert_background(profile_table, path):
    conn, cur = Config.connect_to_db()

    register_heif_opener()
    try:
        with Image.open(path) as image:
            width, height = image.size
    except:
        pass

    orientation = 'Landscape'
    if width < height:
        orientation = 'Portrait'

    path = path.replace(GlobalVars.relative, '')

    cur.execute(f'SELECT * FROM "{profile_table}" WHERE Path = "{path}"')  # See if image already exists in DB
    result = cur.fetchone()
    if not result:
        cur.execute(f'INSERT INTO "{profile_table}" (Used, Orientation, Path) VALUES (0, "{orientation}", "{path}")')
        conn.commit()

def copy_windows_backgrounds(profile_table):
    numFilesCopied = 0
    filesCopied = []

    # Get windows background folder
    windows_backgrounds = os.path.join(os.getenv('LOCALAPPDATA'),
                                       'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets')

    # If backgrounds folder doesn't exist, create it
    if not exists(GlobalVars.windowsBackground_path):
        mkdir(GlobalVars.windowsBackground_path)

    # Iterate though each windows background and copy if it's actually a background (threshold is 720p)
    for file in listdir(windows_backgrounds):
        w_path = os.path.join(windows_backgrounds, file)

        # Get image dimensions
        if isfile(w_path):
            with Image.open(w_path) as img:
                w, h = img.size

            # If higher than 720p and isn't already copied, copy
            dst = os.path.join(GlobalVars.windowsBackground_path, f'{file}.jpg')
            if ((w > 1280 and h > 720) or (w > 720 and h > 1280)) and not exists(dst):
                shutil.copyfile(w_path, dst)
                numFilesCopied += 1
                filesCopied.append(file)
                insert_background(profile_table, dst)

    print(str(numFilesCopied) + " new backgrounds saved.")
    for x, file in enumerate(filesCopied):
        print(f"{str(x + 1)}: {file}.jpg")


def run(profile_name):
    profile_options = Config.get_all_options_for_profile(profile_name)  # Get profile options
    background_dirs = Config.get_paths_for_profile(profile_name)
    profile_table = profile_options['database_id']  # Get profile table name
    conn, cur = Config.connect_to_db()  # Connect to db

    print(GlobalVars.dbFile_path)

    # Get windows backgrounds if profile wants to use them
    if profile_options['use_windows_backgrounds']:
        copy_windows_backgrounds(profile_table)
        background_dirs.append(GlobalVars.windowsBackground_path)

    # Check if all backgrounds are added to database
    for directory in background_dirs:
        """Replace "." with reletive absolute path"""
        directory = directory.replace(".", GlobalVars.relative)
        directory = os.path.abspath(directory)
        for background in listdir(directory):
            s_path = os.path.join(directory, background)
            insert_background(profile_table, s_path)

    # Check if any backgrounds have been removed
    allBackgrounds = cur.execute(f'SELECT Path FROM "{profile_table}"')
    allBackgrounds = allBackgrounds.fetchall()
    for background in allBackgrounds:
        background_test = GlobalVars.relative + background[0]
        if not exists(background_test):
            cur.execute(f'DELETE FROM "{profile_table}" WHERE Path = "{background[0]}"')
            conn.commit()

    # Print images copied
    allBackgrounds = cur.execute(f'SELECT Path FROM "{profile_table}"')
    allBackgrounds = allBackgrounds.fetchall()
    backgroundCount = len(allBackgrounds)
    print(str(backgroundCount) + " backgrounds total.")

# GetBackgrounds.py executed as script
if __name__ == '__main__':
    run(None)
