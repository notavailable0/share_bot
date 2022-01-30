import configparser

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config['SETTINGS']['bot_token']
access_tokens = config['SETTINGS']['login_tokens_divided_by_commas'].split(',')
