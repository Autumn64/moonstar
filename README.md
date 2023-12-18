# MOONSTAR

[![Pull requests](https://img.shields.io/badge/dynamic/json.svg?label=pull%20requests&style=for-the-badge&color=limegreen&url=https://codeberg.org/api/v1/repos/Autumn64/moonstar&query=open_pr_counter)](https://codeberg.org/Autumn64/moonstar/pulls)
[![Issues](https://img.shields.io/badge/dynamic/json.svg?label=issues&style=for-the-badge&color=red&url=https://codeberg.org/api/v1/repos/Autumn64/moonstar&query=open_issues_count)](https://codeberg.org/Autumn64/moonstar/issues)
[![Stars](https://img.shields.io/badge/dynamic/json.svg?label=stars&style=for-the-badge&color=yellow&url=https://codeberg.org/api/v1/repos/Autumn64/moonstar&query=stars_count)](https://codeberg.org/Autumn64/moonstar)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green?label=license&style=for-the-badge&url=)](https://codeberg.org/Autumn64/moonstar/src/branch/main/LICENSE)

## An open-source slash commands-supporting bot for Discord.

### Description
MOONSTAR is an open-source multi-purpose bot for Discord, that supports slash-commands and basic web scraping capabilities, and that is meant to stimulate interaction between users and the activity in your server!

### Contribution Guidelines
In order to contribute, please fork this repository, and create a [pull request](https://codeberg.org/Autumn64/moonstar/pulls) with your proposed changes. You can relicense any forks you make from this project with any other license provided that you meet the requirements stipulated in the [project's original license](./LICENSE). However, any contributions made to this project must be under the BSD-3-Clause license, whether they come from a fork or not.

### Features
- Works primarily by slash commands.
- Has basic web scraping capabilities.
- Has basic moderation features.
- Includes a basic calculator and a translator.

### How to build/self-host
#### You should create a bot at the Discord Developers Portal before building/self-hosting.

- Clone this repository into your local machine.
```bash
#By HTTPS:
git clone https://codeberg.org/Autumn64/moonstar.git
```
- Create and activate a Python virtual environment.
```bash
#By venv:
python -m venv ./
source ./bin/activate
```
- Install the dependencies in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
- Create a file named `config.json` and add the parameters `token`, `bot_id` and `autumn_id` (you can change the name of `autumn_id` as long as you also do it in the source code).
```json
//Example
{
    "token": "DISCORD_TOKEN",
    "bot_id": 1234567890,
    "autumn_id": 1234567890
}
```
- That's it! Run the file `main.py` and the bot will start working.

### Extra information
Thanks so much to all of our [contributors](https://codeberg.org/Autumn64/moonstar/activity/yearly).

#### All the code in this repository is licensed under the [BSD 3-Clause license](./LICENSE). The bot's name and styles were inspirated by K-pop artist [MOONBYUL](https://en.wikipedia.org/wiki/Moonbyul), and all the resources used for the private logos and names inside the software (incluiding those of Discord and MOONBYUL) belong to their respective Copyright holders and no infraction is intended by using them. This software is meant to be distributed for non-commercial purposes, and neither this project's owner nor its contributors are responsible for the use anyone outside of it might give to the software provided and its assets.