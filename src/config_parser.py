import configparser

configfile = '../config.cfg'

config = configparser.ConfigParser()
config.read(configfile)


def get_api_token():
    return config['TELEGRAM']['API_TOKEN']
