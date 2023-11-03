import random
import sqlite3

from Project.bin.Scripts.Global import GlobalVars


def run(profile):
    conn = sqlite3.connect(GlobalVars.dbFile_path)
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

        # Delete background at order to prevent conflict
        cur.execute('DELETE FROM Backgrounds WHERE Num = ' + num)

        # Update existing record (if it still exists)
        cur.execute('UPDATE or REPLACE Backgrounds SET Num = ' + num + ' WHERE Path = "' + background_path + '"')

        # Insert record if it didn't exist.
        cur.execute('INSERT or IGNORE INTO Backgrounds (Num, Used, Orientation, Path) '
                    'VALUES ' + values)

    conn.commit()


if __name__ == '__main__':
    run()
