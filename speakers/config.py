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

    return _config.get(CONFIG_KEY, key, fallback=default)


def config_int(key, default=0):
    """Get the value for the given key in the configuration
    returning default if there is no such key"""

    return _config.getint(CONFIG_KEY, key, fallback=default)


def config_float(key, default=0.0):
    """Get the value for the given key in the configuration
    returning default if there is no such key"""

    return _config.getfloat(CONFIG_KEY, key, fallback=default)


def config_bool(key, default=False):
    """Get the value for the given key in the configuration
    returning default if there is no such key"""

    return _config.getboolean(CONFIG_KEY, key, fallback=default)


def items():
    """Get a list of configuration names"""

    return _config.items(CONFIG_KEY)


def print_config():
    """Print out the current configuration"""
    global _config

    _config.write(sys.stdout)
