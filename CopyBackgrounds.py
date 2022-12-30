import os
# import random
import shutil
import sqlite3
import sys
from os import listdir
from os import mkdir
from os.path import isfile, join, exists

from PIL import Image
from pillow_heif import register_heif_opener


# from pathlib import Path


# noinspection PyUnresolvedReferences
def run():
    try:
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    except AttributeError:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    windows_backgrounds = os.getenv('LOCALAPPDATA') + '\\Packages' \
                          '\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'

    backgrounds_dir = 'Backgrounds'
    if not exists(backgrounds_dir):
        mkdir(backgrounds_dir)

    db_backgrounds = 'backgrounds.db'

    # If backgrounds DB doesn't exist, create new from template
    if not exists(db_backgrounds):
        db_template = bundle_dir + '\db_template.db'
        shutil.copyfile(db_template, db_backgrounds)
    conn = sqlite3.connect(db_backgrounds)
    cur = conn.cursor()

    def insert_background(path):
        register_heif_opener()
        try:
            with Image.open(path) as image:
                width, height = image.size
        except:
            pass

        orientation = 'Landscape'
        if width < height:
            orientation = 'Portrait'
        cur.execute('INSERT or IGNORE INTO Backgrounds (Orientation, Path) VALUES ("' + orientation + '", "' + path + '")')
        conn.commit()

    # Iterate though each windows background and copy if it's actually a background (threshold is 720p)
    numFilesCopied = 0
    filesCopied = []
    for file in listdir(windows_backgrounds):
        w_path = join(windows_backgrounds, file)

        # Get image dimensions
        if isfile(w_path):
            with Image.open(w_path) as img:
                w, h = img.size

            # If higher than 720p and isn't already copied, copy
            dst = backgrounds_dir + '\\' + file + '.jpg'
            if ((w > 1280 and h > 720) or (w > 720 and h > 1280)) and not exists(dst):
                shutil.copyfile(w_path, dst)
                numFilesCopied += 1
                filesCopied.append(file)
                insert_background(dst)

    # Check if all backgrounds are added to database
    for background in listdir(backgrounds_dir):
        s_path = join(backgrounds_dir, background)
        insert_background(s_path)

    # Check if any backgrounds have been removed
    allBackgrounds = cur.execute('SELECT Path FROM Backgrounds')
    allBackgrounds = allBackgrounds.fetchall()
    for background in allBackgrounds:
        background = background[0]
        if not exists(background):
            cur.execute('DELETE FROM Backgrounds WHERE Path = "' + background + '"')
            conn.commit()

        """
        # Reset Used value
        cur.execute('UPDATE Backgrounds SET Used = 0')
        conn.commit()
        
        # Reshuffle background order
        allBackgrounds = cur.execute('SELECT Path FROM Backgrounds')
        allBackgrounds = allBackgrounds.fetchall()
        random.shuffle(allBackgrounds)
        for x, background in enumerate(allBackgrounds):
            x += 1
            cur.execute('UPDATE Backgrounds SET Num = ' + str(x) + ' WHERE Path = "' + background[0] + '"')
        conn.commit()
        """
    # Print images copied
    print(str(numFilesCopied) + " new backgrounds saved.")
    allBackgrounds = cur.execute('SELECT Path FROM Backgrounds')
    allBackgrounds = allBackgrounds.fetchall()
    backgroundCount = len(allBackgrounds)
    print(str(backgroundCount) + " backgrounds total.")
    for x, file in enumerate(filesCopied):
        print(str(x + 1) + ": " + file + ".jpg")

# test1.py executed as script
if __name__ == '__main__':
    run()