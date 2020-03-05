from Robinhood import Robinhood
import configparser
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

config = configparser.ConfigParser()
config.read('config.ini')

robinhood_interface = Robinhood()
robinhood_interface.login(
    username=config['robinhood']['username'],
    password=config['robinhood']['password'],
    qr_code=config['robinhood']['multi_factor_secret']
)

# create seven segment device
serial = spi(port=0, device=0, gpio=int(config['GPIO']['DIN']))
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

while True:
    equity = round(float(robinhood_interface.portfolios()['equity']), 2)
    print(equity)
    seg.text = str(equity)
    time.sleep(float(config['ticker']['refresh_rate']))