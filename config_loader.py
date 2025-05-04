import configparser

APP = "app"
VALUE_AGENT = 'value_agent'
STYLE_AGENT = 'style_agent'

def load_config(file_path):
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(file_path)
    return config
