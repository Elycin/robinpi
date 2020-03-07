# Robinhood Raspberry Pi Ticker for seven segment displays.
https://twitter.com/foxwithpaws/status/1235960968871624705

## Required Hardware
 - Seven Segment Display (max7219 chip)

## Robinhood Requirements
This repository makes use of the unofficial robinhood API located at https://github.com/Jamonek/Robinhood 

You will need:
- Your email
- Password
- Multi Factor Authentication Secret
    - This can be obtained by enabling 2FA/MFA, clicking "Can't scan" and copying that code.
    
## Why 2FA/MFA?
The Robinhood API Requires that you have MFA enabled in order to use the API.

This program works by utilizing the `pyotp` library in order to generate a 6 digit code in realtime with the following snippet:
```py
import pyopt
totp = pyotp.TOTP("YOUR SECRET HERE")
six_digit_code = totp.now()
```


 
## Installation
```sh
git clone https://github.com/elycin/robinpi.git /opt/robinpi
cd /opt/robinpi
# {edit config.ini.example and save as config.ini}
sudo bash install_dependencies.sh
```
 
## Systemd Service
A systemd service can be installed by saving the following file to `/lib/systemd/system/robinpi.service` and pasting the following contents:
```ini
[Unit]
Description=Robinhood Raspberry Pi Ticker
Wants=network-online.target
After=network.target network-online.target

[Service]
WorkingDirectory=/opt/robinpi
ExecStart=python3 /opt/robinpi/main.py
Type=simple
Restart=always

[Install]
WantedBy=multi-user.target
```

Once creating this file, you can enable the service by the following commands:
```sh
systemctl daemon-reload
systemctl enable robinpi
systemctl start robinpi
```
