#!/usr/bin/env python3

from Robinhood import Robinhood
import configparser
import time
import pyotp

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

config = configparser.ConfigParser()
config.read('config.ini')

# create seven segment device
# always use port zero because raspberry pi only has one

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)
seg = sevensegment(device)

totp = pyotp.TOTP(config['robinhood']['multi_factor_secret'])

robinhood_interface = Robinhood()
robinhood_interface.login(
    username=config['robinhood']['username'],
    password=config['robinhood']['password'],
    mfa_code=totp.now()
)

while True:
    equity = round(float(robinhood_interface.portfolios()['extended_hours_portfolio_equity']), 2)
    print(equity)
    seg.text = str(equity)
    time.sleep(float(config['ticker']['refresh_rate']))

