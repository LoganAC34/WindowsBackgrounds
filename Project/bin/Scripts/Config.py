import configparser

from Project.bin.Scripts.Global import GlobalVars


def get_profile_count():
    """Returns how many profiles there are.
        :return: int
    """
    # Get Config values
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)
    count = len(config.sections())
    return count


def get_profile_paths(profile: str):
    """Gets attributes from config file, allowing 'profile_name' to change when debug = True

    :param profile: 'local' or 'remote'
    :return: attribute value (string)
    """

    # Get Config values
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    return config[profile].items()


def add_profile(profile_name, paths: list=None):
    """Add new profile with specified profile name. Will return False if profile already exists.

    :param paths:
    :param profile_name: Profile name to add
    :return: True if successfully run, false otherwise.
    """
    print(f"Adding profile_name {profile_name}")

    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    # If profile already exists early return False
    if profile_name in config.sections():
        return False

    profile_paths = {}
    if paths:
        for x, path in enumerate(paths):
            profile_paths[x] = path

    config[profile_name] = profile_paths

    # Write to config file
    with open(GlobalVars.cfgFile_path, 'w') as configfile:  # save
        config.write(configfile)

    return True


def delete_profile(profile: str):
    """Delete profile_name from config file.

        :param profile: profile_name name
        :return: True if run successfully
    """
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    config.remove_section(profile)

    # Write to config file
    with open(GlobalVars.cfgFile_path, 'w') as configfile:  # save
        config.write(configfile)

    return True


def add_path(profile: str, path: str):
    """Set path of path number

        :param profile: Profile name
        :param path: Folder path
        :return: True if run successfully.
    """

    # Get Config values
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    path_number = str(len(config.sections()))
    config[profile][path_number] = path

    # Write to config file
    with open(GlobalVars.cfgFile_path, 'w') as configfile:  # save
        config.write(configfile)


def delete_path(profile: str, path: str):
    config = configparser.ConfigParser()
    config.read(GlobalVars.cfgFile_path)

    paths = get_profile_paths(profile)
    for x, key, value in enumerate(paths.items()):
        if value != path:
            config[profile][x] = value
