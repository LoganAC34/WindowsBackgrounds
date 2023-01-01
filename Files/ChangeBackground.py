import os
import shutil
import sqlite3
import sys

import pythoncom
from PIL import Image, ImageOps
from screeninfo import get_monitors
from win32comext.shell import shell, shellcon

import CopyBackgrounds

# Reletive and exe paths
try:
    # we are running in a bundle
    exe = sys._MEIPASS + '\\'
    relative = os.path.dirname(sys.executable) + '\\'
except AttributeError:
    # we are running in a normal Python environment
    exe = os.path.dirname(os.path.abspath(__file__)) + '\\'
    relative = '\\'.join(exe.split('\\')[:-2]) + '\\'

# Create shuffle order script if it doesn't exist
shuffleOrder = 'ShuffleOrder.exe'
#print(exe + shuffleOrder)
try:
    shutil.copyfile(exe + shuffleOrder, relative + shuffleOrder)
except shutil.SameFileError:
    pass

monitors = get_monitors()#win32api.EnumDisplayMonitors() # Get monitors

# Set min and max default values
height_min = 0
height_max = 0
width_min = 0
width_max = 0
desktop_width = 0
desktop_height = 0

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

    """
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
    """

# Create new blank image big enough to encompass entire desktop across multiple monitors
desktop_width = abs(width_max) + abs(width_min)
desktop_height = abs(height_max) + abs(height_min)
img = Image.new("RGB", (desktop_width, desktop_height))
def get_image(w, h):
    # Determine orientation
    orientation = "Landscape"
    if w < h:
        orientation = "Portrait"

    # Get 1 background that isn't used, set that background to used. If no backgrounds available, reset order.
    background_image = []
    while not background_image:
        # Get background
        background_image = cur.execute('SELECT Path FROM Backgrounds WHERE Used = 0 AND Orientation = "'
                            + orientation
                            + '" ORDER BY Num ASC LIMIT 1')
        background_image = background_image.fetchone()
        if not background_image: # If no backgrounds left, restart background order
            cur.execute('UPDATE Backgrounds SET Used = 0 WHERE Orientation = "'
                        + orientation
                        + '"')
        else: # else, set available background as used
            background_image = background_image[0]
            cur.execute('UPDATE Backgrounds SET Used = 1 WHERE Path = "' + background_image + '"')
        conn.commit()
    return Image.open(relative + background_image)

CopyBackgrounds.run()
# print(relative + "backgrounds.db")
conn = sqlite3.connect(relative + "backgrounds.db")
cur = conn.cursor()

imagesUsed = []
for monitor in monitors:
    """
    info = win32api.GetMonitorInfo(monitor[0])

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
    """
    monitorRes = (monitor.width, monitor.height)
    image = get_image(monitor.width, monitor.height)
    # Rescale image if necessary
    imagesUsed.append(image.filename.split('\\')[-1])
    imageWidth = image.size[0]
    imageHeight = image.size[1]
    image = ImageOps.exif_transpose(image) # Ensure image is rotated correctly
    image = image.resize(monitorRes, 1, None, 3.0)

    x = monitor.x + abs(width_min)
    y = monitor.y + abs(height_min)

    img.paste(image, (x, y))

# Save merged background image
imagePath = os.path.abspath(relative + "background.png")
img.save(imagePath)

# Sets background
# noinspection PyUnresolvedReferences
iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                                 pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
iad.SetWallpaper(imagePath, 0)
iad.ApplyChanges(shellcon.AD_APPLY_ALL)
# Add command for setting background to tiled

print("Images used:")
for image in imagesUsed:
    print(image)