import configparser
import sqlite3
import uuid

from Project.bin.Scripts.Global import GlobalVars


def get_all_profiles():
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)
    return config.sections()


def get_paths_for_profile(profile: str):
    """Gets paths of profile settings. DOES NOT INCLUDE ANY OTHER SETTINGS!

    :param profile: 'local' or 'remote'
    :return: attribute value (list)
    """

    # Get Config values
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    options = config[profile]

    paths = []
    for key, value in options.items():
        try:
            int(key)
            paths.append(value)
        except ValueError:
            pass

    return paths


def get_options_for_profile(profile: str):
    """Gets options other than paths. DOES NOT INCLUDE PATHS!

    :param profile: 'local' or 'remote'
    :return: attribute value (dict)
    """

    # Get Config values
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    options = config[profile]

    settings = {}
    for key, value in options.items():
        try:
            int(key)
        except ValueError:
            settings[key] = value

    return settings


def get_all_options_for_profile(profile: str):
    """
    Get all settings for profile.
    :param profile: profile name
    :return: profile settings (dict)
    """

    # Get Config values
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    options = config[profile]

    return options

def add_or_update_profile(profile_name: str, options: dict = None):
    """Add new or overwrites existing profile with specified profile name.
    Returns False if profile already exists and True if otherwise.

    :param options:
    :param profile_name: Profile name
    :return: True if profile is new, false otherwise.
    """
    print(f"Adding profile_name {profile_name}")

    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    output = False
    if profile_name not in config.sections():
        output = True

    # Give database unique ID if one does not exist
    if 'database_id' not in options or not options['database_id']:
        options['database_id'] = uuid.uuid4().hex

    config[profile_name] = options

    # Write to config file
    with open(GlobalVars.cfgFile_path, 'w') as configfile:  # save
        config.write(configfile)

    return output


def delete_unused_profiles(profiles_to_keep: list):
    """Delete profile_name from config file.

        :param profiles_to_keep: profile_names to keep
        :return: True if run successfully
    """
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    all_profiles = get_all_profiles()
    for profile in all_profiles:
        if profile not in profiles_to_keep:
            config.remove_section(profile)

    # Write to config file
    with open(GlobalVars.cfgFile_path, 'w') as configfile:  # save
        config.write(configfile)


def create_new_dataset_for_profile(profile_name: str):
    # Connect to the SQLite database
    conn = sqlite3.connect(GlobalVars.dbFile_path)
    cursor = conn.cursor()

    # Define the source table name and the new table name
    source_table_name = 'original_table'  # Replace with your source table name
    new_table_name = 'copied_table'  # Replace with your desired new table name

    # 1. Get the schema of the original table
    cursor.execute(f"PRAGMA table_info({source_table_name})")
    columns = cursor.fetchall()

    # 2. Create a new table with the same schema
    create_table_query = f"CREATE TABLE IF NOT EXISTS {new_table_name} ("
    create_table_query += ', '.join([f"{col[1]} {col[2]}" for col in columns])
    create_table_query += ")"
    cursor.execute(create_table_query)
    conn.commit()

    # 3. Optionally, copy indexes, constraints, and triggers
    # You can query the sqlite_master table for this information and create them for the new table

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()
