import os
import sqlite3

import win32api
import win32con
import win32gui
from PIL import Image, ImageOps
from Project.bin.Scripts import GetBackgrounds, Config
from Project.bin.Scripts.Global import GlobalVars
from screeninfo import get_monitors


def run(profile: str):

    def get_image(w: int, h: int):
        # Determine orientation
        orientation = "Landscape"
        if w < h:
            orientation = "Portrait"

        # Get 1 background that isn't used, set that background to used. If no backgrounds available, reset order.
        background_image = []
        while not background_image:
            profile_table = profile_options['database_id']  # Get profile table name

            # Get background
            background_image = cur.execute(f'SELECT Path FROM "{profile_table}" WHERE Used = 0 '
                                           f'AND Orientation = "{orientation}" ORDER BY Num ASC LIMIT 1')
            background_image = background_image.fetchone()
            if not background_image:  # If no backgrounds left, restart background order
                cur.execute(f'UPDATE "{profile_table}" SET Used = 0 WHERE Orientation = "{orientation}"')
            else:  # else, set available background as used
                background_image = background_image[0]
                cur.execute(f'UPDATE "{profile_table}" SET Used = 1 WHERE Path = "{background_image}"')
            conn.commit()
        return Image.open(GlobalVars.relative + background_image)

    def set_wallpaper(path: str):
        key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "1")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1 + 2)

    # initialization
    profile_options = Config.get_all_options_for_profile(profile)  # Get profile settings
    GetBackgrounds.run(profile)  # Manage background DB
    monitors = get_monitors()  # Get monitors

    # Set min and max default values
    height_min = 0
    height_max = 0
    width_min = 0
    width_max = 0

    # Go through each monitor and get min and max coordinate values
    for monitor in monitors:
        height = monitor.y + monitor.height
        if monitor.y < height_min:
            height_min = monitor.y
        if height > height_max:
            height_max = height

        width = monitor.x + monitor.width
        if monitor.x < width_min:
            width_min = monitor.x
        if width > width_max:
            width_max = width

    # Create new blank image big enough to encompass entire desktop across multiple monitors
    desktop_width = abs(width_max) + abs(width_min)
    desktop_height = abs(height_max) + abs(height_min)
    img = Image.new("RGB", (desktop_width, desktop_height))

    # print(GlobalVars.dbFile_path)
    conn = sqlite3.connect(GlobalVars.dbFile_path)
    cur = conn.cursor()

    imagesUsed = []
    for monitor in monitors:
        monitorRes = (monitor.width, monitor.height)
        image = get_image(monitor.width, monitor.height)

        # Rescale image if necessary
        imagesUsed.append(image.filename.split('\\')[-1])
        image = ImageOps.exif_transpose(image)  # Ensure image is rotated correctly
        image = image.resize(monitorRes, resample=1, reducing_gap=3.0)

        x = monitor.x + abs(width_min)
        y = monitor.y + abs(height_min)

        img.paste(image, (x, y))

    # Save merged background image
    imagePath = os.path.abspath(GlobalVars.relative + "background.png")
    img.save(imagePath)
    if not GlobalVars.debug:
        set_wallpaper(imagePath)  # Sets background

    print("Images used:")
    for image in imagesUsed:
        print(image)


if __name__ == '__main__':
    run('')
