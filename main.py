#!/usr/bin/env python3

from Robinhood import Robinhood
import configparser
import time
import pyotp

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

# Read configuration.
config = configparser.ConfigParser()
config.read('config.ini')


# Marquee function - provide the device and message.
def marquee_message(segment_display, msg):
    # Does same as above but does string slicing itself
    width = seg.device.width
    padding = " " * width
    msg = padding + msg + padding

    for i in range(len(msg)):
        segment_display.text = msg[i:i + width]
        time.sleep(float(config['ticker']['marquee_rate']))


# create seven segment device
# always use port zero because raspberry pi only has oneb
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)
seg = sevensegment(device)

# Generate a TOTP Interface using the provided secret.
totp = pyotp.TOTP(config['robinhood']['multi_factor_secret'])

# Hook Robinhood API.
robinhood_interface = Robinhood()
try:
    marquee_message(seg, "LOGGING IN TO ROBINHOOD.")
    # Attempt to login.
    robinhood_interface.login(
        username=config['robinhood']['username'],
        password=config['robinhood']['password'],
        mfa_code=str(totp.now())
    )
except Exception as e:
    marquee_message(seg, "EXCEPTION OCCURRED WHILE LOGGING IN")
    exit(1)

# Looping.
while True:
    # Portfolio payload.
    portfolio = robinhood_interface.portfolios()

    # Variables
    market_status = ""
    equity = 0.0
    equity_message = ""

    # Determine market and equity.
    if portfolio['extended_hours_portfolio_equity'] is None:
        market_status = "STOCK MARKET IS OPEN"  # Trading Hours
        equity = float(portfolio['equity'])
    else:
        market_status = "STOCK MARKET IS CLOSED - AFTER HOURS"  # After Hours
        equity = float(portfolio['extended_hours_portfolio_equity'])

    # Build equity message
    equity_message = "YOUR EQUITY IS CURRENTLY {:0.2f} USD.".format(equity)

    # Determine change
    change = float(portfolio['adjusted_portfolio_equity_previous_close']) - equity
    change_message = ""

    # Build change message
    if change == 0.0:
        change_message = "YOUR EQUITY HAS NOT CHANGED."
    elif change > 0.0:
        change_message = "YOU GAINED {:0.2f} USD SINCE LAST CLOSE.".format(change)
    else:
        change_message = "YOU LOST {:0.2f} USD SINCE LAST CLOSE.".format(change)

    # Update Display.
    marquee_message(seg, market_status)
    marquee_message(seg, equity_message)
    marquee_message(seg, change_message)

    # Loop Interval.
    time.sleep(float(config['ticker']['loop_delay']))
