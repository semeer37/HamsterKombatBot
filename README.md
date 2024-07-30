# HamsterKombatBot for Mobile

A bot for automating tasks in the Hamster Kombat game on Telegram.

## Table of Contents
1. [Prerequisites](#prerequisites)
   - [Termux](#termux)
   - [Telegram API Keys](#telegram-api-keys)
2. [Installation](#installation)
   - [Auto Installation](#auto-installation)
   - [Manual Installation](#manual-installation)
3. [Configurations](#configurations)
   - [Settings](#settings)
   - [Profiles](#profiles)
4. [Usage](#usage)

## Prerequisites

### Termux
Download and install Termux from [Termux](https://f-droid.org/packages/com.termux/).

### Telegram API Keys
1. Go to [my.telegram.org](https://my.telegram.org) and log in using your phone number.
2. Select **"API development tools"** and fill out the form to register a new application.
3. Note down the `API_ID` and `API_HASH` for use in the configuration step.

## Installation

### Auto Installation
1. To install libraries on Termux, run the following commands:
```shell
pkg install git -y
git clone https://github.com/semeer37/HamsterKombatBot.git
cd HamsterKombatBot
./autoinstall.sh
```

### Manual Installation

```shell
# Update and upgrade Termux packages
pkg update && pkg upgrade

# Install necessary packages
pkg install git python rust

# Clone the repository
git clone https://github.com/semeer37/HamsterKombatBot.git
cd HamsterKombatBot

# Set up the virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env-example .env
nano .env # Specify your API_ID and API_HASH

# Run the bot
python main.py
```

## Configuration

### Settings
Edit the `.env` file with the following settings:

| Setting                      | Description                                                                              | Default Value                     |
|------------------------------|------------------------------------------------------------------------------------------|-----------------------------------|
| **API_ID / API_HASH**        | Platform data from which to launch a Telegram session _(stock - Android)_                |                                   |
| **MIN_AVAILABLE_ENERGY**     | Minimum amount of available energy, upon reaching which there will be a delay _(eg 100)_ | 100                               |
| **SLEEP_BY_MIN_ENERGY**      | Delay when reaching minimum energy in seconds _(eg [1800,2400])_                         | [1800, 2400]                      |
| **AUTO_UPGRADE**             | Whether to upgrade the passive earn _(True / False)_                                     | True                              |
| **MAX_LEVEL**                | Maximum upgrade level _(eg 20)_                                                          | 20                                |
| **MAX_PRICE**                | Maximum upgrade price _(eg 50000000)_                                                    | 50000000                          |
| **BALANCE_TO_SAVE**          | Balance limit that the bot "won't touch" _(eg 1000000)_                                  | 1000000                           |
| **UPGRADES_COUNT**           | The count of cards that the bot will upgrade in 1 lap _(eg 10)_                          | 10                                |
| **MAX_COMBO_PRICE**          | Maximum purchase price for buying combo cards with an available balance _(eg 10000000)_  | 10000000                          |
| **APPLY_DAILY_ENERGY**       | Whether to use the daily free energy boost _(True / False)_                              | True                              |
| **USE_TAPS**                 | Whether to use taps _(True / False)_                                                     | True                              |
| **RANDOM_TAPS_COUNT**        | Random number of taps _(eg [50,200])_                                                    | [50, 200]                         |
| **SLEEP_BETWEEN_TAP**        | Random delay between taps in seconds _(eg [10,25])_                                      | [10, 25]                          |
| **USE_RANDOM_DELAY_IN_RUN**  | Use random delay during run _(True / False)_                                             | True                              |
| **RANDOM_DELAY_IN_RUN**      | Random delay in run _(eg [0,15])_                                                        | [0, 15]                           |
| **USE_RANDOM_MINI_GAME_KEY** | Whether to use random key for mini game cipher _(True / False)_                          | True                              |
| **USE_RANDOM_USERAGENT**     | Whether to random User Agent every time to start _(True / False)_                        | True                              |

### Profiles

You can create profiles with unique data for each session:

```json
{
  "session1": {
    "proxy": "socks5://yGow3a:uBro3wL@58.195.21.83:9715",
    "headers": {"...": "..."},
    "fingerprint": {"...": "..."}
  },
  "session2": {
    "proxy": "socks5://yGow3a:uBro3wL@58.195.21.83:9715",
    "headers": {"...": "..."},
    "fingerprint": {"...": "..."}
  },
  "...": {}
}
```
> ❕ **Note**:  `session1` and `session2` are examples of session names.

## Usage

To use the bot, run the following commands in Termux:

### Create a Session
```shell
python main.py --action 1
# Or
python main.py -a 1
```

### Run the Clicker
```shell
python main.py --action 2
# Or
python main.py -a 2
```
