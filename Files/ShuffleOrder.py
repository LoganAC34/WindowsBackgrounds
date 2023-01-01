import os
import random
import sqlite3
import sys

# Reletive and exe paths
try:
    # we are running in a bundle
    exe = sys._MEIPASS + '\\'
    relative = os.path.dirname(sys.executable) + '\\'
except AttributeError:
    # we are running in a normal Python environment
    exe = os.path.dirname(os.path.abspath(__file__)) + '\\'
    relative = '\\'.join(exe.split('\\')[:-2]) + '\\'

conn = sqlite3.connect(relative + 'backgrounds.db')
cur = conn.cursor()

# Reshuffle background order
allBackgrounds = cur.execute('SELECT * FROM Backgrounds')
allBackgrounds = allBackgrounds.fetchall()
random.shuffle(allBackgrounds)
for x, background in enumerate(allBackgrounds):
    x += 1
    num = str(x)
    values = list(background)
    values[0] = x
    values = str(tuple(values)).replace('\\\\', '\\')
    background_path = background[3]
    cur.execute('DELETE FROM Backgrounds WHERE Num = ' + num) # Delete background at order to prevent conflict
    cur.execute('UPDATE or REPLACE Backgrounds SET Num = ' + num + ' WHERE Path = "' + background_path + '"') # Update existing record (if it still exists)
    cur.execute('INSERT or IGNORE INTO Backgrounds (Num, Used, Orientation, Path) ' # Insert record if it didn't exist. 
                'VALUES ' + values)
conn.commit()
