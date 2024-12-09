import configparser
import shutil
import sqlite3
import uuid
from os.path import exists

from Scripts.Global import GlobalVars


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


def connect_to_db():
    """
    Returns the connection and cursor of the background database, making sure it exists before connecting.
    :return: conn, cursor
    """
    if not exists(GlobalVars.dbFile_path):
        shutil.copyfile(GlobalVars.dbTemplateFile_path, GlobalVars.dbFile_path)

    conn = sqlite3.connect(GlobalVars.dbFile_path)
    cursor = conn.cursor()

    return conn, cursor
