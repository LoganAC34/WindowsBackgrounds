import os
import shutil
import sqlite3
import sys
from os.path import exists

import pythoncom
import win32api
from PIL import Image, ImageOps
from win32comext.shell import shell, shellcon

import CopyBackgrounds

# Create shuffle order script if it doesn't exist
try:
    # we are running in a bundle
    bundle_dir = sys._MEIPASS
except AttributeError:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

shuffleOrder = 'ShuffleOrder.exe'
if not exists(shuffleOrder):
    shutil.copyfile(bundle_dir + '\\' + shuffleOrder, shuffleOrder)

monitors = win32api.EnumDisplayMonitors() # Get monitors

# Set min and max default values
height_min = 0
height_max = 0
width_min = 0
width_max = 0

# Go through each monitor and get min and max coordinate values
for monitor in monitors:
    info = win32api.GetMonitorInfo(monitor[0])["Monitor"]

    left = info[0]
    top = info[1]
    right = info[2]
    bottom = info[3]

    if left == 0 and top == 0 and right > 0 and bottom > 0:
        primaryRes_width = right
        primaryRes_height = bottom

    # Get max and min width coordinates
    width = [left, right]
    max_width = max(width)
    min_width = min(width)

    if max_width > width_max:
        width_max = max_width
    if min_width < width_min:
        width_min = min_width

    # Get max and min height coordinates
    height = [top, bottom]
    max_height = max(height)
    min_height = min(height)

    if max_height > height_max:
        height_max = max_height
    if min_height < height_min:
        height_min = min_height

# Create new blank image big enough to encompass entire desktop across multiple monitors
desktop_width = abs(width_max) + abs(width_min)
desktop_height = abs(height_max) + abs(height_min)
img = Image.new("RGB", (desktop_width, desktop_height))

def get_image(w, h):
    orientation = "Landscape"
    if w < h:
        orientation = "Portrait"
    conn = sqlite3.connect("backgrounds.db")
    cur = conn.cursor()
    background_image = []
    while not background_image:
        background_image = cur.execute('SELECT Path FROM Backgrounds WHERE Used = 0 AND Orientation = "'
                            + orientation
                            + '" ORDER BY Num ASC LIMIT 1')
        background_image = background_image.fetchone()
        if not background_image:
            cur.execute('UPDATE Backgrounds SET Used = 0 WHERE Orientation = "'
                        + orientation
                        + '"')
        else:
            background_image = background_image[0]
            cur.execute('UPDATE Backgrounds SET Used = 1 WHERE Path = "' + background_image + '"')
            conn.commit()
    return Image.open(background_image)

CopyBackgrounds.run()

for monitor in monitors:
    info = win32api.GetMonitorInfo(monitor[0])["Monitor"]

    left = info[0]
    top = info[1]
    right = info[2]
    bottom = info[3]

    if top <= 0 and bottom >= 0:
        monitor_height = abs(bottom) + abs(top)
        monitor_width = abs(left) + abs(right)
    elif top > 0 and bottom > 0:
        monitor_height = abs(bottom) - abs(top)
        monitor_width = abs(left) + abs(right)

    monitorRes = (monitor_width, monitor_height)
    image = get_image(monitor_width, monitor_height)
    # Rescale image if necessary
    imageWidth = image.size[0]
    imageHeight = image.size[1]
    image = ImageOps.exif_transpose(image)
    image = image.resize(monitorRes, 1, None, 3.0)

    x = left + abs(width_min)
    y = top + abs(height_min)

    img.paste(image, (x, y))

# Save merged background image
imagePath = os.path.abspath("background.png")
img.save(imagePath)

# Sets background
# noinspection PyUnresolvedReferences
iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                                 pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
iad.SetWallpaper(imagePath, 0)
iad.ApplyChanges(shellcon.AD_APPLY_ALL)
