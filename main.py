from Robinhood import Robinhood
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

robinhood_interface = Robinhood()
robinhood_interface.login(
    username=config['robinhood']['username'],
    password=config['robinhood']['password'],
    qr_code=config['robinhood']['multi_factor_secret']
)

while True:
    equity = round(float(robinhood_interface.portfolios()['equity']), 2)
    print(equity)
    time.sleep(float(config['ticker']['refresh_rate']))