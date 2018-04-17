import configparser

_config_loaded = False
_config = None
CONFIG_KEY = "default"


def configinit(configfile):
    """Load the configuration file """

    global _config_loaded, _config

    if _config_loaded:
        return _config
    else:
        _config = configparser.ConfigParser()
        _config.read(configfile)
        _config_loaded = True


def set_config(key, value):
    """Set the value for some key in the configuration"""
    global _config

    _config.set(CONFIG_KEY, key, value)


def config(key, default=''):
    """Get the value for the given key in the configuration
    returning default if there is no such key"""
    global _config

    if _config.has_option(CONFIG_KEY, key):
        return _config.get(CONFIG_KEY, key)
    else:
        return default


def print_config():
    """Print out the current configuration"""
    global _config

    _config.write(sys.stdout)
