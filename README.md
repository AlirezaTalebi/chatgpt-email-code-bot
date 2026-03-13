# chatgpt-email-code-bot

A simple Telegram bot that reads your email inbox through IMAP and sends the latest ChatGPT verification code back to Telegram.

This project uses Kurigram.

## Features

- Supports Gmail and Yahoo
- Reads recent email headers through IMAP
- Extracts numeric verification codes from email subjects
- Replies only in allowed Telegram chats

## Requirements

- Python 3.11+
- A Telegram API ID and API hash
- An email account with IMAP enabled
- An app password for your email account

## Installation

1. Clone the repository.
2. Install dependencies:

   `pip install -r requirements.txt`
3. Copy [config.example.py](config.example.py) to `config.py`.
4. Fill in your real values in `config.py`.

## Export requirements

To export the exact packages from your virtual environment, run:

`./bin/python -m pip freeze > requirements.txt`

Current dependencies are listed in [requirements.txt](requirements.txt).

## Configuration

Example configuration is provided in [config.example.py](config.example.py).

- `USERNAME`: your email address
- `PASSWORD`: your email app password
- `APP['session']`: Telegram session name
- `APP['api_id']`: Telegram API ID
- `APP['api_hash']`: Telegram API hash
- `MAIL`: `GMAIL` or `YAHOO`
- `CHAT_IDS`: allowed Telegram chat IDs

## Usage

Run the bot:

`python main.py`

Then send this command in an allowed chat:

`code`

## Disclaimer

There is no guarantee for this project.

You can simply fork it and adapt it to your own needs.
