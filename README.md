# TrackPulse Vic

A Discord bot for logging train, tram, and bus trips in Victoria, New South Wales, South Australia, and Western Australia. It provides real-time line status updates, upcoming departures, train search functionality, and much more.

## Prerequisites

- **Python 3.10+** (Python 3.12 recommended)
- **Git** (for cloning the repository)
- A Discord account
- PTV API credentials (for Victorian public transport data)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TrackPulse-Vic/TrackPulse-Vic.git
cd TrackPulse-Vic
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

First, install the special branch of discord.py with Components V2 support:

```bash
pip install -U git+https://github.com/DA-344/d.py@feat/components-v2
```

Then install the remaining requirements:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Rename `rename.env` to `.env`:
   ```bash
   # On Windows:
   ren rename.env .env
   # On macOS/Linux:
   mv rename.env .env
   ```

2. Open `.env` in a text editor and fill in the required values:

#### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token and paste it as `BOT_TOKEN` in your `.env` file
5. Under "Privileged Gateway Intents", enable the intents your bot needs
6. Go to "OAuth2" > "URL Generator", select "bot" and "applications.commands" scopes
7. Select the permissions your bot needs and use the generated URL to invite the bot to your server

#### PTV API Setup (Required for Victorian Transport Data)

To get PTV API credentials:
1. Email [APIKeyRequest@ptv.vic.gov.au](mailto:APIKeyRequest@ptv.vic.gov.au) requesting API access
2. You will receive a `DEV_ID` and `KEY` - add these to your `.env` file

#### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Your Discord bot token |
| `DEV_ID` | Your PTV Developer ID |
| `KEY` | Your PTV API Key |
| `STARTUP_CHANNEL_ID` | Discord channel ID for bot startup messages |
| `RARE_SERVICE_CHANNEL_ID` | Discord channel ID for rare service alerts |
| `USER_ID` | Your Discord user ID (for admin access) |

#### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_TOKEN` | Telegram bot token (optional) |
| `NSW_API_KEY` | NSW Transport API key (for NSW data) |
| `THUNDERFOREST_MAP` | Thunderforest API key (for map features) |
| `IMGBB` | ImgBB API key (for image hosting) |
| `LINE_STATUS_CHANNEL_ID` | Channel for line status updates |
| `RARE_SERVICE_CHECKER` | Set to `ON` or `OFF` |
| `STARTUP_REFRESH_ACHIEVEMENTS` | Set to `ON` or `OFF` |
| `AUTOMATIC_UPDATES` | Set to `ON` or `OFF` |
| `DEVS_TO_HAVE_ADMIN_ACCESS` | Set to `ON` or `OFF` |
| `HEALTHCHECK_UUID` | UUID for uptime monitoring via healthchecks.io |

### 5. Run the Bot

```bash
python bot.py
```

The bot will create necessary folders automatically on first run and connect to Discord.

## Running with Docker (Alternative)

If you prefer using Docker:

```bash
# Build the Docker image
docker build -t trackpulse-vic .

# Run the container
docker run -d --name trackpulse-vic --env-file .env trackpulse-vic
```

## Configuration Notes

- **Channel IDs**: To get a Discord channel ID, enable Developer Mode in Discord settings, then right-click on a channel and select "Copy ID"
- **User IDs**: Similarly, right-click on a user and select "Copy ID" to get user IDs
- **Admin Access**: Users listed in `admin_users` in `bot.py` have access to administrative commands
- **Changing notification channels**: If you want to change what channels the bot sends notifications in or change the role, you can find these settings in `bot.py`

## Troubleshooting

- **Bot not responding to commands**: Make sure you've synced slash commands by using the `sync` command (requires admin)
- **API errors**: Verify your PTV API credentials are correct and valid
- **Missing dependencies**: Run `pip install -r requirements.txt` again
- **Permission errors**: Ensure the bot has the necessary permissions in your Discord server

## Support

- [Discord Server](https://discord.gg/nfAqAnceQ5)
- [Report Issues on GitHub](https://github.com/TrackPulse-Vic/TrackPulse-Vic/issues)

# Contributors:
<a href="https://github.com/TrackPulse-Vic/TrackPulse-Vic/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TrackPulse-Vic/TrackPulse-Vic" />
</a>

![Alt](https://repobeats.axiom.co/api/embed/6a4b236482f2ba0941a28abe403e386543c2946b.svg "Repobeats analytics image")
