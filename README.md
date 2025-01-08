# Web Scraping Project

## Disclaimer

This project is intended for educational and research purposes only. Please ensure that you have permission to scrape the websites you target and comply with their terms of service. Unauthorized scraping may lead to legal consequences, including potential lawsuits or IP bans. I shall not be held responsible for any misuse or legal issues arising from the use of this tool.

## Overview

This project is a Python-based web scraping tool that extracts data from udemy course listing websites. It utilizes libraries such as `BeautifulSoup`, `requests`

## Features

- Scrapes data from specified web page.
- Exports scraped data to SQLite database.
- Configurable settings for user agents and request headers.
- Sends scraped data as Telegram message

## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup4` library
- `sqlalchemy` library
- `lxml` library
- `python-dotenv` library

You can install the required libraries using pip:
```
pip3 install -r requirements.txt
```

## Setup steps
- Clone the repository
- Create virual environment by using `python3 -m venv venv`
- Activate virtual environment (search the internet on how to do it based on Operating Sytem) it should be easy
	Example for windows: `venv/Scripts/activate`
	Example for linux: `source venv/bin/activate`
- Create a Telegram bot
	- search @BotFather
	- from the menu select create a new bot and follow the instructions
	- copy the bot token which will in be in this format `1234567890:04b28e11342FC821c85Afca6d984c888Ea8`
	- make a .env file and paste bot token as `TELEGRAM_BOT_TOKEN="<your bot token>"` example `TELEGRAM_BOT_TOKEN="1234567890:04b28e11342FC821c85Afca6d984c888Ea8"`
	- visit the bot and send a text message like hello, then visit `https://api.telegram.org/bot<your bot token>/getUpdates` it will give json response in that response look for "chat" section from that section copy value of "id" key which would look like `1234567890`
	- paste chat id in .env file as `TELEGRAM_CHAT_ID="<your chat id>"` example `TELEGRAM_CHAT_ID="1234567890"`
	- enter `WEBSITE_URL = <website link>` and save the .env file
- install requirements by running `pip3 install -r requirements.txt`
- File tree should look like this after following setup steps
```
.
├── .env
├── .git
├── .gitignore
├── LICENSE
├── README.md
├── models.py
├── requirements.txt
├── user_agets_browsers.txt
├── venv
└── webscrapper.py
```
- make sure to check and make changes to necessary parts of the code according to the needs. because the target website response varies
- Run the tool by using `python3 webscrapper.py`
