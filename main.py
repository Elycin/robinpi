#!/usr/bin/env python3

from Robinhood import Robinhood
import configparser
import time
import pyotp

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment


def marquee_message(segment_display, msg, delay=0.2):
    # Does same as above but does string slicing itself
    width = seg.device.width
    padding = " " * width
    msg = padding + msg + padding

    for i in range(len(msg)):
        segment_display.text = msg[i:i + width]
        time.sleep(delay)


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
    mfa_code=str(totp.now())
)

while True:
    # Portfolio paypload.
    portfolio = robinhood_interface.portfolios()

    # Variables
    market_status = ""
    equity = 0.0

    # Determine market.
    if portfolio['extended_hours_portfolio_equity'] is None:
        market_status = "STOCK MARKET IS OPEN"  # Trading Hours
        equity = portfolio['equity']
    else:
        market_status = "STOCK MARKET IS CLOSED - AFTER HOURS"  # After Hours
        equity = portfolio['extended_hours_portfolio_equity']

    # Update Display.
    marquee_message(seg, market_status)
    marquee_message(seg, "YOUR EQUITY IS CURRENTLY {:0.2f} USD".format(float(equity)))

    # Loop Interval.
    time.sleep(float(config['ticker']['refresh_rate']))
