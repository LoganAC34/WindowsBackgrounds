import random

from Scripts import Config, GetBackgrounds


def run(profile):
    GetBackgrounds.run(profile)  # Manage background DB
    profile_options = Config.get_all_options_for_profile(profile)  # Get profile options
    profile_table = profile_options['database_id']  # Get profile table name
    conn, cur = Config.connect_to_db()  # Connect to db

    # Reshuffle background order
    allBackgrounds = cur.execute(f'SELECT * FROM "{profile_table}"')
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
        cur.execute(f'DELETE FROM "{profile_table}" WHERE Path = "{background_path}"')

        # Update existing record (if it still exists)
        cur.execute(f'UPDATE or REPLACE "{profile_table}" SET Num = {num} WHERE Path = "{background_path}"')

        # Insert record if it didn't exist.
        cur.execute(f'INSERT or IGNORE INTO "{profile_table}" (Num, Used, Orientation, Path) VALUES {values}')

    conn.commit()


if __name__ == '__main__':
    run(None)
