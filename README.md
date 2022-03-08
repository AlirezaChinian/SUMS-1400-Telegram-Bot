# SUMS 1400 Telegram Bot v Beta
[![LICENSE](https://img.shields.io/badge/LICENSE-GPL--3.0-green)](https://github.com/AlirezaChinian/SUMS-1400-Telegram-Bot/blob/main/LICENSE)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/python-telegram-bot.svg)](https://www.python.org)
[![Bot API versions](https://img.shields.io/badge/Bot%20API-5.7-blue?logo=telegram)](https://api.telegram.org)

A Telegram Bot that sends Documents and Videos of SUMS MD 1400. This Bot also contain a Support Bot.
## Requirements
* Python3
* pip
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [prettytable](https://github.com/jazzband/prettytable)
## How to use it?
1. Install Requirements: 
```
  $ pip3 install -r requirements.txt
```
2. Run database.py to create database and tables:
```
  $ python3 database.py
```
3. Define Main Bot and Support Bot Token in config.ini
4. Define Bot admins(needs admins's chat_id) in config.ini
5. Run bot.py to start Main Bot: 
```
  $ python3 bot.py
```
6. Run talkbot.py to start Support Bot:
```
  $ python3 talkbot.py
```
## License
SUMS 1400 Telegram Bot is licensed under the [GNU General Public License v3.0](https://github.com/AlirezaChinian/SUMS-1400-Telegram-Bot/blob/main/LICENSE)

Copyright © Alireza Chinian
