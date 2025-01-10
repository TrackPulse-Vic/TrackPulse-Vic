'''TrackPulse 𝕍𝕀ℂ
    Copyright (C) 2024  Billy Evans

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''


from calendar import c
import operator
from shutil import ExecError
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import re
import asyncio
import threading
import queue
from datetime import datetime
import time
import csv
import random
import pandas as pd
from typing import Literal, Optional
import typing
import enum
from re import A
from io import StringIO
import numpy as np
import io
import pytz
from concurrent.futures import ThreadPoolExecutor
import traceback

from utils import trainset
from utils.search import *
from utils.colors import *
from utils.stats.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *
from utils.trainlogger.achievements.check import checkAchievements, getAchievementInfo
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.trainlogger.graph import *
from utils.locationFromNumber import *
from utils.photo import *
from utils.mykipython import *
from utils.myki.savelogin import *
from utils.special.yearinreview import *
from utils.stoppingpattern import *
from utils.locationfromid import *
from utils.stationDisruptions import *
from utils.stats.stats import *
from utils.trainlogger.achievements import *

# settings
rareCheckerOn = False
lineStatusOn = False
admin_users = [1002449671224041502, 780303451980038165]


print("""TrackPulse VIC Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions""")

file = open('utils\\datalists\\stations.txt','r')
stations_list = []
for line in file:
    line = line.strip()
    stations_list.append(line)
file.close()

file = open('utils\\datalists\\lines.txt','r')
lines_list = []
for line in file:
    line = line.strip()
    lines_list.append(line)
file.close()

file = open('utils\\datalists\\nswstations.txt','r')
NSWstations_list = []
for line in file:
    line = line.strip()
    NSWstations_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidestations.txt','r')
Adelaidestations_list = []
for line in file:
    line = line.strip()
    Adelaidestations_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidelines.txt','r')
Adelaidelines_list = []
for line in file:
    line = line.strip()
    Adelaidelines_list.append(line)
file.close()

file = open('utils\\datalists\\perthlines.txt','r')
Perthlines_list = []
for line in file:
    line = line.strip()
    Perthlines_list.append(line)
file.close()

file = open('utils\\datalists\\perthstations.txt','r')
Perthstations_list = []
for line in file:
    line = line.strip()
    Perthstations_list.append(line)
file.close()

file = open('utils\\datalists\\busOps.txt','r')
busOps = []
for line in file:
    line = line.strip()
    busOps.append(line)
file.close()

file = open('utils\\datalists\\interchangestations.txt','r')
interchange_stations = []
for line in file:
    line = line.strip()
    interchange_stations.append(line)
file.close()


vLineLines = ['Geelong','Warrnambool', 'Ballarat', 'Maryborough', 'Ararat', 'Bendigo','Echuca', 'Swan Hill','Albury', 'Seymour', 'Shepparton', 'Traralgon', 'Bairnsdale']


# Global variable to keep track of the last sent message
last_message = None
comeng_last_message = None
last_message_metro = None
comeng_last_message_metro = None
last_message_vline = None
comeng_last_message_vline = None

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
STARTUP_CHANNEL_ID = int(config['STARTUP_CHANNEL_ID']) # channel id to send the startup message
RARE_SERVICE_CHANNEL_ID = int(config['RARE_SERVICE_CHANNEL_ID'])
COMMAND_PREFIX = config['COMMAND_PREFIX']
USER_ID = config['USER_ID']

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())
log_channel = bot.get_channel(STARTUP_CHANNEL_ID)

channel_game_status = {} #thing to store what channels are running the guessing game

try:    
    os.mkdir('utils/game/scores')
except FileExistsError as e:
    print(e)    

# Group commands
class CommandGroups(app_commands.Group):
    ...

trainlogs = CommandGroups(name='log')
games = CommandGroups(name='games')
search = CommandGroups(name='search')
stats = CommandGroups(name='stats')
myki = CommandGroups(name='myki')
completion = CommandGroups(name='completion')
achievements = CommandGroups(name='achievements')

# flight = CommandGroups(name='flight')
def download_csv(url, save_path):
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"CSV downloaded successfully and saved as {save_path}")
        else:
            raise Exception(f"Failed to download CSV. Status code: {response.status_code}")

@bot.event
async def on_ready():
    # download the trainset data     
    csv_url = "https://railway-photos.xm9g.net/trainsets.csv"
    save_location = "utils/trainsets.csv"
    print(f"Downloading trainset data from {csv_url} to {save_location}")
    download_csv(csv_url, save_location)
    
    channel = bot.get_channel(STARTUP_CHANNEL_ID)

    bot.tree.add_command(trainlogs)
    bot.tree.add_command(games)
    bot.tree.add_command(search)
    bot.tree.add_command(stats)
    bot.tree.add_command(myki)
    bot.tree.add_command(completion)
    bot.tree.add_command(achievements)

    await channel.send(f"""TrackPulse 𝕍𝕀ℂ Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions\nBot is online!""")
    try:
        task_loop.start()
    except:
        print("WARNING: Rare train checker is not enabled!")
        await channel.send(f"WARNING: Rare train checker is not enabled! <@{USER_ID}>")

    activity = discord.Activity(type=discord.ActivityType.watching, name='Melbourne trains')
    await bot.change_presence(activity=activity)
    print("Bot started")

# achievement awarder  check achievements
async def addAchievement(username, ctx, mention):
    new = checkAchievements(username)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement get!', color=0x43ea46)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await ctx.channel.send(mention,embed=embed)

# Rare train finder
def check_rare_trains_in_thread():
    rare_trains = checkRareTrainsOnRoute()
    asyncio.run_coroutine_threadsafe(log_rare_trains(rare_trains), bot.loop)

async def log_rare_trains(rare_trains):
    log_channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)
    channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)

    if rare_trains:
        embed = discord.Embed(title="Trains found on lines they are not normally on!", color=0xf23f42)

        for route in rare_trains:
            parts = route.split(' - Train ')
            route_name = parts[0]
            train_type = parts[1]
            
            # Extract the train name and train info from train_type
            train_name, train_info = train_type.split('\n') if '\n' in train_type else ('Unknown train name', 'Unknown train type')

            embed.add_field(name=route_name, value=f"{train_name}\n{train_info}", inline=True)

        try:
            await channel.send(embed=embed)
            with open('logs.txt', 'a') as file:
                file.write(f"Sent rare trains")
        except discord.HTTPException:
            await channel.send("Embed too big! There are many trains on the wrong line. Check ANYTRIP.")
            with open('logs.txt', 'a') as file:
                file.write(f"Sent rare trains but it was too long")
        await channel.send('<@&1227171023795781694> Trains found on lines they are not normally on!\n`Due to errors in the PTV api data out of our control, some data may be inaccurate.`')
    else:
        await log_channel.send("None found")

# def check_lines_in_thread():
#     asyncio.run_coroutine_threadsafe(checklines(), bot.loop)

                 

@tasks.loop(minutes=10)
async def task_loop():
    if rareCheckerOn:
        log_channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)
        await log_channel.send("Checking for trains on lines they aren't meant for")
        with open('logs.txt', 'a') as file:
            file.write(f"Checking for rare trains")

        # Create a new thread to run checkRareTrainsOnRoute
        thread = threading.Thread(target=check_rare_trains_in_thread)
        thread.start()
    else:
        print("Rare checker not enabled!")

# @tasks.loop(minutes=15)
# async def task_loop():
    # Create a new thread to run checkRareTrainsOnRoute
    # thread = threading.Thread(target=check_lines_in_thread)
    # thread.start()


# Help command
help_commands = ['Which /log command should I use?','/about','/achievements view','/completion sets','/completion stations','/departures','/games station-guesser','/games station-order','/help','/line-status','/log adelaide-train','/log bus','/log delete','/log perth-train','/log stats','/log sydney-train','/log sydney-tram','/log train','/log tram','/log view','/metro-line','/myki calculate-fare','/myki save-login','/myki view','/search route','/search td-number','/search train','/search train-photo','/search tram','/stats leaderboard','/stats profile','/stats termini','/submit-photo','/wongm','/year-in-review']

async def help_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = help_commands.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

@bot.tree.command(name="help", description="Lists available commands by category, or learn more about a specific command.")
@app_commands.describe(category="Choose a command category", command='Learn more about how to use a specific command.')
@app_commands.choices(category=[
    app_commands.Choice(name="General", value="general"),
    app_commands.Choice(name="Search", value="search"),
    app_commands.Choice(name="Logs", value="logs"),
    app_commands.Choice(name="Fun", value="fun"),
    app_commands.Choice(name="Myki", value="myki"),
])
@app_commands.autocomplete(command=help_autocompletion)

async def help(ctx, category: app_commands.Choice[str] = None, command:str=None):
    log_command(ctx.user.id, 'help')
    categories = {
        "search": [
            "</search train:1240101357847838814> - Shows information about a specific train. For multiple units use the carriage number otherwise use the locomotive number. Will show live tracking info if avaliable",
            "</departures:1288002114466877529> - Shows the next Metro trains departing a station. Includes information about which exact train is running the service.",
            "</search td-number:1240101357847838814> - Shows the run for a TD number. You can find a TDN from the departures command. Currently only Metro is supported.",
            "</search tram:1240101357847838814> - Shows information about a specific tram.",
            "</metro-line:1288004355475111938> - Shows disruption information for a Train line.",
            "</search route:1240101357847838814> - Shows disruption information for a Tram or Bus route.",
            "</search train-photo:1240101357847838814> - Shows photos of a specific train from https://railway-photos.xm9g.net\nIncludes the option to search for all carriages in a set.",
            "</wongm:1288004355475111939> - Searches Wongm's Rail Gallery"
        ],
        "general": [
            "</about:1322339128121102357> - Shows information about the bot.",
            "</submit-photo:1240999419470413875> - Submit a photo to the bot and [website](https://railway-photos.xm9g.net)",
            "</stats profile:1240101357847838815> - View your profile with key stats from your logs and games.",
        ],
        "fun": [
            "</games station-guesser:1240101357847838813> - Play a game where you guess what station a photo was taken at.",
            "</games station-order:1240101357847838813> - Play a game where you recall which stations are up or down from a specific station.",
            "</stats leaderboard:1240101357847838815> - Shows the leaderboards for the games."
        ],
        "logs":
        [
            "</log train:1289843416628330506> - Log a Melbourne/Victorian train you have been on. The full set and type will be autofilled by inputting a carriage number, for locomotive serviced use the locomotive number. If you don't know any of the information you can type 'Unknown'.",
            "</log tram:1289843416628330506> - Log a Melbourne tram, works in a similar way to log train.",
            "</log sydney-train:1289843416628330506> - Log a Sydney train, works in a similar way to log train however the set and type will not be autofilled.",
            "</log sydney-tram:1289843416628330506> - Log a Sydney tram, works the exact same as the log sydney-train.",
            "</log adelaide-train:1289843416628330506> - Log an Adelaide train. The type will be autofilled from the carriage number.",
            "</log perth-train:1289843416628330506> - Log a Perth train. The type will be autofilled from the carriage number.",
            "</log bus:1289843416628330506> - Log any bus or coach.",
            'For a comprehensive guide of which of these log commands to use in which situation, type open </help:1261177133372280957> and in the "commands" option choose "Which /log command should I use?"',
            "</log stats:1289843416628330506> - View stats for your logs such as top lines, stations, sets etc. You can view your stats in many diffrent ways.",
            "</log view:1289843416628330506> - View your logs",
            "</completion sets:1304404972229623829> - View which sets you have been on for a specific train.",
            "</completion stations:1304404972229623829> - View which stations you have been to.",
            "</stats termini:1240101357847838815> - View which Victorian ail termini you've been to.",
            "</achievements view:1327085604789551134> - View the achievements you've unlocked by logging Victorian Trains."
        ],
        "myki":
        [
            "</myki calculate-fare:1289843416628330507> - Calculate the cost of a trip on the Myki network.",
            "Please note that the following commands are currently broken and won't work:",
            "</myki save-login:1289843416628330507> - Save your username and password for PTV so you can view your Mykis on this bot.",
            "</myki view:1289843416628330507> - View your Mykis and their balance."
        ]
    }
    
    commands = {
        "Which /log command should I use?": """Depending on which region you're in and which type of public transport you are using, you will use a different command to log your trips.""",
        '/about': '''</about:1322339128121102357> is a command that displays a brief summary of this bot and credits''',
        '/achievements view': '''</achievements view:1327085604789551134> is a command that allows you to view all of the achievements you've unlocked. You unlock achievements every time you add a log that meets the requirement for the achievement. Note that achievements are currently only for logs you log with </log train:1289843416628330506>.

                        **Options:**

                        Optional:
                        User: pick a the user who's logs you're looking at the achievements for. By default it's set to you.''',
        '/completion sets': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/completion stations': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/departures': '''</departures:1288002114466877529> is a command that allows you to view the next 9 Metro services departing from any station in Melbourne.

                        **Options:**

                        Required:
                        Station: the station you wish to see the departures from. You must choose from the list.

                        Optional:
                        Line: if you wish to only see departures for services going along a specific line, you may select that line. You must choose from the list.''',
        '/games station-guesser': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/games station-order': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        "/help": """</help:1261177133372280957> is a command... wait a minute. If you've gotten this far I think you know how to use this command. And besides, just /help by itself gives the tutorial for this command.""",
        '/line-status': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/log adelaide-train': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/log bus': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/log perth-train': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        "/log stats": """</log stats:1289843416628330506> is a command to view statistics drawn from a person's logs. There are many statistics you can view, many ways of displaying the graphs, and you can view the statistics of any person who has used the bot.

                        **Options:**

                        Required:
                        Stat: choose a statistic to view from the list. The choices are:\n"Lines": which lines you've riden and how many times you've riden them,\n"Stations": which stations you've gotten on/off at and how many times you've gotten on/off at them,\n"Trips": which trips you've taken and how many times you've taken them,\n"Trip Length (VIC Train Only)": every VIC Train trip you've taken, with the first log it appears in, sorted by length,\n"Sets": which train sets you've riden and how many times you've riden them,\n"Dates": which dates you've logged and how many logs you logged that day,\n"Types": which types of train you've riden and how many times you've riden them and\n"Operators": which Public Transport Operators you've used and how many times you've used them

                        Optional:
                        Format: what format you want the statistic to be displayed in.\nEach statistic has a default format, generally chosen to display the data in the most convenient way. Choose from the list to override the default format 
                        Global_stats: True or False. False by default. If you choose true, it will use all the logs in the system instead of one specific person.
                        User: pick a the user who's logs you're looking at the statistic for. By default it's set to you.
                        Mode: what set of logs are you accessing. By default it's set to "All": all of the logs for that user.
                        """,
        '/log sydney-train': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/log sydney-tram': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        "/log train": """</log train:1289843416628330506> is a command to log any Metro and V/Line train trips. You can also log some heritage trips in Victoria. Make sure to log each different leg of your trip seperately.

                        **Options:**

                        Required:
                        Line: which line you rode on. You have to choose one of the options or type a custom one. If you don't know, tyoe "Unknown".
                        Number: which carriage you rode. Examples include "1M", "2111", "N452", "9026". If you don't know, type "Unknown".
                        Start: the starting station of your trip. You can choose from the list or type your own.
                        End: the ending station of your trip. You can choose from the list or type your own.

                        Optional:
                        Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
                        Traintype: if there are multiple trains with the same number, or you didn't input a number, specify which traintype you rode on. You generally don't need this if you know the train number, it's generally only needed for heritage trips.
                        Notes: add any notes you want to add to your log.
                        """,
        '/log tram': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/log view': '''</log view:1289843416628330506> is a command allows you to view all the logs recorded by a user.

                        Options:

                        Optional:
                        Mode: which set of logs you want to few. By default it is set to "Victorian Trains"
                        User: pick a user who's logs you wish to view. By default it's set to you.
                        Id: if you wish to view a specific log instead of all of your logs, input that log's ID. Examples include "#18A", "#1", "#F"''',        
        '/metro-line': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/myki calculate-fare': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/myki save-login': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/myki view': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/search route': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/search td-number': '''</search td-number:1240101357847838814> is a command that allows you to search the details of a specific Metro service that ran/is running/will run today. You can get the TDN for the service from </departures:1288002114466877529>.

                        **Options:**

                        Required:
                        Td: input the TDN for the run.

                        Optional:
                        Mode: choose which Operator you would like to search the run for. It is set to Metro by default. Currently Metro is also the only option.''',
        "/search train": """</search train:1240101357847838814> is a command to look up any Victorian train (except locomotive hauled carriages or freight cars). It will give you a overview of the train, including photos and status, along with the ability to see the current runs for Metro trains.

                        **Options:**

                        Required:
                        Train: input the Number of the train you're searching. Examples include "1M", "9026", "N452", "2111".

                        Optional:
                        Show_run_info: True or False. True by default. If you choose false, it will not show the run info for the train. 
                        """,
        '/search train-photo': '''</search train-photo:1240101357847838814> is a command to view the all the photos in the Xm9G photo archive for a specific train.

                        **Options:**

                        Required:
                        Number: input the number of the train you're searching. Examples include "1M", "9026", "N452", "2111".
                        Optional:
                        Search_set: True or False. False by default. If you choose true, it will include the photos from the other carriages in the train set (if there are others).''',
        '/search tram': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/stats leaderboard': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/stats profile': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/stats termini': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/submit-photo': """</submit-photo:1240999419470413875> is a command that allows you to submit a photograph of a train to the archive this bot pulls from.\nThese photos will be used by the bot in the </search train:1240101357847838814> and </search train-photo:1240101357847838814> commands to represent a specific trainset, and will be available for viewing on the [Xm9G photo gallery website](https://railway-photos.xm9g.net).\nIn all 3 uses, credit will be provided in the form of "photo by [your name]". If you would like to choose your name, contact Xm9G, otherwise he will use your Discord name (without emojis).

                        **Options:**

                        Required:
                        Photo: attach the photo you would like to submit
                        Car_number: input the ID of the train the photo is of. Examples include "1M", "9026", "N452", "2111", "ACN9", although they do not have to be Victorian trains. If there are multiple trains, include as many of them as you want, with each ID seperated by a comma. Note that Xm9G manually reads this so any info in any understandable form is acceptable.
                        Date: the date the photo was taken. While the date format YYYY-MM-DD is preferred, note that Xm9G manually reads this so any info in any understandable form is acceptable.
                        Location: input the name of the location the photo was taken. Note that Xm9G manually reads this so any info in any understandable form is acceptable.""",
        '/wongm': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>''',
        '/year-in-review': '''Unfortunately the entry for this command hasn't been completed. We're working on it right now. The list of commands who's entries are finished is:</about:1322339128121102357>, </achievements view:1327085604789551134>, </departures:1288002114466877529>, </help:1261177133372280957>, </log stats:1289843416628330506>, </log train:1289843416628330506>, </log view:1289843416628330506>, </search td-number:1240101357847838814>, </search train:1240101357847838814>, </search train-photo:1240101357847838814>, </submit-photo:1240999419470413875>'''
    }

    if category is None and command is None:
        embed = discord.Embed(title="Help Categories", description="Please select a category, or select an exact command to learn more info about it. If you still can't find what your looking for [join our discord](https://discord.gg/nfAqAnceQ5)", color=discord.Color.blue())

    elif command is None:
        chosen_category = category.value
        if chosen_category in categories:
            commands_in_category = categories[chosen_category]  # Renamed to avoid shadowing 'commands'
            embed = discord.Embed(title=f"{chosen_category.capitalize()} Commands", description="Here are the available commands:", color=discord.Color.blue())
            
            # Reset joinedcommands for each field to avoid duplication
            for cmd in commands_in_category:
                embed.add_field(name="\u200b", value=cmd, inline=False)  # Use zero-width space for invisible field name
        else:
            embed = discord.Embed(title="Invalid Category", description="Please choose a valid category.", color=discord.Color.red())
    elif category is None:
        chosen_command = command
        if chosen_command in commands:
            command_data = commands[chosen_command]  # Avoid shadowing 'commands'
            embed = discord.Embed(title=chosen_command, description=str(command_data), color=discord.Color.blue())  # Convert list to string
            if command == 'Which /log command should I use?': embed.add_field(name="", value="""Victoria:
                        Metro Trains Melbourne: </log train:1289843416628330506>
                        V/Line Rail: </log train:1289843416628330506>
                        NSW TrainLink Rail: </log sydney-train:1289843416628330506>
                        Journey Beyond Rail: </log adelaide-train:1289843416628330506>
                        Yarra Trams: </log tram:1289843416628330506>
                        PTV Bus: </log bus:1289843416628330506>
                        V/Line Coach: </log bus:1289843416628330506>
                        NSW TrainLink Coach: </log bus:1289843416628330506>
                        Other Bus/Coach: </log bus:1289843416628330506>
                        Heritage Train On Mainline: </log train:1289843416628330506>
                        Heritage Railway: </log train:1289843416628330506>
                        Heritage Tram On Mainline: Currently Not Available
                        Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""New South Wales:
                        Sydney Trains: </log sydney-train:1289843416628330506>
                        Sydney Metro: </log sydney-train:1289843416628330506>
                        NSW TrainLink Rail: </log sydney-train:1289843416628330506>
                        Journey Beyond Rail: </log adelaide-train:1289843416628330506>
                        V/Line Rail: </log train:1289843416628330506>
                        Sydney Light Rail: </log sydney-tram:1289843416628330506>
                        Newcastle Light Rail: </log sydney-tram:1289843416628330506>
                        Sydney Ferries: Currently Not Available
                        Newcastle Ferries: Currently Not Available
                        Transport for NSW Bus: </log bus:1289843416628330506>
                        NSW TrainLink Coach: </log bus:1289843416628330506>
                        V/Line Coach: </log bus:1289843416628330506>
                        Other Bus/Coach: </log bus:1289843416628330506>"""); embed.add_field(name="", value="""New South Wales Cont.:
                        Heritage Train On Mainline: Currently Not Available
                        Heritage Railway: Currently Not Available
                        Heritage Tram On Mainline: Currently Not Available
                        Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""South Australia:
                        Adelaide Metro Rail: </log adelaide-train:1289843416628330506>
                        Journey Beyond Rail: </log adelaide-train:1289843416628330506>
                        Adelaide Metro Tram: Currently Not Available
                        Adelaide Metro Bus: </log bus:1289843416628330506>
                        Adelaide Metro Regional Bus and Coach: </log bus:1289843416628330506>
                        V/Line Coach: </log bus:1289843416628330506>
                        NSW TrainLink Coach: </log bus:1289843416628330506>
                        Other Bus/Coach: </log bus:1289843416628330506>
                        Heritage Train On Mainline: Currently Not Available
                        Heritage Railway: Currently Not Available
                        Heritage Tram On Mainline: Currently Not Available
                        Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""Western Australia:
                        Transperth Rail: </log perth-train:1289843416628330506>
                        Transwa Rail: </log perth-train:1289843416628330506>
                        Journey Beyond Rail: </log adelaide-train:1289843416628330506>
                        Transperth Ferries: Currently Not Available
                        Transperth Bus: </log bus:1289843416628330506>
                        Transwa Coach: </log bus:1289843416628330506>
                        Other Bus/Coach: </log bus:1289843416628330506>
                        Heritage Train On Mainline: Currently Not Available
                        Heritage Railway: Currently Not Available
                        Heritage Tram On Mainline: Currently Not Available
                        Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""Northern Territory
                        Journey Beyond Rail: </log adelaide-train:1289843416628330506>
                        Darwinbus: </log bus:1289843416628330506>
                        Other Bus/Coach: </log bus:1289843416628330506>
                        Heritage Train On Mainline: Currently Not Available
                        Heritage Railway: Currently Not Available
                        Heritage Tram On Mainline: Currently Not Available
                        Heritage Tramway: Currently Not Available

                        Other regions:
                        Any Bus/Coach: </log bus:1289843416628330506>""")
        else:
            embed = discord.Embed(title="Invalid Command", description="Please choose a valid command.", color=discord.Color.red())  # Corrected title for clarity
    else: 
        ctx.response.send_message('You cant choose both a category and a command!')
        return
    
    await ctx.response.send_message(embed=embed)


    
@bot.tree.command(name="metro-line", description="Show info about a Metro line")
@app_commands.describe(line="What Metro line to show info about?")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.choices(
    line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Frankston", value="Frankston"),
        app_commands.Choice(name="Glen Waverley", value="Glen%20Waverley"),
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Lilydale", value="Lilydale"),
        app_commands.Choice(name="Mernda", value="Mernda"),
        app_commands.Choice(name="Pakenham", value="Pakenham"),
        app_commands.Choice(name="Sandringham", value="Sandringham"),
        app_commands.Choice(name="Stony Point", value="Stony%20Point"),
        app_commands.Choice(name="Sunbury", value="Sunbury"),
        app_commands.Choice(name="Upfield", value="Upfield"),
        app_commands.Choice(name="Werribee", value="Werribee"),
    ]
)
async def line_info(ctx, line: str):
    """
    This function retrieves information about a Metro line and sends it as an embed to the Discord channel.

    Args:
        ctx (ApplicationContext): The context of the command.
        line (str): The name of the Metro line to retrieve information about.

    Returns:
        None
    """
    log_command(ctx.user.id, 'line_info')

    # Retrieve line information from API
    json_info_str = route_api_request(line, "0")
    json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
    json_info = json.loads(json_info_str)

    routes = json_info["routes"]
    status = json_info["status"]
    version = status["version"]
    health = status["health"]

    route = routes[0]
    route_service_status = route["route_service_status"]
    description = route_service_status["description"]
    timestamp = route_service_status["timestamp"]
    route_type = route["route_type"]
    route_id = route["route_id"]
    route_name = route["route_name"]
    route_number = route["route_number"]
    route_gtfs_id = route["route_gtfs_id"]
    geopath = route["geopath"]

    print(f"route id: {route_id}")

    # Retrieve disruption information
    disruption_description = ""
    try:
        disruptions = disruption_api_request(route_id)
        print(disruptions)

        # Extracting title and description
        general_disruption = disruptions["disruptions"]["metro_train"][0]
        disruption_title = general_disruption["title"]
        disruption_description = general_disruption["description"]

    except Exception as e:
        print(e)

    # Determine the color of the embed based on the status description
    color = genColor(description)
    print(f"Status color: {color}")

    # Create the embed with the retrieved information
    embed = discord.Embed(title=f"Route Information - {route_name}", color=color)
    embed.add_field(name="Route Name", value=route_name, inline=False)
    embed.add_field(name="Status Description", value=description, inline=False)
    if disruption_description:
        embed.add_field(name="Disruption Info", value=disruption_description, inline=False)

    # Send the embed to the Discord channel
    await ctx.response.send_message(embed=embed)

    # Log the command usage
    with open("logs.txt", "a") as file:
        file.write(
            f"\n{datetime.datetime.now()} - user sent line info command with input {line}"
        )

# Route Seach v2
@search.command(name="route", description="Show info about a tram or bus route")
@app_commands.describe(rtype = "What type of transport is this route?")
@app_commands.choices(rtype=[
        app_commands.Choice(name="Tram", value="1"),
        # app_commands.Choice(name="Metro Train", value="0"),
        app_commands.Choice(name="Bus", value="2"),
        # app_commands.Choice(name="VLine Train", value="3"),
        app_commands.Choice(name="Night Bus", value="4"),
])
@app_commands.describe(number = "What route number to show info about?")

async def route(ctx, rtype: str, number: int):  
    log_command(ctx.user.id, 'route_search')
    try:
        json_info_str = route_api_request(number, rtype)
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {number}:")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=0xff8200)
        counter = 0
        for route in json_info['routes']:

            routes = json_info['routes']
            status = json_info['status']
            version = status['version']
            health = status['health']
        
        
            route = routes[counter]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            timestamp = route_service_status['timestamp']
            route_type = route['route_type']
            route_id = route['route_id']
            route_name = route['route_name']
            route_number = route['route_number']
            route_gtfs_id = route['route_gtfs_id']
            geopath = route['geopath']
            
             # disruption info
            disruptionDescription = ""
            try:
                disruptions = disruption_api_request(route_id)
                # print(disruptions)
                
                # Extracting title and description
                general_disruption = disruptions["disruptions"]["metro_bus"][0]
                disruptionTitle = general_disruption["title"]
                disruptionDescription = general_disruption["description"]


                
            except Exception as e:
                print(e)

            
            # disruption status:

             # Check if the route number is the one you want
            if route_number == str(number):
                # Create and send the embed only for the desired route number
                embed = discord.Embed(title=f"Route {route_number}:", color=getColor(rtype))
                embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
                embed.add_field(name="Status Description", value=description, inline=False)
                if disruptionDescription:
                    embed.add_field(name="Disruption Info",value=disruptionDescription, inline=False)
                    
                await channel.send(embed=embed)
                with open('logs.txt', 'a') as file:
                    file.write(f"\n{datetime.datetime.now()} - user sent route search command with input {rtype}, {number}")
                                
            counter = counter + 1
                
    except Exception as e:
        await ctx.response.send_message(f"error:\n`{e}`\nMake sure you inputted a valid route number, otherwise, the bot is broken.")
        with open('logs.txt', 'a') as file:
                    file.write(f"\n{datetime.datetime.now()} - ERROR with user command - user sent route search command with input {rtype}, {number}")



# Photo search
@search.command(name="train-photo", description="Search for xm9g's railway photos")
@app_commands.describe(number="Carriage number", search_set="Search the full set instead of the train number")
async def line_info(ctx, number: str, search_set:bool=False):
    async def sendPhoto(photo_url):
        log_command(ctx.user.id, 'photo_search')
        # Make a HEAD request to check if the photo exists
        URLresponse = requests.head(photo_url)
        print(URLresponse.status_code)
        if URLresponse.status_code == 200:
            await channel.send(f'[Photo by {getPhotoCredits(f"{search_query}")}](<https://railway-photos.xm9g.net#:~:text={search_query}>) | [View in browser]({photo_url})')
        else:
            mAdded = search_query+'M'
            # try with m added
            photo_url = f"https://railway-photos.xm9g.net/photos/{mAdded}.webp"
            URLresponse = requests.head(photo_url)
            if URLresponse.status_code == 200:
                await channel.send(photo_url)
                for i in range(2,5):
                    photo_url = f"https://railway-photos.xm9g.net/photos/{mAdded}-{i}.webp"
                    print(f"searching for other images for {mAdded}")
                    print(f"url: {photo_url}")
                    URLresponse = requests.head(photo_url)
                    if URLresponse.status_code == 200:
                        await channel.send(f'[Photo by {getPhotoCredits(f"{search_query}-{i}")}](<https://railway-photos.xm9g.net#:~:text={search_query}>) | [View in browser]({photo_url})')
                    else:
                        print("no other images found")
                        await channel.send(f"Photo not in xm9g database!")
                        break
            else:
                await channel.send(f"Photo not in xm9g database!")
                
            
            
        for i in range(2,5):
            photo_url = f"https://railway-photos.xm9g.net/photos/{search_query}-{i}.webp"
            print(f"searching for other images for {search_query}")
            print(f"url: {photo_url}")
            URLresponse = requests.head(photo_url)
            if URLresponse.status_code == 200:
                await channel.send(f'[Photo by {getPhotoCredits(f"{search_query}-{i}")}](<https://railway-photos.xm9g.net#:~:text={search_query}>) | [View in browser]({photo_url})')
            else:
                print("no other images found")
                break
    
    # start of the thing
    channel = ctx.channel
    search_query = number.upper()
    photo_url = f"https://railway-photos.xm9g.net/photos/{search_query}.webp"
    await ctx.response.send_message(f"Searching for `{search_query}`...")
    
    #get full set
    try:
        fullSet = setNumber(number).split("-")
    except:
        print(f'cannot get full set for {number}')
        search_set=False
                
    await sendPhoto(photo_url)
    
    if search_set:
        print(f'Searching full set: {fullSet}')
        if fullSet[0] != number:
            search_query=fullSet[0].upper()
            await ctx.channel.send(f'Photos for `{fullSet[0]}`')
            await sendPhoto(f"https://railway-photos.xm9g.net/photos/{fullSet[0]}.webp")
        if fullSet[1] != number:
            search_query=fullSet[1].upper()
            await ctx.channel.send(f'Photos for `{fullSet[1]}`')
            await sendPhoto(f"https://railway-photos.xm9g.net/photos/{fullSet[1]}.webp")
        if fullSet[2] != number:
            search_query=fullSet[2].upper()
            await ctx.channel.send(f'Photos for `{fullSet[2]}`')
            await sendPhoto(f"https://railway-photos.xm9g.net/photos/{fullSet[2]}.webp")


 
# myki fare calculator   
@myki.command(name="calculate-fare", description="Calculate fare for a trip")   
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)       
@app_commands.describe(start_zone = "Start zone", end_zone = "End zone")
async def calculate_fair(ctx, start_zone:int, end_zone:int):
    async def calc():
        await ctx.response.defer()
        log_command(ctx.user.id, 'calculate-fare')
    
        start = start_zone
        end = end_zone
        if start > end:
            start = end_zone
            end = start_zone


        try:
            api_response = fareEstimate(start, end)
            json_response = json.dumps(api_response)
            data = json.loads(json_response)

            result = data['FareEstimateResult']
            
            earlyBird = result['IsEarlyBird']
            weekend = result['IsThisWeekendJourney']
            
            fairs = result['PassengerFares']
            
            embed=discord.Embed(title=f"Zone {start_zone} → {end_zone}", color=0xc2d840)
            count=0
            for fair in fairs:
                type = fairs[count]['PassengerType']
                Fare2HourPeak = fairs[count]['Fare2HourPeak']
                Fare2HourOffPeak = fairs[count]['Fare2HourOffPeak']
                FareDailyPeak = fairs[count]['FareDailyPeak']
                WeekendCap = fairs[count]['WeekendCap']
                HolidayCap = fairs[count]['HolidayCap']
                Pass7Days = fairs[count]['Pass7Days']
                Pass28To69DayPerDay = fairs[count]['Pass28To69DayPerDay']
                Pass70PlusDayPerDay = fairs[count]['Pass70PlusDayPerDay']
                count +=1

                embed.add_field(name=type.title(), value=f'2 hour fare: `${Fare2HourPeak:.2f}`\nDaily cap: `${FareDailyPeak:.2f}`\nWeekend cap: `${WeekendCap:.2f}`\nHoliday cap: `${HolidayCap:.2f}`', inline=True)
                
            embed.add_field(name='Fare Info', value=f'Early Bird: {earlyBird}\nWeekend: {weekend}', inline=False)
            await ctx.edit_original_response(embed=embed)          

        except Exception as e:
            await ctx.edit_original_response(content='Invalid information. Please try again.')
            print(e)
            
            

        
    asyncio.create_task(calc())

# thing to save myki credentials to bot:
@myki.command(name='save-login', description='Save your PTV account username and password to the bot, run it again to change your saved info')
@app_commands.describe(ptvusername = "PTV accpunt username", ptvpassword = "PTV account password", encryptionpassword = "A password to encrypt your PTV password")
async def login(ctx, ptvusername: str, ptvpassword: str, encryptionpassword: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'save-login')
    encryptedPassword = encryptPW(encryptionpassword, ptvpassword)
    savelogin(ptvusername, str(encryptedPassword).split("'")[1], ctx.user.id) # the split is so it dosnt include the b' part
    await ctx.edit_original_response(content=f'Saved username and password to bot.\nUsername: `{ptvusername}`\nPassword: `{ptvpassword}`\nYour password is encrypted and cannot be seen by anyone. You will need to enter your encryption password to view your mykis with the bot.\nEncryption password: `{encryptionpassword}`')
    

@myki.command(name='view', description='View your mykis and their balances')
@app_commands.describe(encriptionpassword = "Your encryption password from the login command")
async def viewmykis(ctx, encriptionpassword: str):
    loop = asyncio.get_event_loop()
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'view-myki')
    def viewcards():
        # decrypt the password
        
        # get saved username and password:
        try:
            login = readlogin(ctx.user.id)
        except:
            ctx.edit_original_response(content="You haven't logged in yet. Run </myki login:1289553446659166300> to login.")
            return

        try:
            decryptedPassword = decryptPW(encriptionpassword, login[1].encode())
        except Exception as e:
            ctx.edit_original_response(content="Your encryption password is incorrect. Run </myki login:1289553446659166300> to reset it.")
            return
        
        # run the myki scraper
        try:
            data = getMykiInfo(login[0], decryptedPassword)
        except Exception as e:
            ctx.edit_original_response(content=f"There has been an error: `{e}`")
            return
        
        # make embed
        embed = discord.Embed(title="Your Mykis", color=0xc2d840)
        for myki, info in data.items():
            # find mobile mykis:
            prefix = "mobile myki, "
            if info[0].startswith(prefix):
                cardName = f':mobile_phone: {info[0][len(prefix):]}'
            else:
                cardName = info[0]
            
            embed.add_field(name=f'{cardName}    {info[2]}', value=f'{info[1]}')
        
        return embed

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Run the viewcards function in a separate thread
        result = await loop.run_in_executor(executor, viewcards)

        # Edit the original response based on the result
        if isinstance(result, discord.Embed):
            await ctx.edit_original_response(embed=result)
        else:
            await ctx.edit_original_response(content=result)

# Wongm search
@bot.tree.command(name="wongm", description="Search Wongm's Rail Gallery")
@app_commands.describe(search="search")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def line_info(ctx, search: str):
    log_command(ctx.user.id, 'wongm-search')
    channel = ctx.channel
    print(f"removing spaces in search {search}")
    spaces_removed = search.replace(' ', '%20')
    print(spaces_removed)
    url = f"https://railgallery.wongm.com/page/search/?s={spaces_removed}"
    await ctx.response.send_message(url)



# Train search train
@search.command(name="train", description="Search for a specific Train")
async def train_search(ctx, train: str, show_run_info:bool=True):
    await ctx.response.defer()
    log_command(ctx.user.id, 'train-search')
    # await ctx.response.send_message(f"Searching, trip data may take longer to send...")
    channel = ctx.channel
    type = trainType(train)
    set = setNumber(train.upper())
    
    metroTrains = ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "X'Trapolis 2.0"]
    vlineTrains = ['VLocity', 'Sprinter', 'N Class']
   
    print(f'set: {set}')
    print(f"TRAINTYPE {type}")
    
    # get colour for the embed
    if type in metroTrains:
        colour = 0x008dd0
    elif type in vlineTrains:
        colour = 0x7f3f98
    else:
        colour = 0x444345
    
    if type is None:
       await ctx.edit_original_response(content="Train not found")
    else:
        embed = discord.Embed(title=f"{train.upper()}:", color=colour)
        # embed.add_field(name='\u200b', value=f'{setEmoji(type)}\u200b', inline=False) 
        try:
            if set.endswith('-'):
                embed.add_field(name=type, value=set[:-1])
            else:
                embed.add_field(name=type, value=f'{set}')
        except:
            await ctx.edit_original_response(content="Train not found")
            return
        
        if train.upper() == "7005":  # Only old livery sprinter
            embed.set_thumbnail(url="https://xm9g.net/discord-bot-assets/MPTB/Sprinter-VLine.png")
        else:
            embed.set_thumbnail(url=getIcon(type))
        
        if type in ["X'Trapolis 2.0", 'HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas','VLocity', 'Sprinter', 'N Class', 'Y Class', "T Class", "S Class (Diesel)"]:
            information = trainData(set)
            print(information)
            infoData=''
            if information[5]:
                infoData+=f'\n- **Name:** {information[5]}\n'
                
            if information[2]:
                infoData+=f'- **Entered Service:** {information[2]}\n'
                
            if information[3]:
                infoData+=f'- **Status:** {information[3]}\n'
            
            if information[4]:
                infoData+=f'- **Notes:** {information[4]}\n'
            if information[7]:
                infoData+=f'- **Interior:** {information[7]}\n'
            
            if information[9]:
                infoData+=f'- **Operator:** {information[9]}\n'
            
            if information[8]:
                infoData+=f'- **Gauge:** {information[8]}\n'
            
            if information[1]:
                embed.add_field(name='Livery', value=f'{information[1]}', inline=False)
                
                
            # thing if the user has been on
            def checkTrainRidden(variable, file_path):
                if not os.path.exists(file_path):
                    print(f"The file {file_path} does not exist.")
                    return False

                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[1] == variable:
                            return True
                return False 
        
            fPath = f'utils/trainlogger/userdata/{ctx.user.name}.csv'
            trainridden = checkTrainRidden(set, fPath)
            if trainridden:
                infoData +='\n\n✅ You have been on this train before'
                
            embed.add_field(name='Information', value=infoData)
        else:
            embed.add_field(name='Information', value='None available')
        
        image = getImage(train.upper())
        if image != None:
            embed.set_image(url=image)            
            embed.add_field(name="Source:", value=f'[{getPhotoCredits(train.upper())} (Photo)](https://railway-photos.xm9g.net#:~:text={train.upper()}), [MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html), Vicsig & Wikipedia (Other info)', inline=False)
        else:
            embed.add_field(name="Source:", value='[MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html), Vicsig & Wikipedia (Other info)', inline=False)
        """
        if type in metroTrains:
            embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
            """
        embed_update = await ctx.edit_original_response(embed=embed)
        
        if type in metroTrains and show_run_info:
            # map thing
            mapEmbed = discord.Embed(title=f"Trip Information for {train.upper()}:", color=0x0070c0)
            mapEmbed.add_field(name='<a:botloading2:1261102206468362381> Loading Trip Data', value='⠀')
            mapEmbedUpdate = await ctx.channel.send(file=None, embed=mapEmbed)
        
        async def addmap():

                # Generate the map asynchronously
                # After map generation, send it
                if type == "HCMT": # because ptv api lists hcmts like "9005M-9905M" for some fucking reason
                    hcmtcar1 = set.split('-')
                    location = getTrainLocation(hcmtcar1[0]+'M')
                else:
                    location = getTrainLocation(set)
                line = ""
                print(f"Location: {location}")
                url = convertTrainLocationToGoogle(location)
                stoppingPattern = getStoppingPatternFromCar(location)
                print(f"STOPPING PATTERN: {stoppingPattern}")
                try:
                    if location is not None:
                        for item in location:
                            latitude = item['vehicle_position']['latitude']
                            longitude = item['vehicle_position']['longitude']
                            line = get_route_name(item['route_id'])
                            geopath=''
                            # geopath = getGeopath(item["run_ref"])
                            # print(f'geopath: {geopath}')

                        await makeMapv2(latitude,longitude, train, geopath) 
                except Exception as e:
                    await mapEmbedUpdate.delete()
                    await ctx.channel.send('No trip data available.')
                    print(f'ErROR: {e}')
                    return
                file_path = f"temp/{train}-map.png"
                if os.path.exists(file_path):
                    # Delete the old message
                    await mapEmbedUpdate.delete()
                    
                    file = discord.File(file_path, filename=f"{train}-map.png")
                    
                    embed = discord.Embed(title=f"{train}'s current trip", url=url, colour=lines_dictionary[line][1], timestamp=discord.utils.utcnow())
                    embed.remove_field(0)

                    # Add the stops to the embed.
                    stopsString = ''
                    fieldCounter = 0
                    currentFieldLength = 0

                    first_stop = True

                    for stop_name, stop_time, status, schedule in stoppingPattern:
                        if status == 'Skipped':
                            # For skipped stops
                            stopEntry = f'{getMapEmoji(line, "skipped")} ~~{stop_name}~~'
                        else:
                            # Calculate delay in minutes
                            delay = (convert_times(stop_time) - convert_times(schedule)) // 60  # Convert seconds to minutes
                            delay_str = f"+{delay}m" if delay > 0 else ""

                            if first_stop:
                                if stop_name in interchange_stations:
                                    emoji_type = "interchange_first"
                                else:
                                    emoji_type = "terminus"
                                stopEntry = f'{getMapEmoji(line, emoji_type)} {stop_name} - {convert_iso_to_unix_time(stop_time)} {delay_str}'
                                first_stop = False
                            else:
                                # Check if it's the last stop in the list
                                if stop_name == stoppingPattern[-1][0]:  # Check if current stop name is the last one
                                    if stop_name in interchange_stations:
                                        emoji_type = "interchange_last"
                                    else:
                                        emoji_type = "terminus2"
                                else:
                                    # Check stop_name in interchange_stations
                                    if stop_name in interchange_stations:
                                        emoji_type = "interchange"
                                    else:
                                        emoji_type = "stop"
                                stopEntry = f'{getMapEmoji(line, emoji_type)} {stop_name} - {convert_iso_to_unix_time(stop_time)} {delay_str}'

                        
                        # Add newline for formatting
                        stopEntry += '\n'

                        if currentFieldLength + len(stopEntry) > 1000:
                            # Add the current field and start a new one
                            if fieldCounter == 0:  # First field
                                stopsString += f'{getMapEmoji(line, "cont1")}\n'
                            else:
                                stopsString = f'{getMapEmoji(line, "cont2")}\n{stopsString}{getMapEmoji(line, "cont1")}\n'
                            embed.add_field(name=f"⠀", value=stopsString, inline=False)
                            stopsString = stopEntry
                            fieldCounter += 1
                            currentFieldLength = len(stopEntry)
                        else:
                            stopsString += stopEntry
                            currentFieldLength += len(stopEntry)

                    # Add the last field if there's any content left
                    if stopsString:
                        if fieldCounter > 0:  # Not the first field
                            stopsString = f'{getMapEmoji(line, "cont2")}\n{stopsString}'
                        embed.add_field(name=f"⠀", value=stopsString, inline=False)
                    
                    embed.set_image(url=f'attachment://{train}-map.png')
                    embed.set_footer(text='Maps © Thunderforest, Data © OpenStreetMap contributors')
                
                    # Send a new message with the file and embed
                    await channel.send(file=file, embed=embed)
                else:
                    await mapEmbedUpdate.delete()
                    await ctx.channel.send(f"Error: Map file '{file_path}' not found.")
                    print(f"Error: Map file '{file_path}' not found.")
                    
        # Run transportVicSearch in a separate thread
        
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas']:
            asyncio.create_task(addmap())
            # loop = asyncio.get_event_loop()
            # task = loop.create_task(transportVicSearch_async(ctx, train.upper(), embed, embed_update))
            # await task
            
# search run id   
@search.command(name="td-number", description="Shows the run for a specific TDN, found in the departures command")
@app_commands.describe(td="TD Number", mode="Mode of transport to search TDN for")
@app_commands.choices(mode=[
        app_commands.Choice(name="Metro", value="metro"),
        # app_commands.Choice(name="V/Line", value="vline"),
        # app_commands.Choice(name="Tram", value="tram"),
        # app_commands.Choice(name="Bus", value="bus"),
        # app_commands.Choice(name="Night Bus", value="nightbus"),
        
])
async def runidsearch(ctx, td:str, mode:str="metro"):
    await ctx.response.defer()
    log_command(ctx.user.id, 'runid-search')
    async def addmap():
        runid = TDNtoRunID(td)
        try:
            runData = getTrainLocationFromID(str(runid))
            line = ""
            if mode == "metro":
                stoppingPattern = getStoppingPatternFromRunRef(runData, 0)
                print('Mode is metro')
            elif mode == "tram":
                stoppingPattern = getStoppingPatternFromRunRef(runData, 1)
                print('Mode is tram')
            elif mode == "bus":
                stoppingPattern = getStoppingPatternFromRunRef(runData, 2)
                print('Mode is bus')
            elif mode == "vline":
                stoppingPattern = getStoppingPatternFromRunRef(runData, 3)
                print('Mode is vline')
                def strip_station_name(name):
                    return name.replace('Railway Station', '').strip()
                    
            elif mode == "nightbus":
                stoppingPattern = getStoppingPatternFromRunRef(runData, 4)
                print('Mode is nightbus')

                # Filter out entries where the station name has a slash and status is 'Skipped', then strip 'Railway Station'
                stoppingPattern = [
                    (strip_station_name(station[0]), station[1], station[2]) 
                    for station in stoppingPattern 
                    if not ('/' in station[0] and station[1] == 'Skipped')
]
            print(f"STOPPING PATTERN: {stoppingPattern}")
            try:
                if mode == "metro":
                    if runData is not None:
                        for item in runData:
                            # latitude = item['vehicle_position']['latitude']
                            # longitude = item['vehicle_position']['longitude']
                            line = get_route_name(item['route_id'])
                            print(f'Line: {line}')
                elif mode == "vline":
                    line = 'V/Line'
                    print(f'Line: {line}')
                else: # just make the mode the type name
                    line = mode
                    print(f'Line: {line}')

            except Exception as e:
                await ctx.edit_original_response(content='No trip data available.')
                print(f'ErROR: {e}')
                return
            
            # embed colour
            if mode == "metro":
                colour = lines_dictionary[line][1]
            elif mode == "vline":
                colour = 0x7f3f98
            elif mode == "tram":
                colour = 0x71bd46
            elif mode == "bus" or mode == 'nightbus':
                colour = 0xf78b24
            
            embed = discord.Embed(title=f"TD {runid}", colour=colour, timestamp=discord.utils.utcnow())

            # add the stops to the embed.
            stopsString = ''
            fieldCounter = 1
            currentFieldLength = 0

            first_stop = True
            fieldCounter = 0
            stopsString = ""
            currentFieldLength = 0

            # from here to the other comment should be the same as the train search command
            for stop_name, stop_time, status, schedule in stoppingPattern:
                if status == 'Skipped':
                    # For skipped stops
                    stopEntry = f'{getMapEmoji(line, "skipped")} ~~{stop_name}~~'
                else:
                    # Calculate delay in minutes
                    delay = (convert_times(stop_time) - convert_times(schedule)) // 60  # Convert seconds to minutes
                    delay_str = f"+{delay}m" if delay > 0 else ""

                    if first_stop:
                        if stop_name in interchange_stations:
                            emoji_type = "interchange_first"
                        else:
                            emoji_type = "terminus"
                        stopEntry = f'{getMapEmoji(line, emoji_type)} {stop_name} - {convert_iso_to_unix_time(stop_time)} {delay_str}'
                        first_stop = False
                    else:
                        # Check if it's the last stop in the list
                        if stop_name == stoppingPattern[-1][0]:  # Check if current stop name is the last one
                            if stop_name in interchange_stations:
                                emoji_type = "interchange_last"
                            else:
                                emoji_type = "terminus2"
                        else:
                            # Check stop_name in interchange_stations
                            if stop_name in interchange_stations:
                                emoji_type = "interchange"
                            else:
                                emoji_type = "stop"
                        stopEntry = f'{getMapEmoji(line, emoji_type)} {stop_name} - {convert_iso_to_unix_time(stop_time)} {delay_str}'
                # until here should be the same as train search
                
                # Add newline for formatting
                stopEntry += '\n'

                if currentFieldLength + len(stopEntry) > 1000:
                    # Add the current field and start a new one
                    if fieldCounter == 0:  # First field
                        stopsString += f'{getMapEmoji(line, "cont1")}\n'
                    else:
                        stopsString = f'{getMapEmoji(line, "cont2")}\n{stopsString}{getMapEmoji(line, "cont1")}\n'
                    embed.add_field(name=f"⠀", value=stopsString, inline=True)
                    stopsString = stopEntry
                    fieldCounter += 1
                    currentFieldLength = len(stopEntry)
                else:
                    stopsString += stopEntry
                    currentFieldLength += len(stopEntry)

            # Add the last field if there's any content left
            if stopsString:
                if fieldCounter > 0:  # Not the first field
                    stopsString = f'{getMapEmoji(line, "cont2")}\n{stopsString}'
                embed.add_field(name=f"⠀", value=stopsString, inline=True)
                    
            await ctx.edit_original_response(embed=embed)

        except Exception as e:
            await ctx.edit_original_response(content='No trip data available.')   
            print(f'ErROR: {e}') 
            print(traceback.format_exc())  
    # Run transportVicSearch in a separate thread
        
        
    asyncio.create_task(addmap())
            # loop = asyncio.get_event_loop()
            # task = loop.create_task(transportVicSearch_async(ctx, train.upper(), embed, embed_update))
            # await task
            
@search.command(name="tram", description="Search for a specific Tram")
@app_commands.describe(tram="tram")
async def tramsearch(ctx, tram: str):
    await ctx.response.send_message(f"Searching, trip data may take longer to send...")
    log_command(ctx.user.id, 'tram-search')
    channel = ctx.channel
    type = tramType(tram)
    set = tram.upper()
   
    print(f'Set: {set}')
    print(f"Tram Type: {type}")
    if type is None:
        await channel.send("Tram not found")
    else:
        embed = discord.Embed(title=f"Info for {tram.upper()}:", color=0x0070c0)
        if set.endswith('-'):
            embed.add_field(name=type, value=set[:-1])
        else:
            embed.add_field(name=type, value=set)
        
        embed.set_thumbnail(url=getIcon(type))
        
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas','VLocity', 'Sprinter', 'N Class']:
            information = trainData(set)
            print(information)
            infoData = f'**Livery:** {information[1]}\n**Status:** {information[3]}\n**Entered Service:** {information[2]}\n**Vicsig notes:** {information[4]}'
            if information[5]:
                infoData+=f'\n**Name:** {information[5]}'
                
            # thing if the user has been on
            def check_variable_in_csv(variable, file_path):
                if not os.path.exists(file_path):
                    print(f"The file {file_path} does not exist.")
                    return False

                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[1] == variable:
                            return True
                return False 
        
            fPath = f'utils/trainlogger/userdata/tram/{ctx.user.name}.csv'
            trainridden = check_variable_in_csv(set, fPath)
            if trainridden:
                infoData +='\n\n✅ You have been on this tram before'
                
            embed.add_field(name='Information', value=infoData)
        else:
            embed.add_field(name='Information', value='None available')
            
        
        embed.set_image(url=getTramImage(tram.upper()))
        
        embed.add_field(name="Source:", value=f'[{getPhotoCredits(tram.upper())} (Photo)](https://railway-photos.xm9g.net#:~:text={tram.upper()}), [MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html), [Vicsig (Other info)](https://vicsig.net)', inline=False)
        
        # embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
        embed_update = await channel.send(embed=embed)
        
        # map thing
        '''mapEmbed = discord.Embed(title=f"{tram}'s location")
        mapEmbed.add_field(name='<a:botloading2:1261102206468362381> Loading Map', value='⠀')
        mapEmbedUpdate = await ctx.channel.send(file=None, embed=mapEmbed)
        
        # Generate the map location
        async def addmap():                
                
                location = getTramLocation(set)
                url = convertTrainLocationToGoogle(location)
                try:
                    if location is not None:
                        for item in location:
                            latitude = item['vehicle_position']['latitude']
                            longitude = item['vehicle_position']['longitude']
                            geopath=''
                            # geopath = getGeopath(item["run_ref"])
                            # print(f'geopath: {geopath}')

                        await makeMapv2(latitude,longitude, tram, geopath)  # Adjust this line to asynchronously generate the map
                except Exception as e:
                    await mapEmbedUpdate.delete()
                    await ctx.channel.send('No location data available.')
                    print(f'ErROR: {e}')
                    return
                file_path = f"temp/{tram}-map.png"
                if os.path.exists(file_path):
                    # Delete the old message
                    await mapEmbedUpdate.delete()
                    
                    file = discord.File(file_path, filename=f"{tram}-map.png")
                    
                    embed = discord.Embed(title=f"{tram}'s location", url=url)
                    embed.remove_field(0)
                    embed.set_image(url=f'attachment://{tram}-map.png')
                    embed.set_footer(text='Mapdata © OpenStreetMap contributors')
                
                    # Send a new message with the file and embed
                    await channel.send(file=file, embed=embed)
                else:
                    await mapEmbedUpdate.delete()
                    await ctx.channel.send(f"Error: Map file '{file_path}' not found.")
                    print(f"Error: Map file '{file_path}' not found.")
        '''

            
        # else:
        #     embed.remove_field(3)
        #     await embed_update.edit(embed=embed)
        #     await mapEmbedUpdate.delete()
        #     await ctx.channel.send('Location info is only available for Metro services')
        
        
            

    

        

    
# @app_commands.command(name='test', description="Test command")
# @app_commands.allowed_installs(guilds=False, users=True)
# @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# async def useable_only_users(interaction: discord.Interaction):
#     await interaction.response.send_message("I am only installed to users, but can be used anywhere.")
    

# Next departures for a station
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
@bot.tree.command(name="departures", description="Upcoming trains departing a station")
@app_commands.describe(station="Station")
@app_commands.autocomplete(station=station_autocompletion)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.choices(
    line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Frankston", value="Frankston"),
        app_commands.Choice(name="Glen Waverley", value="Glen Waverley"),
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Lilydale", value="Lilydale"),
        app_commands.Choice(name="Mernda", value="Mernda"),
        app_commands.Choice(name="Pakenham", value="Pakenham"),
        app_commands.Choice(name="Sandringham", value="Sandringham"),
        app_commands.Choice(name="Stony Point", value="Stony Point"),
        app_commands.Choice(name="Sunbury", value="Sunbury"),
        app_commands.Choice(name="Upfield", value="Upfield"),
        app_commands.Choice(name="Werribee", value="Werribee"),
    ]
)
# test
async def departures(ctx, station: str, line:str='all'):
    async def nextdeps():
        channel = ctx.channel
        await ctx.response.defer()
        log_command(ctx.user.id, 'departures-search')
        Nstation = station.replace(' ', '%20')
        search = search_api_request(f'{Nstation.title()}%20Station')
        # find the stop id!
        def find_stop_id(data, location):
            for stop in data['stops']:
                if stop['stop_name'] == location:
                    return stop['stop_id']
            return 'None'
        
        try:
            stop_id = find_stop_id(search, f"{station.title()} Station")
        except:
            await ctx.edit_original_response(content=f"Cannot find departures for {station.title()} Station")
        print(f'STOP ID for {station} Station: {stop_id}')
        if stop_id == 'None':
            # await ctx.channel.send("Station not found, trying for V/LINE")
            search = search_api_request(f'{Nstation.title()}%20Railway%20Station')
            stop_id = find_stop_id(search, f"{station.title()} Railway Station ")
            print(f'STOP ID for {station} Station: {stop_id}')

            
        # get departures for the stop:
        depsData = departures_api_request(stop_id, 0)
        vlineDepsData = departures_api_request(stop_id, 3)
        try:
            departures = depsData['departures']
            runs = depsData['runs']
            # V/Line
            Vdepartures = vlineDepsData['departures']
            Vruns = vlineDepsData['runs']
        except:
            await ctx.edit_original_response(content=f"Cannot find departures for {station.title()} Station")
            return
         
        
        # make embed with data
        if line == "all":
            embed= discord.Embed(title=f"Next Metro trains departing {station.title()} Station", timestamp=discord.utils.utcnow())
        else:
            embed= discord.Embed(title=f"Next Metro trains departing {station.title()} Station on the {line} line", timestamp=discord.utils.utcnow())

        fields = 0
        
        departures = [departure for departure in departures if get_route_name(departure['route_id']) == line or line == "all"]

        
        for departure in departures:
            route_id= departure['route_id'] 
            scheduled_departure_utc = departure['scheduled_departure_utc']
            if isPast(scheduled_departure_utc):
                # print(f"time in past")
                pass
            else:
                estimated_departure_utc = departure['estimated_departure_utc']
                run_ref = departure['run_ref']
                at_platform = departure['at_platform']
                platform_number = departure['platform_number']
                note = departure['departure_note']
                
                # get info for the run:
                desto = runs[run_ref]['destination_name']
                try:
                    trainType = runs[run_ref]['vehicle_descriptor']['description']
                    trainNumber = runs[run_ref]['vehicle_descriptor']['id']
                except:
                    trainType = ''
                    trainNumber = ''

                # train emoji
                trainType = getEmojiForDeparture(trainType)
                
                # Convert PTV run REF to TDN
                TDN = RunIDtoTDN(run_ref)

                #convert to timestamp
                depTime=convert_iso_to_unix_time(scheduled_departure_utc)
                #get route name:
                route_name = get_route_name(route_id)                
                
                #VLINE PLATFORMS DONT WORK PLS HELP
                
                # thing for stony point
                if route_name == "Stony Point":
                    trainType = "Sprinter"
                    if station.title() == "Frankston":
                        platform_number = "3"
                    else:
                        platform_number = "1"
                
                embed.add_field(name=f"{getlineEmoji(route_name)}\n{desto} {note if note else ''}", value=f"\nScheduled to depart {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nPlatform {platform_number}\n{trainType} {trainNumber}\nTDN: `{TDN}`")
                fields = fields + 1
                if fields == 9:
                    break
        # the V/Line part
        '''fields = 0
        
        Vdepartures = [Vdeparture for Vdeparture in Vdepartures if get_route_name(Vdeparture['route_id']) == line or line == "all"]

        
        for Vdeparture in Vdepartures:
            route_id= Vdeparture['route_id'] 
            scheduled_departure_utc = Vdeparture['scheduled_departure_utc']
            if isPast(scheduled_departure_utc):
                print(f"time in past")
                # pass
            else:
                estimated_departure_utc = Vdeparture['estimated_departure_utc']
                run_ref = Vdeparture['run_ref']
                at_platform = Vdeparture['at_platform']
                platform_number = Vdeparture['platform_number']
                note = Vdeparture['departure_note']
                
                #convert to timestamp
                depTime=convert_iso_to_unix_time(scheduled_departure_utc)
                #get route name:
                route_name = get_route_name(route_id)                
                
                #VLINE PLATFORMS DONT WORK PLS HELP
                
                embed.add_field(name=f"{getlineEmoji(route_name)}\ndesto here {note if note else ''}", value=f"\nScheduled to depart {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nPlatform {platform_number}\nRun ID: `{run_ref}`")
                fields = fields + 1
                if fields == 9:
                    break
                                        
        if fields == 0:
            embed.add_field(name="No upcoming departures", value="⠀")'''
            
        # disruptions:
        disruptions = getStationDisruptions(stop_id)
        for disruption in disruptions:
            embed.insert_field_at(index=0, name=f"<:Disruption:1322444175941173280> {disruption['title']}", 
                                value=f"[{disruption['description']}]({disruption['url']})\n", inline=False)
        
        embed.set_footer(text="V/Line departures are unavailable")
        embed.set_thumbnail(url=getStationImage(station))
        await ctx.edit_original_response(embed=embed)          

    asyncio.create_task(nextdeps())



# Montague Bridge search
'''@bot.tree.command(name="days-since-montague-hit", description="See how many days it has been since the Montague Street bridge has been hit.")
async def train_line(ctx):
    await ctx.response.send_message(f"Checking...")
    channel = ctx.channel
    
    embed = discord.Embed(title=f"How many days since the Montague Street bridge has been hit?", color=0xd8d800)
    # embed.set_image(url=getImage(train.upper()))
    
    # Create a new thread to call the function
    # days_queue = queue.Queue()
    # thread = threading.Thread(target=montagueDays, args=(days_queue,))
    # thread.start()

    # thread.join()
    # Retrieve the result from the queue
    # days = days_queue.get()
    
    api_queue = queue.Queue()
    thread = threading.Thread(target=montagueAPI, args=(api_queue,))    
    thread.start()
    thread.join()
    
    apiData = api_queue.get()
    
    # Extract individual variables from the apis data
    date = apiData["date"]
    thanks = apiData["thanks"]
    streak = apiData["streak"]
    chumps = apiData["chumps"]
    name = chumps[0]['name'] # get name from the chumps thing
    image = apiData["image"]
    thumb = apiData["thumb"]
    date_year = apiData["date_year"]
    date_week = apiData["date_week"]
    date_aus_string = apiData["date_aus_string"]
    
    embed.add_field(name=f"{convert_to_unix_time(f'{date}T00:00:00Z')} days", value='\u200b', inline=False)

    embed.add_field(name="Current Champion:", value=name)
    embed.add_field(name="Date:", value=date)
    embed.set_image(url=f'https://howmanydayssincemontaguestreetbridgehasbeenhit.com{image}')
    
    embed.set_author(name='howmanydayssincemontaguestreetbridgehasbeenhit.com', url="https://howmanydayssincemontaguestreetbridgehasbeenhit.com")
    await ctx.channel.send(embed=embed)'''
    
@games.command(name="station-guesser", description="Play a game where you guess what train station is in the photo.")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1, max 100.", ultrahard = "Ultra hard mode.")
async def game(ctx,rounds: int = 1, ultrahard: bool=False):
    
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-guesser')
    async def run_game(): 

        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 100:
            await ctx.response.send_message("You can only play a maximum of 100 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True
        
        # Define the CSV file path
        if ultrahard:
            csv_file = 'utils/game/images/ultrahard.csv'
        else:
            csv_file = 'utils/game/images/guesser.csv'

        # Read the CSV file and store rows in a list
        rows = []
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row)

        # Remove the header row if present
        header = rows[0]
        data = rows[1:]

        ignoredRounds = 0
        
        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []
        
        for round in range(rounds):
            roundResponse = False
            # Get a random row
            random_row = random.choice(data)

            # Extract data from the random row
            url = random_row[0]
            station = random_row[1]
            difficulty = random_row[2]
            credit = random_row[3]

            if ultrahard:
                embed = discord.Embed(title=f"Guess the station!", color=0xe52727, description=f"Type ! before your answer. You have 30 seconds to answer.\n\n**Difficulty:** `{difficulty.upper()}`")
            else:
                embed = discord.Embed(title=f"Guess the station!", description=f"Type ! before your answer. You have 30 seconds!\n\n**Difficulty:** `{difficulty}`")
                if difficulty == 'Very Easy':
                    embed.color = 0x89ff65
                elif difficulty == 'Easy':
                    embed.color = 0xcaff65
                elif difficulty == 'Medium':
                    embed.color = 0xffe665
                elif difficulty == 'Hard':
                    embed.color = 0xffa665
                elif difficulty == 'Very Hard':
                    embed.color = 0xff6565
            
            embed.set_image(url=url)
            embed.set_footer(text=f"Photo by {credit}. DM @xm9g to submit a photo")
            embed.set_author(name=f"Round {round+1}/{rounds}")

            # Send the embed message
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            def check(m):
                return m.channel == channel and m.author != bot.user and m.content.startswith('!')

            try:
                correct = False
                if ultrahard:
                    gameType = 'ultrahard'
                else:
                    gameType = 'guesser'
                
                
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    
                    # Check if the user's response matches the correct station
                    if user_response.content[1:].lower().replace(" ", "") == station.lower().replace(" ", ""):
                        log_command(user_response.author.id, 'game-station-guesser-correct')
                        if ultrahard:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it right!")
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it right! {station.title()} was the correct answer!")
                        correct = True
                        roundResponse = True
                        correctAnswers += 1
                        ignoredRounds = 0
                        print(f'Ignored rounds: {ignoredRounds}')
                        if ultrahard:
                            addLb(user_response.author.id, user_response.author.name, 'ultrahard')
                        else:
                            addLb(user_response.author.id, user_response.author.name, 'guesser')
                        if user_response.author.mention not in participants:
                            participants.append(user_response.author.mention)
                            
                    elif user_response.content.lower() == '!skip':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Round {round+1} skipped.")
                            log_command(user_response.author.id, 'game-station-guesser-skip')
                            skippedGames += 1
                            roundResponse = True
                            break
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                            roundResponse = True
                    elif user_response.content.lower() == '!stop':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Game ended.")
                            log_command(user_response.author.id, 'game-station-guesser-stop')
                            embed = discord.Embed(title="Game Summary")
                            embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                            embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                            embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                            embed.add_field(name="Participants", value=', '.join(participants))
                            await ctx.channel.send(embed=embed)   
                            return
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")    
                    else:
                        await ctx.channel.send(f"Wrong guess {user_response.author.mention}! Try again.")
                        log_command(user_response.author.id, 'game-station-guesser-incorrect')
                        roundResponse = True
                        incorrectAnswers += 1
                        if ultrahard:
                            addLoss(user_response.author.id, user_response.author.name, 'ultrahard')
                        else:
                            addLoss(user_response.author.id, user_response.author.name, 'guesser')
                        if user_response.author.mention not in participants:
                            participants.append(user_response.author.mention)
                        
            except asyncio.TimeoutError:
                if ultrahard:
                    await ctx.channel.send(f"Times up. Answers are not revealed in ultrahard mode.")
                else:
                    await ctx.channel.send(f"Times up. The answer was ||{station.title()}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                print(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds == 2 and roundResponse == False:
                    await ctx.channel.send("No responses for 2 rounds. Game ended.")
                    break
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title="Game Summary")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join(participants))
        await ctx.channel.send(embed=embed)      

    # Run the game in a separate task
    asyncio.create_task(run_game())
    

    
@stats.command(name="leaderboard", description="Global leaderboards for the games.",)
@app_commands.describe(game="What game's leaderboard to show?")
@app_commands.choices(game=[
        app_commands.Choice(name="Station Guesser", value="guesser"),
        app_commands.Choice(name="Ultrahard Station Guesser", value="ultrahard"),
        app_commands.Choice(name="Station order game", value="domino"),

])

async def lb(ctx, game: str='guesser'):
    log_command(ctx.user.id, 'view-leaderboard')
    channel = ctx.channel
    leaders = top5(game)
    if leaders == 'no stats':
        await ctx.response.send_message('There is no data for this game yet!',ephemeral=True)
        return
    print(leaders)
    # Create the embed
    embed = discord.Embed(title=f"Top 7 players for {game}", color=discord.Color.gold())
    
    count = 1
    for item, number, losses in leaders:
        try:
            embed.add_field(name=f'{count}: {item}', value=f'Wins: {str(number)}\nLosses: {str(losses)}\nAccuracy: {str(round((number/(number+losses))*100, 1))}%', inline=False)
        except:
            embed.add_field(name=f'{count}: {item}', value=f'Wins: {str(number)}\nLosses: {str(losses)}', inline=False)
        count = count + 1
        
    await ctx.response.send_message(embed=embed)


# Station order game made by @domino

lines_dictionary = {
    'Alamein': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'Riversdale', 'Willison', 'Hartwell', 'Burwood', 'Ashburton', 'Alamein'],0x01518a],
    'Belgrave': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'East Camberwell', 'Canterbury', 'Chatham', 'Union', 'Box Hill', 'Laburnum', 'Blackburn', 'Nunawading', 'Mitcham', 'Heatherdale', 'Ringwood', 'Heathmont', 'Bayswater', 'Boronia', 'Ferntree Gully', 'Upper Ferntree Gully', 'Upwey', 'Tecoma', 'Belgrave'],0x01518a],
    'Craigieburn': [['North Melbourne', 'Kensington', 'Newmarket', 'Ascot Vale', 'Moonee Ponds', 'Essendon', 'Glenbervie', 'Strathmore', 'Pascoe Vale', 'Oak Park', 'Glenroy', 'Jacana', 'Broadmeadows', 'Coolaroo', 'Roxburgh Park', 'Craigieburn'],0xfcb818],
    'Cranbourne': [['Richmond', 'South Yarra', 'Malvern', 'Caulfield', 'Carnegie', 'Murrumbeena', 'Hughesdale', 'Oakleigh', 'Huntingdale', 'Clayton', 'Westall', 'Springvale', 'Sandown Park', 'Noble Park', 'Yarraman', 'Dandenong', 'Lynbrook', 'Merinda Park', 'Cranbourne'],0x00a8e4],
    'Flemington Racecourse': [['Flemington Racecourse', 'Showgrounds', 'North Melbourne', 'Southern Cross', 'Flinders Street'],0x8a8c8f],
    'Frankston': [['Flinders Street', 'Richmond', 'South Yarra', 'Hawksburn', 'Toorak', 'Armadale', 'Malvern', 'Caulfield', 'Glen Huntly', 'Ormond', 'McKinnon', 'Bentleigh', 'Patterson', 'Moorabbin', 'Highett', 'Southland', 'Cheltenham', 'Mentone', 'Parkdale', 'Mordialloc', 'Aspendale', 'Edithvale', 'Chelsea', 'Bonbeach', 'Carrum', 'Seaford', 'Kananook', 'Frankston'],0x009645],
    'Glen Waverley': [['Richmond', 'East Richmond', 'Burnley', 'Heyington', 'Kooyong', 'Tooronga', 'Gardiner', 'Glen Iris', 'Darling', 'East Malvern', 'Holmesglen', 'Jordanville', 'Mount Waverley', 'Syndal', 'Glen Waverley'],0x01518a],
    'Hurstbridge': [['Jolimont', 'West Richmond', 'North Richmond', 'Collingwood', 'Victoria Park', 'Clifton Hill', 'Westgarth', 'Dennis', 'Fairfield', 'Alphington', 'Darebin', 'Ivanhoe', 'Eaglemont', 'Heidelberg', 'Rosanna', 'Macleod', 'Watsonia', 'Greensborough', 'Montmorency', 'Eltham', 'Diamond Creek', 'Wattle Glen', 'Hurstbridge'],0xd0202e],
    'Lilydale': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'East Camberwell', 'Canterbury', 'Chatham', 'Union', 'Box Hill', 'Laburnum', 'Blackburn', 'Nunawading', 'Mitcham', 'Heatherdale', 'Ringwood', 'Ringwood East', 'Croydon', 'Mooroolbark', 'Lilydale'],0x01518a],
    'Mernda': [['Jolimont', 'West Richmond', 'North Richmond', 'Collingwood', 'Victoria Park', 'Clifton Hill', 'Rushall', 'Merri', 'Northcote', 'Croxton', 'Thornbury', 'Bell', 'Preston', 'Regent', 'Reservoir', 'Ruthven', 'Keon Park', 'Thomastown', 'Lalor', 'Epping', 'South Morang', 'Middle Gorge', 'Hawkstowe', 'Mernda'],0xd0202e],
    'Pakenham': [['Richmond', 'South Yarra', 'Malvern', 'Caulfield', 'Carnegie', 'Murrumbeena', 'Hughesdale', 'Oakleigh', 'Huntingdale', 'Clayton', 'Westall', 'Springvale', 'Sandown Park', 'Noble Park', 'Yarraman', 'Dandenong', 'Hallam', 'Narre Warren', 'Berwick', 'Beaconsfield', 'Officer', 'Cardinia Road', 'Pakenham'],0x00a8e4],
    'Sandringham': [['Flinders Street', 'Richmond', 'South Yarra', 'Prahran', 'Windsor', 'Balaclava', 'Ripponlea', 'Elsternwick', 'Gardenvale', 'North Brighton', 'Middle Brighton', 'Brighton Beach', 'Hampton', 'Sandringham'],0xf17fb1],
    'Stony Point': [['Stony Point', 'Crib Point', 'Morradoo', 'Bittern', 'Hastings', 'Tyabb', 'Somerville', 'Baxter', 'Leawarra', 'Frankston'],0x009645],
    'Sunbury': [['North Melbourne', 'Footscray', 'Middle Footscray', 'West Footscray', 'Tottenham', 'Sunshine', 'Albion', 'Ginifer', 'St Albans', 'Keilor Plains', 'Watergardens', 'Diggers Rest', 'Sunbury'],0xfcb818],
    'Upfield': [['North Melbourne', 'Macaulay', 'Flemington Bridge', 'Royal Park', 'Jewell', 'Brunswick', 'Anstey', 'Moreland', 'Coburg', 'Batman', 'Merlynston', 'Fawkner', 'Gowrie', 'Upfield'],0xfcb818],
    'Werribee': [['Flinders Street', 'Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'Seaholme', 'Altona', 'Westona', 'Laverton', 'Aircraft', 'Williams Landing', 'Hoppers Crossing', 'Werribee'],0x009645],
    'Williamstown': [['Flinders Street', 'Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'North Williamstown', 'Williamstown Beach', 'Williamstown'],0x009645],
    'Unknown/Other':[[None], 0x000000],
}
linelist = [
    None,
    'Alamein', #1
    'Belgrave', #2
    'Craigieburn', #3
    'Cranbourne', #4
    'Mernda', #5
    'Frankston', #6
    'Glen Waverley', #7
    'Hurstbridge', #8
    'Lilydale', #9
    None,
    'Pakenham', #11
    'Sandringham', #12
    None,
    'Sunbury', #14
    'Upfield', #15
    'Werribee', #16
    'Williamstown' #17
]

@games.command(name="station-order", description="A game where you list the stations before or after a station.")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", direction = "The directions you are listing the stations in. Defaults to Up or Down.")
@app_commands.choices(
    direction=[
        app_commands.Choice(name="Up or Down", value='updown'),
        app_commands.Choice(name="Up", value='up'),
        app_commands.Choice(name="Down", value='down')
        ],
    )

async def testthing(ctx, direction: str = 'updown', rounds: int = 1):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-order')
    async def run_game():
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 25:
            await ctx.response.send_message("You can only play a maximum of 25 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        for round in range(rounds):
            # choose random number of stations
            numdirection = random.randint(2,5)

            # choose direction
            if direction == 'updown':
                direction1 = random.choice(['up','down'])
            else:
                direction1 = direction
            if direction1 == 'up':
                numdirection = numdirection*-1
            
            # choose random line
            line = None
            while line == None:
                line = linelist[random.randint(0,len(linelist)-1)]

            # choose random station
            if line == 'Flemington Racecourse':
                if numdirection == 5 or numdirection == -5:
                    numdirection = random.choice([-4,-3,-2,2,3,4])
            station = None
            while station == None:
                station = lines_dictionary[line][0][random.randint(0,len(lines_dictionary[line][0])-1)]
                if not 0 <= lines_dictionary[line][0].index(station)+numdirection <= len(lines_dictionary[line][0]):
                    station = None

            embed = discord.Embed(
                title=f"Which __**{numdirection if numdirection > 0 else numdirection*-1}**__ stations are __**{direction1}**__ from __**{station}**__ station on the __**{line} line**__?",
                description=f"**Answers must be in the correct order!** Answer using this format:\n!<station1>, <station2>{', <station3>' if numdirection >= 3 or numdirection <= -3 else ''}{', <station4>' if numdirection >= 4 or numdirection <= -4 else ''}{', <station5>' if numdirection >= 5 or numdirection <= -5 else ''}\n\n*Use !skip to skip to the next round.*",
                colour=lines_dictionary[line][1])
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            def check(m): return m.channel == channel and m.author != bot.user and m.content.startswith('!')

            # get list of correct stations
            if numdirection > 0:
                correct_list = lines_dictionary[line][0][lines_dictionary[line][0].index(station)+1:lines_dictionary[line][0].index(station)+numdirection+1]
            else:
                correct_list = lines_dictionary[line][0][lines_dictionary[line][0].index(station)+numdirection:lines_dictionary[line][0].index(station)]
                correct_list.reverse()
            correct_list1 = [x.lower() for x in correct_list]

            # the actual input part
            try:
                correct = False
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    response = user_response.content[1:].lower().split(',')
                    response = [x.strip() for x in response]


                    # Check if the user's response matches the correct station
                    if response == correct_list1:
                        await ctx.channel.send(f"{user_response.author.mention} guessed it correctly!")
                        addLb(user_response.author.id, user_response.author.name, 'domino')
                        
                        correct = True 
                    elif user_response.content.lower() == '!skip':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
                            break
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                    elif user_response.content.lower() == '!stop':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Game ended.")
                            return
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                    else:
                        await ctx.channel.send(f"Wrong guess {user_response.author.mention}! Try again.")
                        addLoss(user_response.author.id, user_response.author.name, 'domino')
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
            finally:
                # Reset game status down the game ends
                channel_game_status[channel] = False
            
    # Run the game in a separate task
    asyncio.create_task(run_game())

async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def line_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = lines_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
#log train logger
@trainlogs.command(name="train", description="Log a train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', traintype='Type of train (will be autofilled if a train number is entered)')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.choices(traintype=[
        app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
        app_commands.Choice(name="HCMT", value="HCMT"),
        app_commands.Choice(name="EDI Comeng", value="EDI Comeng"),
        app_commands.Choice(name="Alstom Comeng", value="Alstom Comeng"),
        app_commands.Choice(name="X'Trapolis 2.0", value="X'Trapolis 2.0"),
        app_commands.Choice(name="Siemens Nexas", value="Siemens Nexas"),
        app_commands.Choice(name="VLocity", value="VLocity"),
        app_commands.Choice(name="N Class", value="N Class"),
        app_commands.Choice(name="Sprinter", value="Sprinter"),
        app_commands.Choice(name="Other", value="Other"),
        app_commands.Choice(name="Tait", value="Tait"),
        app_commands.Choice(name="K Class", value="K Class"),
        app_commands.Choice(name="Y Class", value="Y Class"),
        app_commands.Choice(name="Other", value="Other"),
])

# Train logger
async def logtrain(ctx, line:str, number:str, start:str, end:str, date:str='today', traintype:str='auto', notes:str=None):
    channel = ctx.channel
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-train')
    print(date)
    async def log():
        print("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                return
            except TypeError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nUse the form `dd/mm/yyyy`')
                return

        # checking if train number is valid
        if number != 'Unknown':
            set = setNumber(number.upper())
            if set == None:
                await ctx.edit_original_response(content=f'Invalid train number: `{number.upper()}`')
                return
            type = trainType(number.upper())
        else:
            set = 'Unknown'
            type = 'Unknown'
            if traintype == 'auto':
                type = 'Unknown'
            else: type = traintype
        if traintype == "Tait":
            set = '381M-208T-230D-317M'
        
        # make the user set traintype have priority/
        if traintype != 'auto':
            type = traintype
            
        # Add train to the list
        id = addTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title(), notes)
        # await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
        if line in vLineLines:
            embed = discord.Embed(title="Train Logged",colour=0x7e3e98)
        elif line == 'Unknown':
                embed = discord.Embed(title="Train Logged")
        else:
            try:
                embed = discord.Embed(title="Train Logged",colour=lines_dictionary[line][1])
            except:
                embed = discord.Embed(title="Train Logged")
        
        embed.add_field(name="Set", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}, {round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), start, end), 1)}km')
        if notes:
            embed.add_field(name="Notes", value=notes)
        # thing to find image:
        print(f"Finding image for {number}")
        if type == 'Tait':
            image = 'https://railway-photos.xm9g.net/photos/317M-6.webp'
        
        if not '-' in set:
            image = getImage(set)

        else:
            hyphen_index = set.find("-")
            if hyphen_index != -1:
                first_car = set[:hyphen_index]
                print(f'First car: {first_car}')
                image = getImage(first_car)
                if image == None:
                    last_hyphen = set.rfind("-")
                    if last_hyphen != -1:
                        last_car = set[last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                        print(f'Last car: {last_car}')
                        image = getImage(last_car)
                        if image == None:
                            image = getImage(type)
                            print(f'the loco number is: {set}')
        if image != None:
            embed.set_thumbnail(url=image)
        
        await ctx.edit_original_response(embed=embed)
        await addAchievement(ctx.user.name, ctx, ctx.user.mention)

        
                        
    # Run in a separate task
    asyncio.create_task(log())

    
#thing to delete the stuff
@trainlogs.command(name='delete', description='Delete a logged trip. Defaults to the last logged trip.')
@app_commands.describe(id = "The ID of the log that you want to delete.", mode='What mode of log to delete?')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Train", value="train"),
    app_commands.Choice(name="Melbourne Tram", value="tram"),
    app_commands.Choice(name="NSW Train", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Train", value="adelaide-trains"),
    app_commands.Choice(name="Perth Train", value="perth-trains"),
    app_commands.Choice(name="Bus", value="bus"),
])
async def deleteLog(ctx, mode:str, id:str='LAST'):
    
    async def deleteLogFunction():
        log_command(ctx.user.id, 'log-delete')
        if id[0] == '#':
            idformatted = id[1:].upper()
        else:
            idformatted = id.upper()

        if idformatted != 'LAST':
            if not is_hex(idformatted):
                cmds = await bot.tree.fetch_commands()
                for cmd in cmds:
                    if cmd.name == 'train-logs':
                        cmdid = cmd.id
                        await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </train-logs view:{cmdid}>.',ephemeral=True)
                        return
                
            
        dataToDelete = universalReadRow(ctx.user.name, idformatted, mode)
        if dataToDelete in ['no data at all','no data for user']:
            await ctx.response.send_message(f'You have no logs you can delete!',ephemeral=True)
            return
        elif dataToDelete == 'invalid id did not show up':
            cmds = await bot.tree.fetch_commands()
            for cmd in cmds:
                if cmd.name == 'train-logs':
                    cmdid = cmd.id
                    await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </train-logs view:{cmdid}>.',ephemeral=True)
                    return
        else:
            idformatted1 = deleteRow(ctx.user.name, idformatted, mode)
            if idformatted == 'LAST':
                await ctx.response.send_message(f'Most recent log (`#{idformatted1}`) deleted. The data was:\n`{dataToDelete}`',ephemeral=True)
            else:
                await ctx.response.send_message(f'Log `#{idformatted}` deleted. The data was:\n`{dataToDelete}`',ephemeral=True)
            
    asyncio.create_task(deleteLogFunction())

    
  # tram logger goes here
@trainlogs.command(name="tram", description="Log a Melbourne tram you have been on")
@app_commands.describe(number = "Tram Number", date = "Date in DD/MM/YYYY format", route = 'Tram Line', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)

@app_commands.choices(route=[
        app_commands.Choice(name="1 East Coburg - South Melbourne Beach", value="1"),
        app_commands.Choice(name="3 Melbourne University - Malvern East", value="3"),
        app_commands.Choice(name="5 Melbourne University- Malvern", value="5"),
        app_commands.Choice(name="6 Brunswick tram depot - Glen Iris", value="6"),
        app_commands.Choice(name="11 West Preston - Victoria Harbour Docklands", value="11"),
        app_commands.Choice(name="12 Victoria Gardens - St Kilda", value="12"),
        app_commands.Choice(name="16 Melbourne University - Kew", value="16"),
        app_commands.Choice(name="19 North Coburg - Flinders Street station", value="19"),
        app_commands.Choice(name="30 St Vincent's Plaza - Central Pier Docklands", value="30"),
        app_commands.Choice(name="35 City Circle", value="35"),
        app_commands.Choice(name="48 Balwyn North - Victoria Harbour Docklands", value="48"),
        app_commands.Choice(name="57 West Maribyrnong - Flinders Street station", value="57"),
        app_commands.Choice(name="58 West Coburg - Toorak", value="58"),
        app_commands.Choice(name="59 Airport West - Flinders Street station", value="59"),
        app_commands.Choice(name="64 Melbourne University - Brighton East", value="64"),
        app_commands.Choice(name="67 Melbourne University - Carnegie", value="67"),
        app_commands.Choice(name="70 Wattle Park - Waterfront City Docklands", value="70"),
        app_commands.Choice(name="72 Melbourne University - Camberwell", value="72"),
        app_commands.Choice(name="75 Vermont South Shopping Centre - Central Pier Docklands", value="75"),
        app_commands.Choice(name="78 North Richmond - Balaclava", value="78"),
        app_commands.Choice(name="82 Footscray - Moonee Ponds", value="82"),
        app_commands.Choice(name="86 Bundoora RMIT - Waterfront City Docklands", value="86"),
        app_commands.Choice(name="96 Brunswick East - St Kilda Beach", value="96"),
        app_commands.Choice(name="109 Box Hill Central - Port Melbourne", value="109")
])

async def logtram(ctx, route:str, number: str='Unknown', date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        log_command(ctx.user.id, 'log-tram')
        print("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # checking if train number is valid
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        type = tramType(number.upper())
        if type == None:
            type = 'N/A'

        # Add train to the list
        id = addTram(ctx.user.name, number, type, savedate, route, start.title(), end.title())
        await ctx.response.send_message(f"Added {number} ({type}) on route {route} on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())
    
    
    
# sydney train logger
async def NSWstation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = NSWstations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="sydney-train", description="Log a Sydney/NSW train you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of train', date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station')
@app_commands.autocomplete(start=NSWstation_autocompletion)
@app_commands.autocomplete(end=NSWstation_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="T1 North Shore & Western Line", value="T1"),
        app_commands.Choice(name="T2 Inner West & Leppington Line", value="T2"),
        app_commands.Choice(name="T3 Bankstown Line", value="T3"),
        app_commands.Choice(name="T4 Eastern Suburbs & Illawarra Line", value="T4"),
        app_commands.Choice(name="T5 Cumberland Line", value="T5"),
        app_commands.Choice(name="T6 Lidcombe & Bankstown Line", value="T6"),
        app_commands.Choice(name="T7 Olympic Park Line", value="T7"),
        app_commands.Choice(name="T8 Airport & South Line", value="T8"),
        app_commands.Choice(name="T9 Northern Line", value="T9"),
        
        app_commands.Choice(name="Metro North West Line", value="Metro North West Line"),

        app_commands.Choice(name="Blue Mountains Line", value="Blue Mountains Line"),
        app_commands.Choice(name="Central Coast & Newcastle Line", value="Central Coast & Newcastle Line"),
        app_commands.Choice(name="Hunter Line", value="Hunter Line"),
        app_commands.Choice(name="South Coast Line", value="South Coast Line"),
        app_commands.Choice(name="Southern Highlands Line", value="Southern Highlands Line"),

        app_commands.Choice(name="North Coast Region", value="North Coast Region"),
        app_commands.Choice(name="North Western Region", value="North Western Region"),
        app_commands.Choice(name="Southern Region", value="Southern Region"),
        app_commands.Choice(name="Western Region", value="Western Region"),

        app_commands.Choice(name="Unknown", value="Unknown")
])
@app_commands.choices(type=[
        app_commands.Choice(name="K set", value="K set"),
        app_commands.Choice(name="Tangara - T Set", value="Tangara"),
        app_commands.Choice(name="Millennium - M Set", value="Millennium"),
        app_commands.Choice(name="OSCAR - H set", value="OSCAR"),
        app_commands.Choice(name="Waratah - A & B sets", value="Waratah"),
        
        app_commands.Choice(name="V set", value="V set"),
        app_commands.Choice(name="D set", value="D set"),
        app_commands.Choice(name="Endeavour railcar", value="Endeavour railcar"),
        app_commands.Choice(name="Hunter railcar", value="Hunter railcar"),
        app_commands.Choice(name="XPT", value="XPT"),
        app_commands.Choice(name="Xplorer", value="Xplorer"),
        
        app_commands.Choice(name="Metropolis Stock", value="Metropolis Stock"),

        app_commands.Choice(name="Unknown", value="Unknown"),
])
# SYdney train logger nsw train
async def logNSWTrain(ctx, number: str, type:str, line:str, date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        log_command(ctx.user.id, 'log-nsw-train')
        print("logging the nsw sydney train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addSydneyTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())


# Adelaide LOGGER AND overland logger
async def Adelaidestation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Adelaidestations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def Adelaideline_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Adelaidelines_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="adelaide-train", description="Log an Adelaide Metro or Journey Beyond train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station')
@app_commands.autocomplete(start=Adelaidestation_autocompletion)
@app_commands.autocomplete(end=Adelaidestation_autocompletion)
@app_commands.autocomplete(line=Adelaideline_autocompletion)

# Adelaide train logger journey beyond too
async def logNSWTrain(ctx, number: str, line:str, date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    log_command(ctx.user.id, 'log-adelaide-train')
    print(date)
    async def log():
        print("logging the adelaide train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        
        if number.startswith('NR'):
            type = 'NR Class'
        elif number.startswith('4'):
            type = '4000 Class'
        elif number.startswith('3'):
            if number.startswith('31'):
                type = '3100 Class'
            else:
                type = '3000 Class'
        else:
            type = 'Unknown'
        
        # Add train to the list
        id = addAdelaideTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())
    
# Perth logger
async def Perthstation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Perthstations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def Perthline_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Perthlines_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="perth-train", description="Log a Perth train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station')
@app_commands.autocomplete(start=Perthstation_autocompletion)
@app_commands.autocomplete(end=Perthstation_autocompletion)
@app_commands.autocomplete(line=Perthline_autocompletion)

# Perth logger
async def logPerthTrain(ctx, number: str, line:str, start:str, end:str, date:str='today'):
    channel = ctx.channel
    log_command(ctx.user.id, 'log-perth-train')
    print(date)
    async def log():
        print("logging the perth train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        
        if 201 <= int(number) >=248:
            type = 'A-Series'
        elif 301 <= int(number) >=348:
            type = 'A-Series'
        elif 4049 <= int(number) >=4126:
            type = 'B-Series'
        elif 6049 <= int(number) >=6126:
            type = 'B-Series'
        elif 5049 <= int(number) >=5126:
            type = 'B-Series'
        elif int(number)< 5126:
            type = 'C-Series'
        else:
            type = 'Unknown'
        
        # Add train to the list
        id = addPerthTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())


@trainlogs.command(name="sydney-tram", description="Log a Sydney Tram/Light Rail you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Light Rail Line', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(start=NSWstation_autocompletion)
@app_commands.autocomplete(end=NSWstation_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="L1 Dulwich Hill Line", value="L1"),
        app_commands.Choice(name="L2 Randwick", value="L2"),
        app_commands.Choice(name="L3 Kingsford Line", value="L3"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="Urbos 3", value="Urbos 3"),
        app_commands.Choice(name="Citadis 305", value="Citadis 305"),
])
# SYdney tram logger nsw tram
async def logNSWTram(ctx, type:str, line:str, number: str='Unknown', date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        log_command(ctx.user.id, 'log-nsw-tram')
        print("logging the sydney tram")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addSydneyTram(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())



async def busOpsautocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = busOps.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]
    
@trainlogs.command(name="bus", description="Log a Bus you have been on")
@app_commands.describe(number = "Bus number", type = 'Type of bus', date = "Date in DD/MM/YYYY format", line = 'bus route', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(operator=busOpsautocompletion)

# @app_commands.autocomplete(end=NSWstation_autocompletion)

async def logBus(ctx, line:str, operator:str='Unknown', date:str='today', start:str='N/A', end:str='N/A', type:str='Unknown', number: str='Unknown',):
    channel = ctx.channel
    print(date)
    async def log():
        log_command(ctx.user.id, 'log-bus')
        print("logging the bus")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        set = number

        # Add train to the list
        id = addBus(ctx.user.name, set, type, savedate, line, start.title(), end.title(), operator.title())
        await ctx.response.send_message(f"Added bus on route {line} on {savedate} from {start.title()} to {end.title()} with bus number {set} ({type}) Operator: {operator} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())



# train logger reader log view

vLineLines = ['Geelong','Warrnambool', 'Ballarat', 'Maryborough', 'Ararat', 'Bendigo','Echuca', 'Swan Hill','Albury', 'Seymour', 'Shepparton', 'Traralgon', 'Bairnsdale']

@trainlogs.command(name="view", description="View logged trips for a user")
@app_commands.describe(user = "Who do you want to see the data of?", mode = 'Train or tram logs?')
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="train"),
        app_commands.Choice(name="Melbourne Trams", value="tram"),
        app_commands.Choice(name="Bus", value="bus"),
        app_commands.Choice(name="NSW Trains", value="sydney-trains"),
        app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
        app_commands.Choice(name="Adelaide Trains & Journey Beyond", value="adelaide-trains"),
        app_commands.Choice(name="Perth Trains", value="perth-trains"),

])

async def userLogs(ctx, mode:str='train', user: discord.User=None, id:str=None):
    async def sendLogs():
        log_command(ctx.user.id, 'view-log')
        if user == None:
                userid = ctx.user
        else:
            userid = user
            
        if id != None:
            
            if mode == 'train':
                file_path = f'utils/trainlogger/userdata/{userid.name}.csv'
                
            if mode == 'tram':
                file_path = f'utils/trainlogger/userdata/tram/{userid.name}.csv'
            
            if mode == 'bus':
                file_path = f'utils/trainlogger/userdata/bus/{userid.name}.csv'  
                
            if mode == 'sydney-trains':
                file_path = f'utils/trainlogger/userdata/sydney-trains/{userid.name}.csv'  
            if mode == 'sydney-trams':
                file_path = f'utils/trainlogger/userdata/sydney-trams/{userid.name}.csv' 
            if mode == 'adelaide-trains':
                file_path = f'utils/trainlogger/userdata/adelaide-trains/{userid.name}.csv' 
            if mode == 'perth-trains':
                file_path = f'utils/trainlogger/userdata/perth-trains/{userid.name}.csv'   
                
            
            
            with open(file_path, mode='r', newline='') as file:
                
                if not id.startswith('#'):
                    cleaned_id = '#' + id
                else:
                    cleaned_id = id
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[0] == cleaned_id.upper():
                        
                        # thing to find image:
                        if row[2] == 'Tait':
                            image = 'https://railway-photos.xm9g.net/photos/317M-6.webp'
                        
                        if not '-' in row[1]:
                            image = getImage(row[1])

                        else:
                            hyphen_index = row[1].find("-")
                            if hyphen_index != -1:
                                first_car = row[1][:hyphen_index]
                                print(f'First car: {first_car}')
                                image = getImage(first_car)
                                if image == None:
                                    last_hyphen = row[1].rfind("-")
                                    if last_hyphen != -1:
                                        last_car = row[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                                        print(f'Last car: {last_car}')
                                        image = getImage(last_car)
                                        if image == None:
                                            image = getImage(row[2])
                                            print(f'the loco number is: {row[1]}')
                                        
                            # Make the embed
                        if row[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {row[0]}",colour=0x7e3e98)
                        elif row[4] == 'Unknown':
                                embed = discord.Embed(title=f"Log {row[0]}")
                        else:
                            try:
                                embed = discord.Embed(title=f"Log `{row[0]}`",colour=lines_dictionary[row[4]][1])
                            except:
                                embed = discord.Embed(title=f'Log `{id}`')
                        embed.add_field(name=f'Set', value="{} ({})".format(row[1], row[2]))
                        embed.add_field(name=f'Line', value="{}".format(row[4]))
                        embed.add_field(name=f'Date', value="{}".format(row[3]))
                        embed.add_field(name=f'Trip', value=f"{row[5]} to {row[6]}")
                        if row[5] != 'N/A' and row[6] != 'N/A':
                            embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), row[5], row[6]))}km')
                        try:
                            if row[7]:
                                embed.add_field(name='Notes:', value=row[7])
                        except:
                            pass
                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            print('no image')
                        await ctx.response.send_message(embed=embed)
                await ctx.response.send_message(f'Cannot find log `{id}`')
                
        else:
            # for train
            if mode == 'train':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
            
                # create thread
                try:
                    logsthread = await ctx.channel.create_thread(
                        name=f'{userid.name}\'s Train Logs',
                        auto_archive_duration=60,
                        type=discord.ChannelType.public_thread
                    )
                except Exception as e:
                    await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
                    
                # send reponse message
                pfp = userid.avatar.url
                embed=discord.Embed(title='Train Logs', colour=0x7e3e98)
                embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
                embed.add_field(name='Click here to view your logs:', value=f'<#{logsthread.id}>')
                await ctx.response.send_message(embed=embed)
                await logsthread.send(f'# <:train:1241164967789727744> {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                        
                        # thing to find image:
                        if not ('-' in sublist[1]):
                            image = getImage(sublist[1])
                        else:
                            hyphen_index = sublist[1].find("-")
                            if hyphen_index != -1:
                                first_car = sublist[1][:hyphen_index]
                                print(f'First car: {first_car}')
                                image = getImage(first_car)
                                if image == None:
                                    last_hyphen = sublist[1].rfind("-")
                                    if last_hyphen != -1:
                                        last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                                        print(f'Last car: {last_car}')
                                        image = getImage(last_car)
                                        if image == None:
                                            image = getImage(sublist[2])
                                            print(f'the loco number is: {sublist[1]}')
                                        
                        #send in thread to reduce spam!
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=0x7e3e98)
                        elif sublist[4] == 'Unknown':
                                embed = discord.Embed(title=f"Log `{sublist[0]}`")
                        else:
                            try:
                                embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=lines_dictionary[sublist[4]][1])
                            except:
                                embed = discord.Embed(title=f"Log {sublist[0]}")
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        if sublist[5] != 'N/A' and sublist[6] != 'N/A':
                            embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km')
                        if sublist[7]:
                            embed.add_field(name='Notes:', value=sublist[7])
                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            print('no image')
                        
                        await logsthread.send(embed=embed)
                        # if count == 6:
                        #     await ctx.channel.send('Max of 5 logs can be sent at a time. Use the csv option to see all logs')
                        #     return
            # for tram:
            if mode == 'tram':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/tram/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readTramLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Tram Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' #<:tram:1241165701390012476> {userid.name}\'s Tram Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                        
                        # # thing to find image:
                        # hyphen_index = sublist[1].find("-")
                        # if hyphen_index != -1:
                        #     first_car = sublist[1][:hyphen_index]
                        #     print(f'First car: {first_car}')
                        #     image = getImage(first_car)
                        #     if image == None:
                        #         last_hyphen = sublist[1].rfind("-")
                        #         if last_hyphen != -1:
                        #             last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                        #             print(f'Last car: {last_car}')
                        #             image = getImage(last_car)
                        #             if image == None:
                        #                 image = getImage(sublist[2])
                        #                 print(f'the loco number is: {sublist[1]}')
                                        
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0x7e3e98)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0x71bf44)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        # embed.set_thumbnail(url=image)

                        await logsthread.send(embed=embed)
                        time.sleep(0.5)
            
            # for sydney light rail tram:
            if mode == 'sydney-trams':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/sydney-trams/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readSydneyLightRailLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Sydney Light Rail Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Light Rail Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                        
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed

                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xed2438)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(0.5) 
            
            # for nsw train:
            if mode == 'sydney-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/sydney-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readSydneyTrainLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s NSW Train Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# <:NSWTrains:1255084911103184906>  {userid.name}\'s NSW Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                        
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0x7e3e98)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xf47913)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(0.5)     
            # for adelaide:
            if mode == 'adelaide-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/adelaide-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Adelaide trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Adelaide trains logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readPerthLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Adelaide trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Adelaide trains logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Adelaide Train Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' # <:Adelaide_train_:1300008231510347807><:journeybeyond:1300021503093510155> {userid.name}\'s Adelaide Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s Adelaide Train logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xf68a24)
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        # embed.add_field(name=f'Operator', value="{}".format(sublist[7]))
                        embed.add_field(name=f'Number', value="{} ({})".format(sublist[1], sublist[2]))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(0.5)
                          
            # for perth:
            if mode == 'perth-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/perth-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Perth trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Perth trains logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readAdelaideLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Perth trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Perth trains logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Perth Train Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# <:transperthtrain:1326470161385128019> {userid.name}\'s Perth Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s Perth Train logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xf68a24)
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Number', value="{} ({})".format(sublist[1], sublist[2]))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(0.5)  
            # for bus:
            if mode == 'bus':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/bus/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no busses logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no busses logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readBusLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no busses logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no busses logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Bus Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' # <:bus:1241165769241530460> {userid.name}\'s Bus Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s bus logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xf68a24)
                        embed.add_field(name=f'Route', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Operator', value="{}".format(sublist[7]))
                        embed.add_field(name=f'Bus Number', value="{} ({})".format(sublist[1], sublist[2]))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(0.5)  
    asyncio.create_task(sendLogs())

# train log stats
@trainlogs.command(name="stats", description="View stats for a logged user's trips.")
@app_commands.describe(stat='Type of stats to view', user='Who do you want to see the data of?', format='Diffrent ways and graphs for showing the data.', mode='Train or Tram logs?')
@app_commands.choices(stat=[
    app_commands.Choice(name="Lines", value="lines"),
    app_commands.Choice(name="Stations", value="stations"),
    app_commands.Choice(name="Trips", value="pairs"),
    app_commands.Choice(name="Trip Length (VIC train only)", value="length"),
    app_commands.Choice(name="Sets", value="sets"),
    app_commands.Choice(name="Dates", value="dates"),
    app_commands.Choice(name="Types", value="types"),
    app_commands.Choice(name="Operators", value="operators"),
])
@app_commands.choices(format=[
    app_commands.Choice(name="List and Bar chart", value="l&g"),
    app_commands.Choice(name="Pie chart", value="pie"),
    app_commands.Choice(name="CSV file", value="csv"),
    app_commands.Choice(name="Daily Chart", value="daily"),
])
@app_commands.choices(mode=[
    app_commands.Choice(name="All", value="all"),
    # app_commands.Choice(name="All Trains", value="all-trains"),
    # app_commands.Choice(name="All Trams", value="all-trams"),

    app_commands.Choice(name="Victorian Trains", value="train"),
    app_commands.Choice(name="Melbourne Trams", value="tram"),
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="New South Wales Trains", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Trains", value="adelaide-trains"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),

])
async def statTop(ctx: discord.Interaction, stat: str, format: str='l&g', global_stats:bool=False, user: discord.User = None, mode:str = 'all', year:int=0):
    async def sendLogs():
        log_command(ctx.user.id, 'log-stats')
        statSearch = stat
        userid = user if user else ctx.user
        
        if userid.name == 'comeng_17':
            name = 'comeng17'
        else:
            name = userid
            
        if global_stats:
            data = globalTopStats(statSearch)
        else:
            try:
                if stat == 'operators':
                    data = topOperators(userid.name)
                elif stat == 'length':
                    data = getLongestTrips(userid.name)  
                elif mode == 'all':
                    data = allTopStats(userid.name, statSearch, year)
                else:
                    data = topStats(userid.name, statSearch, year, mode)
                
            except:
                await ctx.response.send_message('You have no logged trips!')
        count = 1
        message = ''
        
        # top operators thing:
        if stat == 'operators':
            try:
                pieChart(data, f'Top Operators ― {name}', ctx.user.name)
                await ctx.response.send_message(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.response.send_message('User has no logs!')  
        if stat == 'length':
            try:
                # create thread
                try:
                    logsthread = await ctx.channel.create_thread(
                        name=f"{userid.name}'s longest trips in Victoria",
                        auto_archive_duration=60,
                        type=discord.ChannelType.public_thread
                    )
                except Exception as e:
                    await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
                    
                # send reponse message
                pfp = userid.avatar.url
                embed=discord.Embed(title=f"{userid.name}'s longest trips in Victoria", colour=0x0070c0)
                embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
                embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
                await ctx.response.send_message(embed=embed)
                
                lines = data.splitlines()
                chunks = []
                current_chunk = ""
                await logsthread.send('Here are your longest trips in Victoria:')

                for line in lines:
                    # Check if adding this line would exceed the max_length
                    if len(current_chunk) + len(line) + 1 > 1500:  # +1 for the newline character
                        chunks.append(current_chunk)
                        current_chunk = line
                    else:
                        if current_chunk:
                            current_chunk += "\n" + line
                        else:
                            current_chunk = line

                # Add the last chunk
                if current_chunk:
                    chunks.append(current_chunk)
                    
                for i, chunk in enumerate(chunks):
                    await logsthread.send(chunk)
                
            except Exception as e:
                await ctx.response.send_message(f"Error: `{e}`")
                
        # make temp csv
        csv_filename = f'temp/top{stat.title()}.{userid}-t{time.time()}.csv'
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)  # Use csv.writer on csv_file, not csvs
            for item in data:
                station, times = item.split(': ')
                writer.writerow([station, times.split()[0]])
        
        if format == 'csv':
            try:
                await ctx.response.send_message("Here is your file:", file=discord.File(csv_filename))
            except:
                ctx.response.send_message('You have no logs!')
            
        elif format == 'l&g':
            # create thread
            try:
                logsthread = await ctx.channel.create_thread(
                    name=stat.title(),
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
            except Exception as e:
                await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
                
            # send reponse message
            pfp = userid.avatar.url
            embed=discord.Embed(title=stat.title(), colour=0x0070c0)
            embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
            embed.add_field(name='Click here to view your stats:', value=f'<#{logsthread.id}>')
            await ctx.response.send_message(embed=embed)
            for item in data:
                station, times = item.split(': ')
                message += f'{count}. **{station}:** `{times}`\n'
                count += 1
                if len(message) > 1900:
                    await logsthread.send(message)
                    message = ''
            try:
                if global_stats:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} ― Global', ctx.user.name)
                else:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} in {year} ― {name}' if year !=0 else f'Top {stat.title()} ― {name}', ctx.user.name)
                await logsthread.send(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await logsthread.send('User has no logs!')
        elif format == 'pie':
            try:
                if global_stats:
                    pieChart(csv_filename, f'Top {stat.title()} ― {name}', ctx.user.name)
                else:
                    pieChart(csv_filename, f'Top {stat.title()} ― Global', ctx.user.name)

                await ctx.response.send_message(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.response.send_message('You have no logs!')
        elif format == 'daily':
            if stat != 'dates':
                await ctx.response.send_message('Daily chart can only be used with the stat set to Top Dates')
            try:
                dayChart(csv_filename, ctx.user.name)
                await ctx.response.send_message(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                ctx.response.send_message('User has no logs!')
    await sendLogs()

@stats.command(name='termini', description='View which line termini you have been to')
async def termini(ctx):
    log_command(ctx.user.id, 'log-termini')
    try:
        data =terminiList(ctx.user.name)
    except:
        data = 'No logs found'
    
    if len(data) <= 2000:
        await ctx.response.send_message(data)
    else:
        await ctx.response.send_message(f"Termini you have visited:")
        split_strings = []
        start = 0
        
        while start < len(data):
            # Find the index where the string should be split
            if start + 2000 < len(data):
                split_index = data.rfind('\n', start, start + 2000)
                if split_index == -1:
                    split_index = start + 2000
            else:
                split_index = len(data)
            
            split_strings.append(data[start:split_index])
            start = split_index + 1  # Move past the newline or split point
            
        for item in split_strings:
            await ctx.channel.send(item)

@completion.command(name='sets', description='View which sets you have been on')
@app_commands.choices(train=[
    app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
    app_commands.Choice(name="Comeng", value="Comeng"),
    app_commands.Choice(name="Siemens Nexas", value="Siemens Nexas"),
    app_commands.Choice(name="HCMT", value="HCMT"),
    app_commands.Choice(name='VLocity', value='VLocity'),
    app_commands.Choice(name='Sprinter', value='Sprinter'),
    app_commands.Choice(name='N Class', value='N Class'),
])
async def sets(ctx, train:str):
    userid = ctx.user
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-sets')
    try:
        data =setlist(ctx.user.name, train)
    except:
        await ctx.edit_original_response(content='No logs found!')
    
    # create thread
    try:
        logsthread = await ctx.channel.create_thread(
            name=f'{train} sets {userid.name} has been on',
            auto_archive_duration=60,
            type=discord.ChannelType.public_thread
        )
    except Exception as e:
        await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
        
    # send reponse message
    pfp = userid.avatar.url
    embed=discord.Embed(title=f'{train} sets {userid.name} has been on', colour=0x0070c0)
    embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
    embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
    await ctx.edit_original_response(embed=embed)

    if len(data) <= 2000:
        await logsthread.send(data)
    else:
        await logsthread.send(f"{train} sets you have been on:")
        split_strings = []
        start = 0
        
        while start < len(data):
            # Find the index where the string should be split
            if start + 2000 < len(data):
                split_index = data.rfind('\n', start, start + 2000)
                if split_index == -1:
                    split_index = start + 2000
            else:
                split_index = len(data)
            
            split_strings.append(data[start:split_index])
            start = split_index + 1
            
        for item in split_strings:
            await logsthread.send(item)


@completion.command(name='stations', description='View which you have visited')
@app_commands.choices(state=[
    app_commands.Choice(name="Victoria", value="Victorian"),
    app_commands.Choice(name="New South Wales", value="New South Wales"),
    app_commands.Choice(name="South Australia", value="South Australian"),
])
async def sets(ctx, state:str):
    userid = ctx.user
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-stations')
    try:
        data =stationlist(ctx.user.name, state)
    except Exception as e:
        await ctx.edit_original_response(content='No logs found')
        print(f'ERROR: {e}')
        
    # create thread
    try:
        logsthread = await ctx.channel.create_thread(
            name=f'{state} stations {userid.name} has been to',
            auto_archive_duration=60,
            type=discord.ChannelType.public_thread
        )
    except Exception as e:
        await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
        
    # send reponse message
    pfp = userid.avatar.url
    embed=discord.Embed(title=f'{state} stations {userid.name} has been to', colour=0x0070c0)
    embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
    embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
    await ctx.edit_original_response(embed=embed)
    
    if len(data) <= 2000:
        await logsthread.send(data)
    else:
        await logsthread.send(f"{state} stations you have been to:")
        split_strings = []
        start = 0
        
        while start < len(data):
            # Find the index where the string should be split
            if start + 2000 < len(data):
                split_index = data.rfind('\n', start, start + 2000)
                if split_index == -1:
                    split_index = start + 2000
            else:
                split_index = len(data)
            
            split_strings.append(data[start:split_index])
            start = split_index + 1  # Move past the newline or split point
            
        for item in split_strings:
            await logsthread.send(item)

@bot.tree.command(name='submit-photo', description="Submit a photo to railway-photos.xm9g.net and the bot.")
async def submit(ctx: discord.Interaction, photo: discord.Attachment, car_number: str, date: str, location: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'submit-photo')
    async def submitPhoto():
        target_guild_id = 1214139268725870602
        target_channel_id = 1238821549352685568
        
        showcase_channel = 1322889624250486848
        
        target_guild = bot.get_guild(target_guild_id)
        if target_guild:
            channel = target_guild.get_channel(target_channel_id)
            public_channel = target_guild.get_channel(showcase_channel)
            if channel:
                if photo.content_type.startswith('image/'):
                    await photo.save(f"./photo-submissions/{photo.filename}")
                    file = discord.File(f"./photo-submissions/{photo.filename}")
                    await channel.send(f'# Photo submitted by <@{ctx.user.id}>:\n- Number {car_number}\n- Date: {date}\n- Location: {location}\n<@780303451980038165> ', file=file)
                    
                    # publically send embed
                    embed = discord.Embed(title='Photo Submission', 
                      description=f'Photo submitted by <@{ctx.user.id}>:\n- Number {car_number}\n- Date: {date}\n- Location: {location}')
                    file = discord.File(f"./photo-submissions/{photo.filename}", filename=f'{photo.filename}')
                    embed.set_image(url=f"attachment://{photo.filename}")
                    await public_channel.send(embed=embed, file=file)
                    await ctx.edit_original_response(content='Your photo has been submitted and will be reviewed shortly!\nSubmitted photos can be used in their original form with proper attribution to represent trains, trams, groupings, stations, and stops. They will be featured on the Discord bot and on https://railway-photos.xm9g.net.\n[Join the Discord server to be notified when you photo is accepted.](https://discord.gg/nfAqAnceQ5)')
                else:
                    await ctx.edit_original_response(content="Please upload a valid image file.")
            else:
                await ctx.edit_original_response(content="Error: Target channel not found.")
        else:
            await ctx.edit_original_response(content="Error: Target guild not found.")

    await submitPhoto()
    
@stats.command(name='profile', description="Shows a users trip log stats, and leaderboard wins")    
async def profile(ctx, user: discord.User = None):
    log_command(ctx.user.id, 'view-profile')
    try:
        await ctx.response.defer()
        async def profiles():
            if user == None:
                username = ctx.user.name
                pfp = ctx.user.avatar.url
            else:
                username = user.name
                pfp = user.avatar.url

            embed = discord.Embed(title=f"Profile")
            embed.set_author(name=username, url='https://xm9g.net', icon_url=pfp)

            
            # train logger
            try:
                lines = topStats(username, 'lines', 0, 'train')
                stations = topStats(username, 'stations', 0, 'train')
                sets = topStats(username, 'sets', 0, 'train')
                trains = topStats(username, 'types', 0, 'train')
                dates = topStats(username, 'dates', 0, 'train')
                trips = topStats(username, 'pairs', 0, 'train')

                #other stats stuff:
                eDate =lowestDate(username, 'train')
                LeDate =highestDate(username, 'train')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:train:1241164967789727744><:vline:1241165814258729092> Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Train:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Set:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'**Total logs:** `{logAmounts(username, "train")}`\n'
            f'**Stations visited:** `{stationPercent(username)}`\n'
            f'**Lines visited:** `{linePercent(username)}`\n'
            f'**Distance:** `{round(getTotalTravelDistance(username))}km`'
    )

                            
            except FileNotFoundError:
                embed.add_field(name="<:train:1241164967789727744><:vline:1241165814258729092> Train Log Stats", value=f'{username} has no logged trips!')
                    
            # Tram Logger
            try:
                lines = topStats(username, 'lines', 0, 'tram')
                stations = topStats(username, 'stations', 0, 'tram')
                sets = topStats(username, 'sets', 0, 'tram')
                trains = topStats(username, 'types', 0, 'tram')
                dates = topStats(username, 'dates', 0, 'tram')
                trips = topStats(username, 'pairs', 0, 'tram')

                #other stats stuff:
                eDate =lowestDate(username, 'tram')
                LeDate =highestDate(username, 'tram')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:tram:1241165701390012476> Tram Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Class:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Tram Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "tram")}'
    )

    
            except FileNotFoundError:
                embed.add_field(name="<:tram:1241165701390012476> Tram Log Stats", value=f'{username} has no logged trips!')

    # sydney trains Logger
            try:
                lines = topStats(username, 'lines', 0, 'sydney-trains')
                stations = topStats(username, 'stations', 0, 'sydney-trains')
                sets = topStats(username, 'sets', 0, 'sydney-trains')
                trains = topStats(username, 'types', 0, 'sydney-trains')
                dates = topStats(username, 'dates', 0, 'sydney-trains')
                trips = topStats(username, 'pairs', 0, 'sydney-trains')
                
                #other stats stuff:
                eDate =lowestDate(username, 'sydney-trains')
                LeDate =highestDate(username, 'sydney-trains')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:NSWTrains:1255084911103184906><:NSWMetro:1255084902748000299> Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Train Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "sydney-trains")}'
    )

                                    
            except FileNotFoundError:
                embed.add_field(name="<:NSWTrains:1255084911103184906><:NSWMetro:1255084902748000299> Train Log Stats", value=f'{username} has no logged trips in NSW!')

    # sydney tram Logger
            try:
                lines = topStats(username, 'lines', 0, 'sydney-trams')
                stations = topStats(username, 'stations', 0, 'sydney-trams')
                sets = topStats(username, 'sets', 0, 'sydney-trams')
                trains = topStats(username, 'types', 0, 'sydney-trams')
                dates = topStats(username, 'dates', 0, 'sydney-trams')
                trips = topStats(username, 'pairs', 0, 'sydney-trams')
                
                #other stats stuff:
                eDate =lowestDate(username, 'sydney-trams')
                LeDate =highestDate(username, 'sydney-trams')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:NSWLightRail:1255084906053369856> Light Rail Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Tram Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "sydney-trams")}'
    )

                                    
            except FileNotFoundError:
                embed.add_field(name="<:NSWLightRail:1255084906053369856> Light Rail Log Stats", value=f'{username} has no logged trips in NSW!')
    
    
    # adelaide Logger
            try:
                lines = topStats(username, 'lines', 0, 'adelaide-trains')
                stations = topStats(username, 'stations', 0, 'adelaide-trains')
                sets = topStats(username, 'sets', 0, 'adelaide-trains')
                trains = topStats(username, 'types', 0, 'adelaide-trains')
                dates = topStats(username, 'dates', 0, 'adelaide-trains')
                trips = topStats(username, 'pairs', 0, 'adelaide-trains')

                #other stats stuff:
                eDate =lowestDate(username, 'adelaide-trains')
                LeDate =highestDate(username, 'adelaide-trains')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:Adelaide_train_:1300008231510347807><:journeybeyond:1300021503093510155> Adelaide Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "adelaide-trains")}'
    )
            except FileNotFoundError:
                embed.add_field(name="<:Adelaide_train_:1300008231510347807><:journeybeyond:1300021503093510155> Adelaide Train Log Stats:", value=f'{username} has no logged trips in Adelaide!')

        # perth Logger
            try:
                lines = topStats(username, 'lines', 0, 'perth-trains')
                stations = topStats(username, 'stations', 0, 'perth-trains')
                sets = topStats(username, 'sets', 0, 'perth-trains')
                trains = topStats(username, 'types', 0, 'perth-trains')
                dates = topStats(username, 'dates', 0, 'perth-trains')
                trips = topStats(username, 'pairs', 0, 'perth-trains')

                #other stats stuff:
                eDate =lowestDate(username, 'perth-trains')
                LeDate =highestDate(username, 'perth-trains')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:transperthtrain:1326470161385128019> Perth Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "perth-trains")}'
    )
                                    
            except FileNotFoundError:
                embed.add_field(name="<:transperthtrain:1326470161385128019> Perth Train Log Stats", value=f'{username} has no logged trips in Perth!')
            
    # bus Logger
            try:
                lines = topStats(username, 'lines', 0, 'bus')
                stations = topStats(username, 'stations', 0, 'bus')
                sets = topStats(username, 'sets', 0, 'bus')
                trains = topStats(username, 'types', 0, 'bus')
                dates = topStats(username, 'dates', 0, 'bus')
                trips = topStats(username, 'pairs', 0, 'bus')
                
                #other stats stuff:
                eDate =lowestDate(username, 'bus')
                LeDate =highestDate(username, 'bus')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:Canberra_Bus:1264885650826465311> Bus Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Bus Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "bus")}'
    )

                                    
            except FileNotFoundError:
                embed.add_field(name="<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:Canberra_Bus:1264885650826465311> Bus Log Stats", value=f'{username} has no logged bus trips!')

            
            #games
            stats = fetchUserStats(username)
            
            if stats[0] != 'no stats':
                item, wins, losses = stats[0]
                embed.add_field(name=':question: Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%')
            else:
                embed.add_field(name=':question: Station Guesser', value='No data',inline=False)
            if stats[1] != 'no stats':
                item, wins, losses = stats[1]
                embed.add_field(name=':interrobang: Ultrahard Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%')
            else:
                embed.add_field(name=':interrobang: Ultrahard Station Guesser', value='No data',inline=False)
            if stats[2] != 'no stats':
                item, wins, losses = stats[2]
                embed.add_field(name=':left_right_arrow: Station Order Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
            else:
                embed.add_field(name=':left_right_arrow: Station Order Guesser', value='No data',inline=False)
            
            # other stats
            embed.set_footer(text=f"Favorite command: {getFavoriteCommand(ctx.user.id)[0]}")
            
            await ctx.edit_original_response(embed=embed)
            
        await profiles()
        
    except Exception as e:
        await ctx.edit_original_response(content = f"Error: `{e}`")

@bot.command()
async def refreshachievements(ctx):
    log_command(ctx.author.id, 'refresh-achievements')
    response = await ctx.send('Checking for new Achievements...')
    await addAchievement(ctx.author.name,ctx, ctx.author.mention)
    
@achievements.command(name='view', description='View your achievements.')
@app_commands.describe(user="Who's achievements to show?")
async def viewAchievements(ctx, user: discord.User = None):
    await ctx.response.defer()
    log_command(ctx.user.id, 'view-achievements')

    if user is None:
        user = ctx.user

    # Get user's achievements
    filepath = f'utils/trainlogger/achievements/data/{user.name}.csv'
    user_achievements = []
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                user_achievements.extend(row)

    # Create embed
    embed = discord.Embed(title=f"{user.name}'s Achievements", color=0x43ea46)
    
    # Get all achievements from master list
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        rowcount = 0
        for row in reader:
            if row:  # Skip empty rows
                achievement_id = row[0]
                name = row[1]
                description = row[2]
                
                # Add checkmark if user has achievement
                if achievement_id in user_achievements:
                    embed.add_field(name=f"✅ {name}", value=description, inline=False)
                else:
                    embed.add_field(name=f"❌ {name}", value=description, inline=False)
                rowcount = rowcount + 1
            if rowcount == 25:
                break

    await ctx.edit_original_response(embed=embed)

    
    
@bot.tree.command(name="line-status", description="View your line status for all lines.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.choices(operator=[
    app_commands.Choice(name="Metro", value="metro"),
    app_commands.Choice(name="V/Line", value="vline"),
])
async def checklines(ctx, operator: str):
    # Defer the response to avoid timeout
    await ctx.response.defer()
    log_command(ctx.user.id, 'line-status')

    # Run the async function in the background
    asyncio.create_task(run_in_thread(ctx, operator))

async def run_in_thread(ctx, operator):
    statuses = [f'{datetime.now()}']
    log_channel = bot.get_channel(int(config['STARTUP_CHANNEL_ID']))

    # Process metro lines
    if operator == 'metro':
        embed_metro = discord.Embed(title=f'<:train:1241164967789727744> Metro Line Status', color=0x008dd0, timestamp=discord.utils.utcnow())
        lines = ['Alamein', 'Belgrave', 'Craigieburn', 'Cranbourne', 'Mernda', 'Frankston', 'Glen%20Waverley', 'Hurstbridge', 'Lilydale', 'Pakenham', 'Sandringham', 'Stony%20Point', 'Sunbury', 'Upfield', 'Werribee', 'Williamstown']
        
        # Process each line in a separate background thread to avoid blocking
        for line in lines:
            json_info_str = await asyncio.to_thread(route_api_request, line, "0")
            json_info = json.loads(json_info_str.replace("'", '"'))
            
            # Process JSON data
            routes = json_info['routes']
            status = json_info['status']
            route = routes[0]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            route_id = route['route_id']
            route_name = route['route_name']
            
            if description == "Service Information":
                description = "Good Service"
            
            disruptionDescription = ""
            try:
                disruptions = await asyncio.to_thread(disruption_api_request, route_id)
                general_disruption = disruptions["disruptions"]["metro_train"][0]
                disruptionDescription = general_disruption["description"]
            except Exception as e:
                print(e)

            color = genColor(description)
            info = f'{description}'
            embed_metro.add_field(name=f'{route_name}', value=f'{statusEmoji(description)} {info}', inline=True)
            statuses.append(description)

    # Process V/Line lines
    # Made by Comeng17
    elif operator == 'vline':
        embed_vline = discord.Embed(title=f'<:vline:1241165814258729092> V/Line Line Status', color=0x7f3e98, timestamp=discord.utils.utcnow())
        lines = ['Geelong - Melbourne', 'Warrnambool - Melbourne via Apollo Bay & Geelong', 'Ballarat-Wendouree - Melbourne via Melton', 'Ararat - Melbourne via Ballarat', 'Maryborough - Melbourne via  Ballarat', 'Bendigo - Melbourne via Gisborne', 'Echuca-Moama - Melbourne via Bendigo or Heathcote', 'Swan Hill - Melbourne via Bendigo', 'Seymour - Melbourne via Broadmeadows', 'Shepparton - Melbourne via Seymour', 'Albury - Melbourne via Seymour', 'Traralgon - Melbourne via Morwell & Moe & Pakenham', 'Bairnsdale - Melbourne via Sale & Traralgon']
        
        for line in lines:
            line = line.replace(" ", "%20")
            json_info_str = await asyncio.to_thread(route_api_request, line, "3")
            json_info = json.loads(json_info_str.replace("'", '"'))
            
            routes = json_info['routes']
            route = routes[0]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            route_id = route['route_id']
            route_name = route['route_name']
            
            # Simplify route name
            route_name = route_name.split(' - ')[0]  # This is a simple approach; adjust if names change
            
            disruptionDescription = ""
            try:
                disruptions = await asyncio.to_thread(disruption_api_request, route_id)
                general_disruption = disruptions["disruptions"]["regional_train"][0]
                disruptionDescription = general_disruption["description"]
                disruption_vline = general_disruption["disruption_type"]
                currentness = general_disruption["disruption_status"]
                if currentness == "Planned" or disruption_vline == "Service Information":
                    disruption_vline = "Good Service"
            except Exception as e:
                print(e)

            color = genColor(disruption_vline)
            info = f'{disruption_vline}'
            embed_vline.add_field(name=f'{route_name}', value=f'{statusEmoji(disruption_vline)} {info}', inline=True)
            statuses.append(disruption_vline)

    try:
        # Send the response after data is processed
        await ctx.edit_original_response(embed=embed_metro if operator == 'metro' else embed_vline)
    except Exception as e:
        print(f'ERROR: {e}')

    with open('logs.txt', 'a') as file:
        file.write(f"LINE STATUS CHECKED MANUALLY\n")
        
    with open('utils/line-status-data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(statuses)

#about/credits
@bot.tree.command(name="about", description="View information about the bot.")
async def about(ctx):
    await ctx.response.defer()
    log_command(ctx.user.id, 'about')
    embed = discord.Embed(title="About", description="TrackPulse VIC is a Discord bot that allows users to log their train, tram, and bus trips in Victoria, New South Wales and South Australia. It also provides real-time line status updates for Metro Trains Melbourne, as well as a range of other features.", color=discord.Color.blue())
    embed.add_field(name="Developed by", value="[Xm9G](https://xm9g.net/)\n", inline=True)
    embed.add_field(name="Contributions by",value='[domino6658](https://github.com/domino6658)\n[AshKmo](https://github.com/AshKmo)\n[Comeng17](https://github.com/Comeng17)',inline=True)
    embed.add_field(name='Photos sourced from',value="[XM9G's Victorian Railway Photos](https://railway-photos.xm9g.net/)")
    embed.add_field(name="Data Sources", value="[Public Transport Victoria](https://www.ptv.vic.gov.au/)\n", inline=True)
    embed.add_field(name='Discord Server', value='https://discord.gg/nfAqAnceQ5')
    await ctx.edit_original_response(embed=embed)


# year in review
@bot.tree.command(name="year-in-review", description="View your year in review for a specific year.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def yearinreview(ctx, year: int=2024):
    async def yir():
        await ctx.response.defer()
        log_command(ctx.user.id, 'year-in-review')
        current_year = datetime.now().year
        unix_time = int(time.time())
        if current_year == year:
            if unix_time < 1732971600:
                # await ctx.edit_original_response(content=f"Your {current_year} year in review will be available <t:1732971600:R>.")
                # return
                pass
        try:
        
            embed = discord.Embed(title=f":bar_chart: {ctx.user.name}'s Victorian Trains Year in Review: {year}", color=discord.Color.blue())
            data = year_in_review(f'utils/trainlogger/userdata/{ctx.user.name}.csv', year)
            
            (lilydale_value, ringwood_value), count = data.get("top_pair")
            embed.add_field(name=f"In {year} {ctx.user.name} went on {str(data['total_trips'])} train trips :chart_with_upwards_trend:", value=f"\n**First Trip:** {data['first_trip'][5]} to {data['first_trip'][6]} on {data['first_trip'][3]} :calendar_spiral: \n**Last Trip:** {data['last_trip'][5]} to {data['last_trip'][6]} on {data['last_trip'][3]} :calendar_spiral: \n\n:star: **Favorite Trip:** {lilydale_value} to {ringwood_value} - {count} times\n:metro: {vline_metroprecent(ctx.user.name, year)}", inline=False)
            
            top_lines = data['top_5_lines']
            formatted_lines = "\n".join([f"{i + 1}. {line[0]}: {line[1]} trips" for i, line in enumerate(top_lines)])
            embed.add_field(name=f"{ctx.user.name}'s Top Lines :railway_track:", value=formatted_lines or "No lines found.", inline=False)
            
            top_stations = data['top_5_stations']
            formatted_stations = "\n".join([f"{i + 1}. {line[0]}: {line[1]} visits" for i, line in enumerate(top_stations)])
            embed.add_field(name=f"{ctx.user.name}'s Top Stations :station:", value=formatted_stations or "No Stations found.", inline=False)
            
            top_stations = data['top_5_trains']
            formatted_stations = "\n".join([f"{i + 1}. {line[0]}: {line[1]} trips" for i, line in enumerate(top_stations)])
            embed.add_field(name=f"{ctx.user.name}'s Top Train types :train:", value=formatted_stations or "No Trains found.", inline=False)
            
            top_stations = data['top_number']
            formatted_stations = "\n".join([f"{i + 1}. {line[0]}: {line[1]} trips" for i, line in enumerate(top_stations)])
            embed.add_field(name=f"{ctx.user.name}'s Top Trains :bullettrain_side:", value=formatted_stations or "No Trains found.", inline=False)
            
            # v/line vs metro percent
            
            embed.set_thumbnail(url=ctx.user.avatar.url)
            embed.set_footer(text="Trains Logged with TrackPulse VIC", icon_url="https://xm9g.net/discord-bot-assets/logo.png")

            await ctx.edit_original_response(embed=embed)
            
        except Exception as e:
            await ctx.edit_original_response(embed=discord.Embed(title="Error", description=f"An error occurred while fetching data: {e}"))
        
    asyncio.create_task(yir())
    
    
# THING TO UPDATE CSV

# Disabled to not fuck up the data by accident
'''@bot.command()
async def ids(ctx: commands.Context) -> None:
    if ctx.author.id in admin_users:
        checkaddids = addids()
        if checkaddids == 'no userdata folder':
            await ctx.send('Error: No userdata folder found.')
        else:
            await ctx.send('Hexadecimal IDs have been added to all CSV files in the userdata folder.\n**Do not run this command again.**')'''

# @bot.tree.command(name='train-emoji', description='Sends emojis of the train (Art by MPTG)')
# # @app_commands.allowed_installs(guilds=True, users=True)
# # @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# @app_commands.choices(train=[
#     app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
#     app_commands.Choice(name="EDI Comeng", value="EDI Comeng"),
#     app_commands.Choice(name="Alstom Comeng", value="Alstom Comeng"),
#     app_commands.Choice(name="Siemens Nexas", value="Siemens Nexas"),
#     # app_commands.Choice(name="HCMT", value="HCMT"),
#     app_commands.Choice(name='VLocity', value='VLocity'),
#     app_commands.Choice(name='Sprinter', value='Sprinter'),
#     # app_commands.Choice(name='N Class', value='N Class'),
# ])
# async def trainemoji(ctx, train:str):
#     async def sendemojis():
#         await ctx.response.send_message(setEmoji(train))
        
#     asyncio.create_task(sendemojis())
    
# HERE ARE THE INTERNAL USE COMMANDS

@bot.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if ctx.author.id in admin_users:

        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException as e:
                print(f'Error: {e}')
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

# sends a message to a specific channel
@bot.command()
async def send(ctx, user: discord.Member, *, message: str):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'send')
        try:
            await user.send(message)
            await ctx.send(f"Sent message to {user.mention}.")
        except discord.errors.Forbidden:
            await ctx.send("Couldn't send a message to that user.")
    else:
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert latency to ms
    await ctx.send(f"Pong! Latency: {latency} ms")
    log_command(ctx.author.id, 'ping')
    
@bot.command()
async def syncdb(ctx, url='https://railway-photos.xm9g.net/trainsets.csv'):
    if str(ctx.author.id) == USER_ID:
        log_command(ctx.author.id, 'sync-db')
        csv_url = url
        save_location = "utils/trainsets.csv"
        await ctx.send(f"Downloading trainset data from {csv_url} to {save_location}")
        print(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            download_csv(csv_url, save_location)
            await ctx.send(f"Sucsess!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")
    else:
        print(f'{USER_ID} tried to synd the database.')
        await ctx.send("You are not authorized to use this command.")
        
@bot.command()
async def syncgame(ctx):
    if str(ctx.author.id) == USER_ID:
        log_command(ctx.author.id, 'sync-db')
        csv_url = 'https://railway-photos.xm9g.net/botgames/guesser.csv'
        save_location = "utils/game/images/guesser.csv"
        await ctx.send(f"Downloading guesser data from {csv_url} to {save_location}")
        print(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            download_csv(csv_url, save_location)
            await ctx.send(f"Sucsess!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")
            
        csv_url = 'https://railway-photos.xm9g.net/botgames/ultrahard.csv'
        save_location = "utils/game/images/ultrahard.csv"
        await ctx.send(f"Downloading ultrahard data from {csv_url} to {save_location}")
        print(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            download_csv(csv_url, save_location)
            await ctx.send(f"Sucsess!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")
    else:
        print(f'{USER_ID} tried to synd the database.')
        await ctx.send("You are not authorized to use this command.")
    
# imptrant
bot.run(BOT_TOKEN)