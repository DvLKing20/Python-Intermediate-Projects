# Telegram Advertising Bot

This bot is an asynchronous Telegram automation tool built with `python-telegram-bot`.  
It can store ads, collect group IDs, and automatically post ads on a schedule.  
The bot also uses inline buttons for navigation and per-user states for handling input.

## What the bot can do
- Add an advertisement (text, photo, or video)
- Save groups for auto-posting
- Automatically post the user's ad to all their groups
- Start/stop the auto-posting system
- Greet the user and save their private ID
- Show the bot owner (Master)
- Simple help menu and exit panel
- Restricts commands based on chat type (private/group)
- Prevents unauthorized access using `subscribers_id.txt`

## How the bot stores data
- Every user gets a text file named `<user_id>.txt` to store their group list.
- Ads are stored temporarily using `context.user_data`.
- A `subscribers_id.txt` file controls who is allowed to use higher access features.
- `PrivateUser_id.txt` stores IDs of users who use the “Greet Me” option.

## How to run
1. Install the required library:

```bash
pip install python-telegram-bot --upgrade
