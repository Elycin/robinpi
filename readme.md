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
import pyotp
totp = pyotp.TOTP("YOUR SECRET HERE")
six_digit_code = totp.now()
```

## Installation
Note: following this segment will utilize your package manager, it must be ran as root.
```sh
git clone https://github.com/elycin/robinpi.git /opt/robinpi
cd /opt/robinpi
sudo bash install_dependencies.sh
```

## Configuring the script
- Move to working directory: `cd /opt/robinpi`
- Copy example configuration: `cp config.ini.example config.ini`
- Edit configuration and providde requirements: `nano config.ini`

You can either run the script manually by performing `python3 main.py` or by creating a systemd service below.
 
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
### Footnotes
- Storing your 2FA secret is considered insecure, this project was created in mind of being helpful, not to deliberately jeopardize your credentials if your device running this software is compromised.
- Please make sure that you properly secure down your device running this script. I am not to be held responsibile and do not provide warranty if it is compromised due to your error/lack of security.
- There is no license on this code in the repository. You are free to modify it at will.
- This code makes use of the luma.led_matrix library which contains support for multiple displays. You don't have to use a sevensegment display, but this will require modifying the code.
