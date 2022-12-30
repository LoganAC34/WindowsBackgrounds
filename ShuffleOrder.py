import random
import sqlite3

conn = sqlite3.connect('backgrounds.db')
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
