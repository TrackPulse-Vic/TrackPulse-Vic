'''TrackPulse Vic
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
from math import e
from numbers import Number
import operator
from shutil import ExecError
import shutil
import sqlite3
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import asyncio
import threading
from datetime import datetime
import time
import csv
import random
from typing import Literal, Optional
import typing
from re import A
import traceback
import os
from pathlib import Path
import git
import pandas as pd
import builtins

# thing to make it work on all oses
import sys

from commands.NSWsearchtrain import NSWsearchTrainCommand
from commands.searchPhoto import searchTrainPhoto
from commands.searchtrain import searchTrainCommand
sys.stdout = sys.__stdout__  # Reset stdout if needed

original_open = builtins.open

original_mkdir = os.mkdir
def custom_mkdir(path, mode=0o777):
    if isinstance(path, str):
        fixed_path = path.replace('\\', os.sep).replace('/', os.sep)
    else:
        fixed_path = str(path).replace('\\', os.sep).replace('/', os.sep)
    # print(f"Creating dir: {fixed_path}", flush=True) 
    return original_mkdir(fixed_path, mode)
os.mkdir = custom_mkdir

original_open = builtins.open
def custom_open(file, *args, **kwargs):
    if isinstance(file, str):
        fixed_path = file.replace('\\', os.sep).replace('/', os.sep)
        # print(f"Opening: {fixed_path}", flush=True)
    else:
        fixed_path = file
    try:
        return original_open(fixed_path, *args, **kwargs)
    except FileNotFoundError as e:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, fixed_path)
        print(f"Trying alt path: {alt_path}", flush=True)
        try:
            return original_open(alt_path, *args, **kwargs)
        except:
            raise e
builtins.open = custom_open

original_listdir = os.listdir
def custom_listdir(path='.'):
    if isinstance(path, str):
        fixed_path = path.replace('\\', os.sep).replace('/', os.sep)
    else:
        fixed_path = str(path).replace('\\', os.sep).replace('/', os.sep)
    print(f"Listing dir: {fixed_path}", flush=True)
    return original_listdir(fixed_path)
os.listdir = custom_listdir

# Commands imports
from commands.help import helpCommand
from commands.logexport import logExport

# Utils imports
from utils import trainset
from utils.directions import getDirectionName
from utils.downloader import downloader_function
from utils.favourites.viewer import *
from utils.search import *
from utils.colors import *
from utils.stationID import nameToStopID
from utils.stats.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *
from logconverter import convertLogsToDB

# trainlogger imports
from utils.trainlogger.achievements.check import awardAchievement, checkAchievements, checkGameAchievements, checkHangmanAchievements, getAchievementInfo
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.trainlogger.map.readlogs import logMap
from utils.trainlogger.map.mapimage import compress, legend
from utils.trainlogger.map.lines_dictionaries import *
from utils.trainlogger.achievements import *
from utils.trainlogger.graph import *

from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.locationFromNumber import *
from utils.photo import *
from utils.mykipython import *
from utils.myki.savelogin import *
from utils.special.yearinreview import *
from utils.stoppingpattern import *
from utils.locationfromid import *
from utils.stationDisruptions import *
from utils.stats.stats import *
from utils.vlineTrickery import getVlineStopType




print("""TrackPulse Vic Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions""")

# Load data from text files to lists

file = open('utils\\datalists\\lines.txt','r')
lines_list = []
for line in file:
    line = line.strip()
    lines_list.append(line)
file.close()

file = open('utils\\datalists\\types.txt','r')
types_list = []
for line in file:
    line = line.strip()
    types_list.append(line)
file.close()

file = open('utils\\datalists\\nswstations.txt','r')
NSWstations_list = []
for line in file:
    line = line.strip()
    NSWstations_list.append(line)
file.close()

file = open('utils\\datalists\\nswstops.txt','r')
NSWstops_list = []
for line in file:
    line = line.strip()
    NSWstops_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidestations.txt','r')
Adelaidestations_list = []
for line in file:
    line = line.strip()
    Adelaidestations_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidestops.txt','r')
Adelaidestops_list = []
for line in file:
    line = line.strip()
    Adelaidestops_list.append(line)
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

file = open('utils\\datalists\\autogeneratedptvlists\\metrostops.txt','r')
metro_stops = []
for line in file:
    line = line.strip()
    metro_stops.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\tramstops.txt','r')
tram_stops = []
for line in file:
    line = line.strip()
    tram_stops.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\busstops.txt','r')
bus_stops = []
for line in file:
    line = line.strip()
    bus_stops.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\vlinestops.txt','r')
vline_stops = []
for line in file:
    line = line.strip()
    vline_stops.append(line)
file.close()

file = open('utils\\datalists\\heritagestations.txt','r')
heritage_stations = []
for line in file:
    line = line.strip()
    heritage_stations.append(line)
file.close()


# Create lists of stops

metro_stations = metro_stops
metro_stations = [station.replace(' Station','') for station in metro_stations]

vline_stations = []
for stop in vline_stops:
    if stop.endswith(" Railway Station"):
        vline_stations.append(stop.replace(' Railway Station',''))

metro_tunnel_stations = ['Town Hall','Arden','Anzac','Parkville','State Library']
stations_list = metro_stations + vline_stations + metro_tunnel_stations + heritage_stations
stations_list = sorted(set(stations_list))

vline_coach_stops = []
for stop in vline_stops:
    if not stop.endswith(" Railway Station"):
        vline_coach_stops.append(stop)
ptv_list = metro_stops + vline_stops + tram_stops + bus_stops
ptv_list = sorted(set(ptv_list))

ptv_list_short = metro_stops + tram_stops + bus_stops
ptv_list_short = sorted(set(ptv_list_short))

bus_coach_stops = bus_stops + vline_coach_stops
bus_coach_stops = sorted(set(bus_coach_stops))

# Create required folders cause their not on github
required_folders = ['utils/trainlogger/userdata','temp','utils/trainlogger/userdata/adelaide-trains','utils/trainlogger/userdata/adelaide-trams','utils/trainlogger/userdata/sydney-trains','utils/trainlogger/userdata/sydney-trams','utils/trainlogger/userdata/perth-trains','utils/trainlogger/userdata/bus','utils/trainlogger/userdata/tram',
                    'utils/trainlogger/achievements/data','utils/train/images','utils/game/images','utils/game/scores','photo-submissions','logins','utils/favourites/data','utils/trainlogger/userdata/maps']
for folder in required_folders:
    if os.path.exists(folder) and os.path.isdir(folder):
        print(f"{folder} exists")
    else:
        os.makedirs(folder)    
        print(f'Created {folder}')


#V/Line Rail Lines
vLineLines = ['Geelong','Warrnambool', 'Ballarat', 'Maryborough', 'Ararat', 'Bendigo','Echuca', 'Swan Hill','Albury', 'Seymour', 'Shepparton', 'Traralgon', 'Bairnsdale']
vline_rail_lines = [1706, 1837, 1823, 1728, 1740, 1849, 1745, 4871, 1710, 1908, 1848, 1824, 1853]


# Colours
achievement_colour = 0x43ea46
rare_trains_colour = 0xf23f42
ptv_grey = 0x333434

metro_colour = 0x0072ce
vline_colour = 0x8f1a95
vline_map_colour = 0x782f9a
tram_colour = 0x78be20
bus_colour = 0xff8200
coach_colour = 0xa57fb2
myki_colour = 0xc2d840

sydney_train_colour = 0xf47913
sydney_tram_colour = 0xed2438

transperth_colour = 0x008635
transwa_colour = 0xcf4520

adelaide_metro_colour = 0xf68a24 #this may or may not need fixing
adelaide_tram_colour = adelaide_metro_colour

#guesser colours
very_easy_colour = 0x89ff65
easy_colour = 0xcaff65
medium_colour = 0xffe665
hard_colour = 0xffa665
very_hard_colour = 0xff6565
ultrahard_colour = 0xe52727

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
STARTUP_CHANNEL_ID = int(config['STARTUP_CHANNEL_ID']) # channel id to send the startup message
RARE_SERVICE_CHANNEL_ID = int(config['RARE_SERVICE_CHANNEL_ID'])
COMMAND_PREFIX = config['COMMAND_PREFIX']
USER_ID = config['USER_ID']

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())
log_channel = bot.get_channel(STARTUP_CHANNEL_ID)

async def printlog(text):
    print(text)
    if len(str(text)) < 1000:
        log_channel = bot.get_channel(STARTUP_CHANNEL_ID)
        await log_channel.send(text)

# check if these things are on in the .env
rareCheckerOn = False
automatic_updates = False
admin_users = [1002449671224041502, 780303451980038165, int(USER_ID)]
if config['RARE_SERVICE_CHECKER'] == 'ON':
    rareCheckerOn = True
startupAchievements = False
if config['STARTUP_REFRESH_ACHIEVEMENTS'] == 'ON':
    startupAchievements = True
if config['AUTOMATIC_UPDATES'] == 'ON':
    automatic_updates = True
if config['DEVS_TO_HAVE_ADMIN_ACCESS'] == 'OFF':
    admin_users = [int(USER_ID)]
# settings
    
lineStatusOn = False

channel_game_status = {} # variable to store what channels are running the guessing game

global traintoedit 
traintoedit = None # var that will store the selected train in the db to edit.

# line stations and colours
lines_dictionary_main = {
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
    'Unknown/Other':[[None], ptv_grey],
}

# Command Groups
class CommandGroups(app_commands.Group):
    ...

trainlogs = CommandGroups(name='log')
games = CommandGroups(name='games')
search = CommandGroups(name='search')
stats = CommandGroups(name='stats')
maps = CommandGroups(name='maps')
myki = CommandGroups(name='myki')
completion = CommandGroups(name='completion')
achievements = CommandGroups(name='achievements')
favourites = CommandGroups(name='favourite')

async def download_csv(url, save_path):
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            await printlog(f"CSV downloaded successfully and saved as {save_path}")
        else:
            raise Exception(f"Failed to download CSV. Status code: {response.status_code}")

@bot.event
async def on_ready():
    # download the trainset data     
    csv_url = "https://railway-photos.xm9g.net/trainsets.csv"
    save_location = "utils/trainsets.csv"
    # await printlog(f"Downloading trainset data from {csv_url} to {save_location}")
    # await download_csv(csv_url, save_location)
    
    channel = bot.get_channel(STARTUP_CHANNEL_ID)

    bot.tree.add_command(trainlogs)
    bot.tree.add_command(games)
    bot.tree.add_command(search)
    bot.tree.add_command(stats)
    bot.tree.add_command(maps)
    bot.tree.add_command(myki)
    bot.tree.add_command(completion)
    bot.tree.add_command(achievements)
    bot.tree.add_command(favourites)

    try:
        await channel.send(f"""TrackPulse Vic Copyright (C) 2024  Billy Evans
        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions""")
    except Exception as e:
        await printlog(f'Error: {e}\n make sure the bot has premission to send in the startup channel')
        return
    
    try:
        task_loop.start()
    except:
        await printlog("WARNING: Rare train checker is not enabled!")
        await channel.send(f"WARNING: Rare train checker is not enabled! <@{USER_ID}>")

    activity = discord.Activity(type=discord.ActivityType.watching, name='Melbourne trains')
    await bot.change_presence(activity=activity)
    
    # Refresh all users
    if startupAchievements:
        channel_id = int(config['STARTUP_CHANNEL_ID'])  # Convert string to integer
        response_channel = bot.get_channel(channel_id)
        
        if response_channel is None:
            await printlog(f"Error: Could not find channel with ID {channel_id}")
            return
        
        response = await response_channel.send('Checking log achievements for all users...')
        
        user_files = os.listdir('utils/trainlogger/userdata')
        csv_files = [f for f in user_files if f.endswith('.csv')]
        
        for csv_file in csv_files:
            username = csv_file[:-4]  # Remove .csv extension
            await response.edit(content=f'Checking achievements for {username}...')
            await addAchievement(username, channel_id, f'<@{username}>')
        
        mode = 'guesser'
        filepath = f"utils/game/scores/{mode}.csv"
        new_achievements = []

        await response.edit(content='Finished checking log achievements for all users')
        response = await response_channel.send('Checking game achievements for all users...')

        with open(filepath, mode='r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row != ['username','id','wins','losses']:
                    username = row[1]
                    await response.edit(content=f'Checking game achievements for {username}...')
                    
                    #send achievement message
                    new = checkGameAchievements(username)
                    for achievement in new:
                        info = getAchievementInfo(achievement)
                        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
                        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
                        await channel.send(f'<@{username}>',embed=embed)
                
        await response.edit(content='Finished checking game achievements for all users')

    # restart or normal start
    file = open('restart.txt','r')
    file = file.read()

    if file == '':
        await printlog("Bot started")
    else:
        await printlog("Bot restarted")
        channel = bot.get_channel(int(file))
        await channel.send("Bot restarted")
        with open('restart.txt', 'w') as file:
                file.write('')

# achievement awarder  check achievements
async def addAchievement(username, channel, mention):
    channel = bot.get_channel(channel)
    new = checkAchievements(username)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await channel.send(mention,embed=embed)
        
# game achievement awarder  check game achievements
async def addGameAchievement(username, channel, mention, game:str='guesser'):
    await printlog(f'checking game achievements for {username}')
    channel = bot.get_channel(channel)
    print('game:', game)
    if game == 'guesser':
        new = checkGameAchievements(username)
    elif game == 'hangman':
        new = checkHangmanAchievements(username)
    print('New achievements:', new)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await channel.send(mention,embed=embed)


# Rare train finder
async def check_rare_trains_in_thread():
    rare_trains = checkRareTrainsOnRoute()
    asyncio.run_coroutine_threadsafe(log_rare_trains(rare_trains), bot.loop)

async def log_rare_trains(rare_trains):
    log_channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)
    channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)

    if rare_trains:
        embed = discord.Embed(title="Trains found on lines they are not normally on!", color=rare_trains_colour)

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

# async def check_lines_in_thread():
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
help_commands = ['Which /log command should I use?','/about','/achievements view','/completion sets','/completion stations','/departures','/favourite add','/favourite remove','/games station-guesser','/games station-hangman','/games station-order','/help','/line-status','/log adelaide-train','/log adelaide-tram','/log bus','/log delete','/log edit','/log export','/log import','/log perth-train','/log stats','/log sydney-train','/log sydney-tram','/log train','/log tram','/log view','/disruptions','/maps trips','/maps view','/myki calculate-fare','/search ptv','/search route','/search station','/search run','/search train','/search train-photo','/search tram','/stats leaderboard','/stats profile','/stats termini','/submit-photo','/wongm','/year-in-review']

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
    await helpCommand(ctx, category, command)


    
@bot.tree.command(name="disruptions", description="Show disruptions on a Metro line")
@app_commands.describe(line="What Metro line to show disruptions for?")
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
    await ctx.response.defer()
    log_command(ctx.user.id, 'line_info')

    # Retrieve line information from API
    json_info_str = route_api_request(line, "0")
    json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
    json_info = json.loads(json_info_str)

    routes = json_info["routes"]
    status = json_info["status"]

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

    await printlog(f"route id: {route_id}")

    # Retrieve disruption information
    disruption_description = ""
    try:
        disruptions = disruption_api_request(route_id)

        # Extracting title and description
        for general_disruption in disruptions["disruptions"]["metro_train"]:
            if general_disruption["display_on_board"]:
                disruption_description = general_disruption["description"]
                url = general_disruption['url']
                updateTime = convert_iso_to_unix_time(general_disruption['last_updated'])
                break

    except Exception as e:
        await printlog(f'here: {e}')

    # Determine the color of the embed based on the status description
    color = genColor(description)
    await printlog(f"Status color: {color}")

    # Create the embed with the retrieved information
    if disruption_description:
        embed = discord.Embed(title=f"{description} - {route_name}", color=color, url=url if url else None)
    else:
        embed = discord.Embed(title=f"{description} - {route_name}", color=color)
    embed.add_field(name="Status Description", value=description, inline=False)
    if disruption_description:
        embed.add_field(name="Disruption Info", value=f'{disruption_description}\n\nUpdated {updateTime}', inline=False)
    else:
        embed.add_field(name="Disruption Info", value=f'There are no disruptions on the {route_name} line!', inline=False)

    # Send the embed to the Discord channel
    await ctx.edit_original_response(embed=embed)


# Route Seach v2
@search.command(name="route", description="Show info about a tram or bus route")
@app_commands.describe(mode = "What type of transport is this route?")
@app_commands.choices(mode=[
        app_commands.Choice(name="Bus", value="2"),
        app_commands.Choice(name="Tram", value="1"),
        app_commands.Choice(name="Metro Train", value="0"),
        # app_commands.Choice(name="VLine Train", value="3"),
        # app_commands.Choice(name="Night Bus", value="4"),
])
@app_commands.describe(number = "What route number to show info about?")

async def route(ctx, mode: str, number: int):  
    log_command(ctx.user.id, 'route_search')
    try:
        json_info_str = route_api_request(number, mode)
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {number}:")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=bus_colour)
        counter = 0
        found_routes = False
        
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
            url = ''
            try:
                disruptions = disruption_api_request(route_id)
                # await printlog(disruptions)
                
                # Extracting title and description
                general_disruption = disruptions["disruptions"]["metro_bus"][0]
                disruptionTitle = general_disruption["title"]
                disruptionDescription = general_disruption["description"]
                url = general_disruption['url']
                updateTime = convert_iso_to_unix_time(general_disruption['last_updated'])
                
            except Exception as e:
                await printlog(e)

            
            # disruption status:

             # Check if the route number is the one you want
            if route_number == str(number):
                found_routes = True
                # Create and send the embed only for the desired route number
                if url:
                    embed = discord.Embed(title=f"Route {route_number}:", color=getColor(mode), url=url)
                else:
                    embed = discord.Embed(title=f"Route {route_number}:", color=getColor(mode))
                embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
                embed.add_field(name="Status Description", value=description, inline=False)
                if disruptionDescription:
                    embed.add_field(name="Disruption Info",value=f'{disruptionDescription}\n\nUpdated {updateTime}', inline=False)
                    
                await channel.send(embed=embed)
          
            counter = counter + 1

        if not found_routes:
            await channel.send(f"No routes found matching number {number}")
                
    except Exception as e:
        await ctx.channel.send(f"error:\n`{e}`\nMake sure you inputted a valid route number, otherwise, the bot is broken.")


# train Photo search
@search.command(name="train-photo", description="Search for xm9g's railway photos")
@app_commands.describe(number="Carriage number", search_set="Search the full set instead of the train number")
async def line_info(ctx, number: str, search_set:bool=False):
    log_command(ctx.user.id, 'train-photo')
    await searchTrainPhoto(ctx, number, search_set)

# Station search station

async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
@search.command(name='station', description='View info about and a photo of a railway station')
@app_commands.autocomplete(station=station_autocompletion)
async def stationphoto(ctx, station:str):
    async def searchstationpic():
        await ctx.response.defer()
        log_command(ctx.user.id, 'search-station')
        
        data = stationInfoAPIRequest(nameToStopID(station, '0'), 0)
        mode = 0
        if data == None: # check if its a v/line stop
            await printlog('there is no data so im trying vline')
            data = stationInfoAPIRequest(nameToStopID(station, '3'), 3)
            mode = 3
            
        suburb = data['stop']['stop_location']['suburb']
        
        amenities = data['stop']['stop_amenities']
        phone = amenities['pay_phone']
        waitingRoom = amenities['sheltered_waiting_area']
        kiosk = amenities['kiosk']
        toilet = amenities['toilet']
        car_park = amenities['car_parking']
        bike_locker = amenities['bicycle_locker']
        bike_rack = amenities['bicycle_rack']
        zone = data['stop']['stop_ticket']['zone']
        ticket_machine = data['stop']['stop_ticket']['ticket_machine']
        
        stepfree = True
        if station.title() == 'Heyington':
            stepfree = False
        
        # routes:
        routelines = ''
        for route in data['stop']['routes']:    
            routelines += f'{route["route_name"]}\n'
        
        embed= discord.Embed(title=f'{getModeEmoji(mode)} {station.title()} Station', description=suburb)
        embed.add_field(name='Services', value=f'''🚻 Toilet: {yesOrNo(toilet)}\n⌚ Waiting Room: {yesOrNo(waitingRoom)}\n☕ Kiosk: {yesOrNo(kiosk)}\n📞 Payphone: {yesOrNo(phone)}''', inline=False)
        embed.add_field(name='Parking', value=f'''🚗 Parking Spaces: {car_park} spaces\n🚲 Bike Cage: {bike_locker} spaces, Bike Racks: {bike_rack} spaces''', inline=False)
        embed.add_field(name='Ticketing', value=f'{zone}\nTicket Machine {yesOrNo(ticket_machine)}', inline=False)
        if not stepfree:
            embed.add_field(name='⚠️ Accessibility', value='This station is not step free', inline=False)
        
        photo = getStationImage(station)
        if photo != None:
            embed.set_image(url=photo)
            embed.set_footer(text=f'Photo by {getPhotoCredits(station)}')
        else:
            await printlog('no photo')
            # await ctx.edit_original_response(content=f'No photos found for {station.title()}')
            
        await ctx.edit_original_response(embed=embed)
    asyncio.create_task(searchstationpic())
 
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
            
            embed=discord.Embed(title=f"Zone {start_zone} → {end_zone}", color=myki_colour)
            count=0
            for fair in fairs:
                type = fairs[count]['Passengemode']
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
            await printlog(e)
            
    asyncio.create_task(calc())
            

        
'''
# thing to save myki credentials to bot:
@myki.command(name='save-login', description='Save your PTV account username and password to the bot, run it again to change your saved info')
@app_commands.describe(ptvusername = "PTV accpunt username", ptvpassword = "PTV account password", encryptionpassword = "A password to encrypt your PTV password")
async def login(ctx, ptvusername: str, ptvpassword: str, encryptionpassword: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'save-login')
    encryptedPassword = encryptPW(encryptionpassword, ptvpassword)
    savelogin(ptvusername, str(encryptedPassword).split("'")[1], ctx.user.id) # the split is so it dosnt include the b' part
    await ctx.edit_original_response(content=f'Saved username and password to bot.\nUsername: `{ptvusername}`\nPassword: `{ptvpassword}`\nYour password is encrypted and cannot be seen by anyone. You will need to enter your encryption password to view your mykis with the bot.\nEncryption password: `{encryptionpassword}`')
    
# disabled myki view command

@myki.command(name='view', description='View your mykis and their balances')
@app_commands.describe(encriptionpassword = "Your encryption password from the login command")
async def viewmykis(ctx, encriptionpassword: str):
    loop = asyncio.get_event_loop()
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'view-myki')
    async def viewcards():
        # decrypt the password
        
        # get saved username and password:
        try:
            login = readlogin(ctx.user.id)
        except:
            return "You haven't logged in yet. Run </myki login:1289553446659166300> to login."

        try:
            decryptedPassword = decryptPW(encriptionpassword, login[1].encode())
        except Exception as e:
            return "Your encryption password is incorrect. Run </myki login:1289553446659166300> to reset it."
        
        # run the myki scraper
        try:
            data = getMykiInfo(login[0], decryptedPassword)
        except Exception as e:
            return f"There has been an error: `{e}`"
        
        # make embed
        embed = discord.Embed(title="Your Mykis", color=myki_colour)
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
'''
# Wongm search
@bot.tree.command(name="wongm", description="Search Wongm's Rail Gallery")
@app_commands.describe(search="search")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def line_info(ctx, search: str):
    log_command(ctx.user.id, 'wongm-search')
    channel = ctx.channel
    await printlog(f"removing spaces in search {search}")
    spaces_removed = search.replace(' ', '%20')
    await printlog(spaces_removed)
    url = f"https://railgallery.wongm.com/page/search/?s={spaces_removed}"
    await ctx.response.send_message(url)



# search Train search train
@search.command(name="train", description="Search for a specific Train")
@app_commands.describe(train="Carriage/Locomotive number to search for. For NSW you can also put the set number.", state="State to search in, will be found automattically if empty.", hide_run_info="Hide run info")
@app_commands.choices(state=[
        app_commands.Choice(name="Victoria", value="Victoria"),
        app_commands.Choice(name="New South Wales", value="NSW"),
])
async def train_search(ctx, train: str, state:str='auto', hide_run_info:bool=False):
    if train == 'IEV120': train = 'EV120'
    # try and auto find state
    if state == 'auto':
        Type = trainType(train) 
        if Type == f'Train type not found for {train}' or Type == None:
            print('Carriage is not victorian, checking for nsw')
            state = 'NSW'
        else:
            state = 'Victoria'
    
    if state == 'Victoria':
        # try:
        await searchTrainCommand(ctx, train, hide_run_info, metro_colour, vline_colour, ptv_grey,interchange_stations,lines_dictionary_main)
        # except Exception as e:
        #     await ctx.edit_original_response(content=f'An error has occored. Please try again.\n`{e}`')
        #     await printlog(f'Search Train error: {e}')
        #     return
    elif state == 'NSW':
        try:
            await NSWsearchTrainCommand(ctx,train)
        except Exception as e:
            await ctx.edit_original_response(content=f'An error has occored. Please try again.\n`{e}`')
            await printlog(f'Search Sydney Train error: {e}')
            return
    else:
        await ctx.response.send_message(f"{state} is not supported yet.")
        
            
# search run id   
@search.command(name="run", description="Shows the run for a specific TDN, found in the departures command")
@app_commands.describe(number="Run ID/TD Number", mode="Mode of transport to search run for")
@app_commands.choices(mode=[
        app_commands.Choice(name="Metro", value="metro"),
        # app_commands.Choice(name="V/Line", value="vline"),
        # app_commands.Choice(name="Tram", value="tram"),
        # app_commands.Choice(name="Bus", value="bus"),
        # app_commands.Choice(name="Night Bus", value="nightbus"),
        
])
async def runidsearch(ctx, number:str, mode:str='metro'):
    await ctx.response.defer()
    log_command(ctx.user.id, 'runid-search')
    async def addmap():
        try:
            line = ""
            if mode == "metro":
                runid = "9"+TDNtoRunID(number)
                runData = getTrainLocationFromID(str(runid))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 0)
                await printlog('Mode is metro')
            elif mode == "tram":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 1)
                await printlog('Mode is tram')
            elif mode == "bus":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 2)
                await printlog('Mode is bus')
            elif mode == "vline":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 3)
                await printlog('Mode is vline')
                async def strip_station_name(name):
                    return name.replace('Railway Station', '').strip()
                    
            elif mode == "nightbus":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 4)
                await printlog('Mode is nightbus')

                # Filter out entries where the station name has a slash and status is 'Skipped', then strip 'Railway Station'
                stoppingPattern = [
                    (strip_station_name(station[0]), station[1], station[2]) 
                    for station in stoppingPattern 
                    if not ('/' in station[0] and station[1] == 'Skipped')
]
            await printlog(f"STOPPING PATTERN: {stoppingPattern}")
            try:
                if mode == "metro":
                    if runData is not None:
                        for item in runData:
                            # latitude = item['vehicle_position']['latitude']
                            # longitude = item['vehicle_position']['longitude']
                            try:
                                vehicle = item['vehicle_descriptor']['description']
                            except:
                                print('couldnt get vehicle')
                                vehicle = 'Unknown Train'
                            line = get_route_name(item['route_id'])
                            await printlog(f'Line: {line}')
                elif mode == "vline":
                    line = 'V/Line'
                    await printlog(f'Line: {line}')
                else: # just make the mode the type name
                    line = mode
                    await printlog(f'Line: {line}')

            except Exception as e:
                await ctx.edit_original_response(content='No trip data available.')

                await printlog(f'ErROR: {e}')
                return
            
            # embed colour
            if mode == "metro":
                try:
                    colour = lines_dictionary_main[line][1]
                except:
                    colour = metro_colour
            elif mode == "vline":
                colour = vline_colour
            elif mode == "tram":
                colour = tram_colour
            elif mode == "bus" or mode == 'nightbus':
                colour = bus_colour
            
            embed = discord.Embed(title=f"{number}- {vehicle}", colour=colour, timestamp=discord.utils.utcnow())

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
            await printlog(f'ErROR: {e}') 
            await printlog(traceback.format_exc())  
            # await log_channel.send(f'Error: ```{e}```\n with finding train run ran by {ctx.user.mention}\n<@{USER_ID}>')

    # Run transportVicSearch in a separate thread
        
        
    asyncio.create_task(addmap())
            # loop = asyncio.get_event_loop()
            # task = loop.create_task(transportVicSearch_async(ctx, train.upper(), embed, embed_update))
            # await task
            
@search.command(name="tram", description="Search for a specific Tram")
@app_commands.describe(tram="tram")
async def tramsearch(ctx, tram: str):
    await ctx.response.defer()
    log_command(ctx.user.id, 'tram-search')
    channel = ctx.channel
    type = tramType(tram)
    set = tram.upper()
   
    await printlog(f'Set: {set}')
    await printlog(f"Tram Type: {type}")
    if type is None:
        await ctx.edit_original_response(content="Tram not found")
    else:
        embed = discord.Embed(title=f"Info for {tram.upper()}:", color=metro_colour)
        if set.endswith('-'):
            embed.add_field(name=type, value=set[:-1])
        else:
            embed.add_field(name=type, value=set)
        
        embed.set_thumbnail(url=getIcon(type))
        
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas','VLocity', 'Sprinter', 'N Class']:
            information = trainData(set)
            await printlog(information)
            infoData = f'**Livery:** {information[1]}\n**Status:** {information[3]}\n**Entered Service:** {information[2]}\n**Vicsig notes:** {information[4]}'
            if information[5]:
                infoData+=f'\n**Name:** {information[5]}'
                
            # thing if the user has been on
            async def check_variable_in_csv(variable, file_path):
                if not os.path.exists(file_path):
                    await printlog(f"The file {file_path} does not exist.")
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
        
        embed.add_field(name="Source:", value=f'[{getPhotoCredits(tram.upper())} (Photo)](https://railway-photos.xm9g.net?number={tram.upper()}), [MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html), [Vicsig (Other info)](https://vicsig.net)', inline=False)
        
        # embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
        embed_update = await ctx.edit_original_response(embed=embed)
    
# add a favourite stop
async def stop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    stations = ptv_list.copy()
    suggestions = []
    
    # Add matching stations 
    for station in stations:
        if current.lower() in station.lower():
            suggestions.append(app_commands.Choice(name=station, value=station))
    return suggestions[:25]

@favourites.command(name="add", description="Add a favourite stop")
@app_commands.describe(stop="Stop name")
@app_commands.autocomplete(stop=stop_autocompletion)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def favourite(ctx, stop: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'favourite-stop')
    
    # add the stop to the favourites
    message = save_favourites(ctx.user.id, stop)
    
    await ctx.edit_original_response(content=message)
    
async def stop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # Get favourites list
    favourites = get_favourites(interaction.user.id)
    suggestions = []
    
    # Add matching favourites
    for fav in favourites:
        if current.lower() in fav.lower():
            suggestions.append(app_commands.Choice(name=f"⭐ {fav}", value=fav))
    return suggestions[:25]

@favourites.command(name="remove", description="Remove a favourite stop")
@app_commands.describe(stop="Stop name")
@app_commands.autocomplete(stop=stop_autocompletion)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def remove(ctx, stop: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'remove-favourite-stop')
    
    # remove the stop from favourites
    message = remove_favourite(ctx.user.id, stop)
    
    await ctx.edit_original_response(content=message)

# Next departures for a station
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # Get favourites list
    favourites = get_favourites(interaction.user.id)
    stations = ptv_list_short.copy()
    suggestions = []
    
    # Add matching favourites first
    for fav in favourites:
        if current.lower() in fav.lower():
            suggestions.append(app_commands.Choice(name=f"⭐ {fav}", value=fav))
    
    # Add matching stations 
    for station in stations:
        if current.lower() in station.lower():
            suggestions.append(app_commands.Choice(name=station, value=station))
    return suggestions[:25]

async def time_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # Get favourites list
    times = list(pd.date_range("00:00", "23:59", freq="1min").strftime('%H:%M'))
    suggestions = []
    
    # Add matching time
    for time in times:
        if current.lower() in time.lower():
            suggestions.append(app_commands.Choice(name=time, value=time))
    return suggestions[:25]

@bot.tree.command(name="departures", description="Upcoming departures for a stop")
@app_commands.describe(stop="Station/Stop name")
@app_commands.autocomplete(stop=station_autocompletion)
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
        app_commands.Choice(name="Williamstown", value="Williamstown"),
        app_commands.Choice(name="Flemington Racecourse", value="Flemington Racecourse"),
        app_commands.Choice(name="City Circle", value="City Circle"),
    ]
)
@app_commands.describe(time="The time you want to search the departures from (use 24hr time format)")
@app_commands.autocomplete(time=time_autocompletion)

# test
async def departures(ctx, stop: str, time:str="none", line:str='all'):
    async def nextdeps(station, time):
        channel = ctx.channel
        await ctx.response.defer()
        log_command(ctx.user.id, 'departures-search')
        station = station.strip('⭐ ')
        try:
            await printlog(f'{ctx.user.name} ran departures for {station} at time {datetime.today()} in channel {ctx.channel.mention}')
        except:
            await printlog(f'{ctx.user.name} ran departures for {station} at time {datetime.today()}')

        if station in metro_stops:
            mode = '0'
        elif station in tram_stops:
            mode = '1'
        elif station in bus_stops:
            mode ='2'
        elif station in vline_stops:
            mode = '3'
        elif station.endswith('Railway Station'):
            mode = '3'
        else:
            mode = '0'
            

        if mode == '3':
            pass
            # await ctx.edit_original_response(content="You cannot currently search departures for V/Line services")
            return
        if line != "all" and mode != "0":
            await ctx.edit_original_response(content="You can only specify a line for trains")
            return
        
        print(f'Finding stop id for {station}, mode {mode}')
        stop_id = nameToStopID(station, mode)
        
        if stop_id == 'None':
            print('Trying to see if its a V/Line station')
            mode = 3
            stop_id = nameToStopID(f'{station} Railway Station', mode)
            if stop_id == 'None':
                await ctx.edit_original_response(content=f"Cannot find stop {station.title()}.")
                return

        timecopy = time
        if time == "none":
            dt = datetime.fromisoformat(str(datetime.today()))
            dt = dt.astimezone()
            final_time = dt.astimezone(timezone.utc)
        else:
            try:
                # add leading 0 to time
                if len(time) == 4:
                    time = '0' + time
                date = datetime.today().strftime('%Y-%m-%d')
                date = date + ' '
                time = date + time
                dt = datetime.fromisoformat(time)
                dt = dt.astimezone()
                final_time = dt.astimezone(timezone.utc)
            except Exception as e:
                await printlog(e)
            try: # this will see if its a valid time
                await printlog(final_time)
            except UnboundLocalError:
                await ctx.edit_original_response(content=f'Invalid time: `{timecopy}`, loading current departures <a:botloading2:1261102206468362381>')
                dt = datetime.fromisoformat(str(datetime.today()))
                dt = dt.astimezone()
                final_time = dt.astimezone(timezone.utc)

        start_time = convert_iso_to_unix_time(final_time, 'short-time')

        # get departures for the stop:
        depsData = departures_api_request(stop_id, mode)
        try:
            departures = depsData['departures']
            runs = depsData['runs']
            routes = depsData['routes']
        except:
            await ctx.edit_original_response(content=f"Cannot find departures for {station.title()}")
            return
         
        
        # make embed with data
        print(f'Making embed for mode {mode}')
        # Default embed title and color
        embed_title = f"Departures from {station.title()}"
        embed_color = ptv_grey

        # Customize embed based on mode and line
        if mode == "0":
            embed_color = metro_colour
            if line == "all":
                embed_title = f"Metro trains departing {station.title()}"
            else:
                embed_title = f"Metro trains departing {station.title()} on the {line} line"
        elif mode == "1":
            embed_color = tram_colour
            embed_title = f"Trams departing {station.title()}"
        elif mode == "2":
            embed_color = bus_colour
            embed_title = f"Busses departing {station.title()}"
        elif mode == "3":
            embed_color = vline_colour
            embed_title = f"V/Line trains departing {station.title()}"

        # Add "Station" suffix if not already present
        if not station.title().endswith('Station') and mode in ["0", "3"]:
            embed_title += " Station"
            
        # Add timestamp to title
        embed_title += f" after {start_time}"
        
        # Create embed
        embed = discord.Embed(title=embed_title, timestamp=discord.utils.utcnow(), color=embed_color)


        fields = 0
        
        departures = [departure for departure in departures if get_route_name(departure['route_id']) == line or line == "all"]

        
        for departure in departures:
            # print(f'Departure: {departure}')
            route_id= departure['route_id'] 
            scheduled_departure_utc = departure['scheduled_departure_utc']
            if isPast(scheduled_departure_utc, final_time):
                # print(f"time in past")
                pass
            else:
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
                    
                # get live departure time
                if mode == "0":
                    stoppingPattern=getStoppingPattern(run_ref, mode)
                    delay = 0
                    for stop in stoppingPattern:
                        if stop[0].strip() == station.title():
                            scheduled_departure_utc = stop[1] 
                            # Calculate delay in minutes
                            delay = (convert_times(stop[1]) - convert_times(stop[3])) // 60  # Convert time difference to minutes
                            if delay > 0:
                                delaystring = f'{delay} minutes late'
                            else:
                                delaystring = ''
                        else:
                            delaystring = ''
                else:
                    delaystring = ''
                
                # get the direction for busses and trams and also the route number
                if mode in ['1', '2']:
                    route_number = routes[str(route_id)]['route_number']
                    direction = getDirectionName(runs[run_ref]['direction_id'])     
                
                # train emoji
                # trainType = getEmojiForDeparture(trainType)
                
                # Convert PTV run REF to TDN
                if run_ref.startswith('9') and mode == '0':
                    TDN = RunIDtoTDN(run_ref)
                else:
                    TDN = run_ref

                #convert to timestamp
                depTime=convert_iso_to_unix_time(scheduled_departure_utc)
                #get route name:
                route_name = get_route_name(route_id)
                
                # get the train type from the number
                if mode == "0":
                    print(f'Train number: {trainNumber}')
                    trainType, trainNumber = await cleanAPITrainNumber(trainNumber)       
                    print(f'Train type: {trainType}')         
                
                # thing for stony point
                if route_name == "Stony Point":
                    trainType = "Sprinter"
                    if station.title() == "Frankston":
                        platform_number = "3"
                    else:
                        platform_number = "1"
                if mode == '0':
                    embed.add_field(name=f"{getlineEmoji(route_name)}\n{desto} {note if note else ''}", value=f"\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')}) {delaystring}\nPlatform {platform_number}\n{trainType} {trainNumber}\nTDN: `{TDN}`")
                elif mode in ['1', '2']: 
                    embed.add_field(name=f"{route_number} to {desto}", value=f"\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nRun `{run_ref}`") 
                elif mode == '3':
                    embed.add_field(name=f"dsddsds", value=f"\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nRun `{run_ref}`")
                    
                fields = fields + 1
                if fields == 9:
                    break
        # add message for no depatures
        if fields == 0:
            embed.add_field(name="No departures found", value="There are currently no departures for this stop.")
        
        # disruptions:
        disruptions = getStationDisruptions(stop_id)
        for disruption in disruptions:
            # Truncate disruption title if its ling
            title = disruption['title']
            if len(title) > 200:
                title = title[:200] + "..."
            
            embed.insert_field_at(index=0, name=f"<:Disruption:1322444175941173280> {title}", 
                                value=f"[{disruption['description']}]({disruption['url']})\n", inline=False)
        # get station image
        if mode == '0' or mode == '3':
            image = getStationImage(station)
            if image != None: 
                embed.set_thumbnail(url=image)  
                embed.set_footer(text=f"V/Line departures are unavailable | Photo by {getPhotoCredits(station)}")       
            else:
                embed.set_footer(text=f"V/Line departures are unavailable")
        
        try:
            await ctx.edit_original_response(embed=embed, content='')     
        except Exception as e:
            await ctx.edit_original_response(content=f'Error loading departures. Please try again later.\n```{e}```')
            await printlog(f'ErROR: {e}') 
            await printlog(traceback.format_exc())  
    
    asyncio.create_task(nextdeps(stop, time))
    
    
# ptv api search command
@search.command(name="ptv", description="Search stops, routes and myki ticket outlets provided by PTV")
@app_commands.describe(search="What to search for")
@app_commands.choices(type=[
        app_commands.Choice(name="stops", value="stops"),
        app_commands.Choice(name="routes", value="routes"),
        app_commands.Choice(name="myki outlets", value="myki")
])
@app_commands.describe(maximum_responses="How many responses for each mode of transport you want")
async def search(ctx, search:str, type:str, maximum_responses:int=3):
    async def ptvsearch(search):
        await ctx.response.defer()
        log_command(ctx.user.id, 'ptv-search')
        fmtSearch = search.replace(" ", "%20")
        data = search_api_request(fmtSearch)
        if type == 'stops':
            if data['stops']:
                embed = discord.Embed(title=f"Results for {search}:")
                train_count = 0
                vline_count = 0
                tram_count = 0
                bus_count = 0
                coach_count = 0
                train_list = []
                vline_list = []
                tram_list = []
                bus_list = []
                coach_list = []
                train_embed = f""
                vline_embed = f""
                tram_embed = f""
                bus_embed = f""
                coach_embed = f""
                for stop in data['stops']:
                    stop_name = stop['stop_name']
                    stop_id = stop['stop_id']
                    stop_suburb = stop['stop_suburb']
                    route_type = stop['route_type']
                    # find emojis for the route type
                    if route_type == 3:
                        emoji = getVlineStopType(stop_name, True)
                    else:
                        emoji = getModeEmoji(route_type)
                    url = f'https://www.ptv.vic.gov.au/stop/{stop_id}'

                    if emoji == "<:train:1241164967789727744>" and train_count < maximum_responses:
                        train_count +=1
                        train_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on PTV website]({url})\n")                    
                    elif emoji == "<:vline:1241165814258729092>" and vline_count < maximum_responses:
                        vline_count +=1
                        vline_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on PTV website]({url})\n")
                    elif emoji == "<:tram:1241165701390012476>" and tram_count < maximum_responses:
                        tram_count +=1
                        tram_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on PTV website]({url})\n")
                    elif emoji == "<:bus:1241165769241530460>" and bus_count < maximum_responses:
                        bus_count +=1
                        bus_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on PTV website]({url})\n")
                    elif emoji == "<:coach:1241165858274021489>" and coach_count < maximum_responses:
                        coach_count +=1
                        coach_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on PTV website]({url})\n")
                
                if train_count != 0:
                    for train in train_list:
                        train_embed = f"{train_embed}{train}"
                    embed.add_field(name="<:train:1241164967789727744> Train", value=f"{train_embed}\n\n", inline=False)

                if vline_count != 0:
                    for vline in vline_list:
                        vline_embed = f"{vline_embed}{vline}"
                    embed.add_field(name="<:vline:1241165814258729092> V/Line", value=f"{vline_embed}\n\n", inline=False)

                if tram_count != 0:
                    for tram in tram_list:
                        tram_embed = f"{tram_embed}{tram}"
                    embed.add_field(name="<:tram:1241165701390012476> Tram", value=f"{tram_embed}\n\n", inline=False)

                if bus_count != 0:
                    for bus in bus_list:
                        bus_embed = f"{bus_embed}{bus}"
                    embed.add_field(name="<:bus:1241165769241530460> Bus", value=f"{bus_embed}\n\n", inline=False)

                if coach_count != 0:
                    for coach in coach_list:
                        coach_embed = f"{coach_embed}{coach}"

                    embed.add_field(name="<:coach:1241165858274021489> Coach", value=f"{coach_embed}\n\n", inline=False)
                embed.set_footer(text="Tip: You can save a stop to your favourites with /favourites add <stop>")
                
            else:
                embed = discord.Embed(title=f"Results for {search}:")
                embed.add_field(name="No stops found", value="Try searching for something else")
                
        elif type == 'routes':
            if data['routes']:
                embed = discord.Embed(title=f"Results for {search}:")
                train_count = 0
                vline_count = 0
                tram_count = 0
                bus_count = 0
                coach_count = 0
                train_list = []
                vline_list = []
                tram_list = []
                bus_list = []
                coach_list = []
                train_embed = f""
                vline_embed = f""
                tram_embed = f""
                bus_embed = f""
                coach_embed = f""
                for route in data['routes']:
                    route_name = route['route_name']
                    route_id = route['route_id']
                    route_number = route['route_number'] + " - " if route['route_number'] else ""
                    route_service_status = route['route_service_status']['description']
                    url = f'https://www.ptv.vic.gov.au/route/{route_id}'
                    emoji = getModeEmoji(route['route_type'])

                    if emoji == "<:train:1241164967789727744>" and train_count < maximum_responses:
                        train_count +=1
                        train_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on PTV website]({url})\n")                    
                    elif emoji == "<:vline:1241165814258729092>":
                        if route_id in vline_rail_lines and vline_count < maximum_responses:
                            vline_count +=1
                            vline_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on PTV website]({url})\n")
                        if coach_count < maximum_responses:
                            coach_count +=1
                            coach_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on PTV website]({url})\n")
                    elif emoji == "<:tram:1241165701390012476>" and tram_count < maximum_responses:
                        tram_count +=1
                        tram_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on PTV website]({url})\n")
                    elif emoji == "<:bus:1241165769241530460>" and bus_count < maximum_responses:
                        bus_count +=1
                        bus_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on PTV website]({url})\n")
                
                if train_count != 0:
                    for train in train_list:
                        train_embed = f"{train_embed}{train}"
                    embed.add_field(name="<:train:1241164967789727744> Train", value=f"{train_embed}\n\n", inline=False)

                if vline_count != 0:
                    for vline in vline_list:
                        vline_embed = f"{vline_embed}{vline}"
                    embed.add_field(name="<:vline:1241165814258729092> V/Line", value=f"{vline_embed}\n\n", inline=False)

                if tram_count != 0:
                    for tram in tram_list:
                        tram_embed = f"{tram_embed}{tram}"
                    embed.add_field(name="<:tram:1241165701390012476> Tram", value=f"{tram_embed}\n\n", inline=False)

                if bus_count != 0:
                    for bus in bus_list:
                        bus_embed = f"{bus_embed}{bus}"
                    embed.add_field(name="<:bus:1241165769241530460> Bus", value=f"{bus_embed}\n\n", inline=False)

                if coach_count != 0:
                    for coach in coach_list:
                        coach_embed = f"{coach_embed}{coach}"
                    embed.add_field(name="<:coach:1241165858274021489> Coach", value=f"{coach_embed}\n\n", inline=False)
            else:
                embed = discord.Embed(title=f"Results for {search}:")
                embed.add_field(name="No routes found", value="Try searching for something else")
                
        elif type == 'myki':
            if data['outlets']:
                embed = discord.Embed(title=f"Results for {search}:")
                count = 0
                for outlet in data['outlets']:
                    buisness = outlet['outlet_business']
                    suburb = outlet['outlet_suburb']
                    url = generate_google_maps_link(outlet['outlet_latitude'], outlet['outlet_longitude']) 
                    embed.add_field(name=f"{buisness} - {suburb}", value=f'[View on Google Maps]({url})',inline=False)
                    count +=1
                    if count == maximum_responses:
                        break
            else:
                embed = discord.Embed(title=f"Results for {search}:")
                embed.add_field(name="No routes found", value="Try searching for something else")
                
        try:
            await ctx.edit_original_response(embed=embed)
        except Exception as e:
            await printlog('Too many characters because "maximum_responses" was set to high.')
            await ctx.edit_original_response(content='''"maximum_responses" set too high, try a lower number. If you're using the myki outlet mode, the maximum is 25.''')
            return
    asyncio.create_task(ptvsearch(search))
        



# Montague Bridge search
'''@bot.tree.command(name="days-since-montague-hit", description="See how many days it has been since the Montague Street bridge has been hit.")
async def train_line(ctx):
    await ctx.response.send_message(f"Checking...")
    channel = ctx.channel
    
    embed = discord.Embed(title=f"How many days since the Montague Street bridge has been hit?", color=tram_colour)
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
@app_commands.describe(rounds = "The number of rounds. Defaults to 1, max 100.", line='Select a line to only show photos from that line', ultrahard = "Ultra hard mode.")
@app_commands.choices(line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Flemington Racecourse", value="Flemington Racecourse"),
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
        app_commands.Choice(name="Williamstown", value="Williamstown"),
])
async def game(ctx,rounds: int = 1, line:str='all', ultrahard: bool=False):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-guesser')
    async def run_game(): 

        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 500:
            await ctx.response.send_message("You can only play a maximum of 500 rounds!", ephemeral=True )
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

        # Filter data by line if a specific line is selected
        if line != 'all':
            try:
                line_stations = lines_dictionary_main[line][0]
                filtered_data = []
                for row in data:
                    if row[1] in line_stations:  # Check if station is in the line's station list
                        filtered_data.append(row)
                data = filtered_data
            except KeyError:
                await ctx.response.send_message(f"Invalid line selected: {line}")
                return

        ignoredRounds = 0
        setLine = 'All Lines' if line == 'all' else f'{line.title()} line'

        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []
        
        # Get the photos at start and shuffle them
        try:
            available_photos = data.copy()
            random.shuffle(available_photos)
            
            if len(available_photos) < rounds:
                await ctx.response.send_message(f'Not enough photos available for {rounds} rounds. Maximum available is {len(available_photos)}.')
                channel_game_status[channel] = False
                return
            
        except IndexError:
            await ctx.response.send_message('There are currently no photos for your selected options! Try a different line.')
            channel_game_status[channel] = False
            return

        for round in range(rounds):
            roundResponse = False
            
            # Get the next photo from the shuffled list
            random_row = available_photos[round]

            # Extract data from the random row
            url = random_row[0]
            station = random_row[1] 
            difficulty = random_row[2]
            credit = random_row[3]

            if ultrahard:
                embed = discord.Embed(title=f"Guess the station! | {setLine}", color=ultrahard_colour, description=f"Type ! before your answer. You have 30 seconds to answer.\n\n**Difficulty:** `{difficulty.upper()}`")
            else:
                embed = discord.Embed(title=f"Guess the station! | {setLine}", description=f"Type ! before your answer. You have 30 seconds!\n\n**Difficulty:** `{difficulty}`")
                if difficulty == 'Very Easy':
                    embed.color = very_easy_colour
                elif difficulty == 'Easy':
                    embed.color = easy_colour
                elif difficulty == 'Medium':
                    embed.color = medium_colour
                elif difficulty == 'Hard':
                    embed.color = hard_colour
                elif difficulty == 'Very Hard':
                    embed.color = very_hard_colour
            
            embed.set_image(url=url)
            embed.set_footer(text=f"Photo by {credit}. DM @xm9g to submit a photo | {len(data)} photos in set")
            embed.set_author(name=f"Round {round+1}/{rounds}")

            # Send the embed message
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            async def check(m):
                return m.channel == channel and m.author != bot.user and m.content.startswith('!')
            async def funnyCheck(m):    
                return m.channel == channel and m.author != bot.user
            try:
                correct = False
                if ultrahard:
                    gameType = 'ultrahard'
                else:
                    gameType = 'guesser'
                
                
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    if await check(user_response) == True:  # fixed cause check broke
                    
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
                            await printlog(f'Ignored rounds: {ignoredRounds}')
                            if ultrahard:
                                addLb(user_response.author.id, user_response.author.name, 'ultrahard')
                            else:
                                addLb(user_response.author.id, user_response.author.name, 'guesser')
                            if user_response.author not in participants:
                                participants.append(user_response.author)
                                
                        elif user_response.content.lower() == '!skip':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{station.title()}||" if not ultrahard else f"Round {round+1} skipped.")
                                log_command(user_response.author.id, 'game-station-guesser-skip')
                                skippedGames += 1
                                roundResponse = True
                                break
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                                roundResponse = True
                        elif user_response.content.lower() == '!stop':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Game ended.")
                                log_command(user_response.author.id, 'game-station-guesser-stop')
                                embed = discord.Embed(title=f"Game Summary | {setLine}")
                                embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                                embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                                embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                                embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                                await ctx.channel.send(embed=embed)  
                                for user in participants:
                                    await addGameAchievement(user.name,ctx.channel.id,user.mention)  
                                channel_game_status[channel] = False
                                return
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")  
                        
                        # view the image info (admin only) 
                        elif user_response.content.lower() == '!reveal' or user_response.content.lower() == '!release':
                            if user_response.author.id in admin_users :
                                await ctx.channel.send(f"Station Name: `{station}`\nUrl: `{url}`")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only reveal the image if you are an admin.")
                        
                        
                        else:
                            await user_response.add_reaction('❌')
                            log_command(user_response.author.id, 'game-station-guesser-incorrect')
                            roundResponse = True
                            incorrectAnswers += 1
                            if ultrahard:
                                addLoss(user_response.author.id, user_response.author.name, 'ultrahard')
                            else:
                                addLoss(user_response.author.id, user_response.author.name, 'guesser')
                            if user_response.author not in participants:
                                participants.append(user_response.author)
                    
                    # checker for the funnies ( no ! needed)       
                    if await funnyCheck(user_response) == True:
                        # funny ones
                        if 'idk' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'i dont know' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'sorry' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'my bad' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.") 
                        elif 'oops' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'bruh' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} 💀")
                        elif 'shit' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'fuck' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'what' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} its a station.")
                        elif 'wtf' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} what?")
                          
            except asyncio.TimeoutError:
                if ultrahard:
                    await ctx.channel.send(f"Times up. Answers are not revealed in ultrahard mode.")
                else:
                    await ctx.channel.send(f"Times up. The answer was ||{station.title()}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                await printlog(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds >= 4 and roundResponse == False:
                    await ctx.channel.send("No responses for 4 rounds. Game ended.")
                    embed = discord.Embed(title=f"Game Summary | {setLine}")
                    embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                    embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                    embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                    embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                    await ctx.channel.send(embed=embed)  
                    for user in participants:
                        await addGameAchievement(user.name,ctx.channel.id,user.mention)
                    return
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title=f"Game Summary | {setLine}")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
        await ctx.channel.send(embed=embed)  
        for user in participants:
            await addGameAchievement(user.name,ctx.channel.id,user.mention)

    # Run the game in a separate task
    try:
        asyncio.create_task(run_game())
    except Exception as e:
        await printlog(f'GUESSER ERROR: {e}')
        await ctx.channel.send(f'An error has occurred\n```{e}```')
        await log_channel.send(f'Error: ```{e}```\n with guesser run ran by {ctx.user.mention}\n<@{USER_ID}>')



    
@stats.command(name="leaderboard", description="Global leaderboards for the games.",)
@app_commands.describe(game="What game's leaderboard to show?")
@app_commands.choices(game=[
        app_commands.Choice(name="Station Guesser", value="guesser"),
        app_commands.Choice(name="Ultrahard Station Guesser", value="ultrahard"),
        app_commands.Choice(name="Station order game", value="domino"),
        app_commands.Choice(name="Station Hangman", value="hangman"),

])

async def lb(ctx, game:str):
    log_command(ctx.user.id, 'view-leaderboard')
    channel = ctx.channel
    leaders = top5(game)
    if leaders == 'no stats':
        await ctx.response.send_message('There is no data for this game yet!',ephemeral=True) # lol this would never show
        return

    # Create the embed
    embed = discord.Embed(title=f"Top 10 players for {game}", color=discord.Color.gold())
    
    count = 1
    for userid, number, losses in leaders:
        try:
            embed.add_field(name=f'{count}.', value=f'<@{userid}>\nWins: {str(number)}\nLosses: {str(losses)}\nAccuracy: {str(round((number/(number+losses))*100, 1))}%', inline=False)
        except:
            embed.add_field(name=f'{count}.', value=f'<@{userid}>\nWins: {str(number)}\nLosses: {str(losses)}', inline=False)
        count = count + 1
        
    await ctx.response.send_message(embed=embed)


# Station order game made by @domino

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
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", direction = "The directions you are listing the stations in. Defaults to Up or Down.", line ='Which line to guess stations from, defaults to all lines.')
@app_commands.choices(
    direction=[
        app_commands.Choice(name="Up or Down", value='updown'),
        app_commands.Choice(name="Up", value='up'),
        app_commands.Choice(name="Down", value='down')
        ],
    )
@app_commands.choices(line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        # app_commands.Choice(name="Flemington Racecourse", value="Flemington Racecourse"),
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
        app_commands.Choice(name="Williamstown", value="Williamstown"),
])

async def testthing(ctx, rounds: int = 1, direction: str = 'updown', line:str='all'):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-order')
    async def run_game(line):
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 10:
            await ctx.response.send_message("You can only play a maximum of 10 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        ignoredRounds = 0
        setLine = 'All Lines' if line == 'all' else f'{line.title()} line'
        
        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []

        for round in range(rounds):
            roundResponse = False

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
            if line == 'all':
                line = None
                while line == None:
                    line = linelist[random.randint(0,len(linelist)-1)]            

            # choose random station
            if line == 'Flemington Racecourse':
                if numdirection == 5 or numdirection == -5:
                    numdirection = random.choice([-4,-3,-2,2,3,4])
            station = None
            while station == None:
                station = lines_dictionary_main[line][0][random.randint(0,len(lines_dictionary_main[line][0])-1)]
                if not 0 <= lines_dictionary_main[line][0].index(station)+numdirection <= len(lines_dictionary_main[line][0]):
                    station = None

            embed = discord.Embed(
                title=f"Which __**{numdirection if numdirection > 0 else numdirection*-1}**__ stations are __**{direction1}**__ from __**{station}**__ station on the __**{line} line**__?",
                description=f"**Answers must be in the correct order!** Answer using this format:\n!<station1>, <station2>{', <station3>' if numdirection >= 3 or numdirection <= -3 else ''}{', <station4>' if numdirection >= 4 or numdirection <= -4 else ''}{', <station5>' if numdirection >= 5 or numdirection <= -5 else ''}\n\n*Use !skip to skip to the next round.*",
                colour=lines_dictionary_main[line][1])
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            async def check(m): 
                return m.channel == channel and m.author != bot.user and m.content.startswith('!')
            async def funnyCheck(m):    
                return m.channel == channel and m.author != bot.user

            # get list of correct stations
            if numdirection > 0:
                correct_list = lines_dictionary_main[line][0][lines_dictionary_main[line][0].index(station)+1:lines_dictionary_main[line][0].index(station)+numdirection+1]
            else:
                correct_list = lines_dictionary_main[line][0][lines_dictionary_main[line][0].index(station)+numdirection:lines_dictionary_main[line][0].index(station)]
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

                    if await check(user_response) == True:  # fixed cause check broke    
                        # Check if the user's response matches the correct station
                        if response == correct_list1:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it correctly!")
                            addLb(user_response.author.id, user_response.author.name, 'domino')
                            log_command(user_response.author.id, 'game-station-order-correct')
                            correctAnswers += 1
                            ignoredRounds = 0
                            roundResponse = True
                            correct = True 
                        elif user_response.content.lower() == '!skip':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
                                log_command(user_response.author.id, 'game-station-order-skip')
                                skippedGames += 1
                                roundResponse = True
                                break
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                        elif user_response.content.lower() == '!stop':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Game ended.")
                                log_command(user_response.author.id, 'game-station-order-stop')
                                embed = discord.Embed(title=f"Game Summary | {setLine}")
                                embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                                embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                                embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                                embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                                await ctx.channel.send(embed=embed)  
                                for user in participants:
                                    await addGameAchievement(user.name,ctx.channel.id,user.mention)
                                channel_game_status[channel] = False
                                return
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                        # view the image info (admin only) 
                        elif user_response.content.lower() == '!reveal' or user_response.content.lower() == '!release':
                            if user_response.author.id in admin_users :
                                await ctx.channel.send(f"Stations: `{correct_list1}`")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only reveal the image if you are an admin.")
                        else:
                            await user_response.add_reaction('❌')
                            log_command(user_response.author.id, 'game-station-order-incorrect')
                            roundResponse = True
                            incorrectAnswers += 1
                            addLoss(user_response.author.id, user_response.author.name, 'domino')
                            if user_response.author not in participants:
                                participants.append(user_response.author)
                
                    # checker for the funnies ( no ! needed)       
                    if await funnyCheck(user_response) == True:
                        # funny ones
                        if 'idk' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'i dont know' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'sorry' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'my bad' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.") 
                        elif 'oops' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'bruh' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} 💀")
                        elif 'shit' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'fuck' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'what' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} its a set of stations.")
                        elif 'wtf' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} what?")
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                await printlog(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds >= 4 and roundResponse == False:
                    await ctx.channel.send("No responses for 4 rounds. Game ended.")
                    embed = discord.Embed(title=f"Game Summary | {setLine}")
                    embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                    embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                    embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                    embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                    await ctx.channel.send(embed=embed)  
                    for user in participants:
                        await addGameAchievement(user.name,ctx.channel.id,user.mention)
                    return
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title=f"Game Summary | {setLine}")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
        await ctx.channel.send(embed=embed)  
        for user in participants:
            await addGameAchievement(user.name,ctx.channel.id,user.mention)
            
    # Run the game in a separate task
    asyncio.create_task(run_game(line))



@games.command(name="station-hangman", description="A game where you guess the letters comprising a station name")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.")
@app_commands.describe(attempts = "The number of wrong guesses allowed. Defaults to 10.")

async def hangman(ctx, rounds: int = 1, attempts: int = 10):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-hangman')
    async def run_game(line):
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 10:
            await ctx.response.send_message("You can only play a maximum of 10 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        ignoredRounds = 0
        line = 'all' # change this when lines are added
        setLine = 'All Lines' if line == 'all' else f'{line.title()} line'
        
        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []

        for round in range(rounds):
            roundResponse = False
            
            # choose random line
            if line == 'all':
                line = None
                while line == None:
                    line = linelist[random.randint(0,len(linelist)-1)]            

            # choose random station
            station = ""
            while station == "":
                station = lines_dictionary_main[line][0][random.randint(0,len(lines_dictionary_main[line][0])-1)]

            guessed_list = ""
            guessed = ""
            for letter in station.replace(" ", ""):
                guessed = guessed + "- "

            failed = f""

            incorrectGuesses = 0

            embed = discord.Embed(
                title=f"Guess the station! It has {len(station)} letters",
                description=f"**Guess either letters or station names.\nNote you only have {attempts} incorrect guesses until you lose**\nAnswer using this format:\n!<Letter> or !<Station name or part of station name>\n\n*Use !skip to skip to the next round.*",
                colour=metro_colour)
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            async def check(m): 
                return m.channel == channel and m.author != bot.user and m.content.startswith('!')
            async def funnyCheck(m):    
                return m.channel == channel and m.author != bot.user

            # the actual input part
            try:
                correct = False
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)

                    if await check(user_response) == True:  # fixed cause check broke    
                        # Check if the user's response matches the correct station
                        if user_response.content[1:].lower().replace(" ", "") in station.lower().replace(" ", ""):
                            if not user_response.content[1:].lower().replace(" ", "") in guessed_list:
                                guessed_list = guessed_list + user_response.content[1:].lower().replace(" ", "") # this is obviously broken, will be funny to see tho
                                await printlog(guessed_list)
                                guessed = ""
                                for letter in station.replace(" ", ""):
                                    if letter.lower() in guessed_list:
                                        guessed = guessed + letter + " "
                                    else:
                                        guessed = guessed + "- "
                                await user_response.add_reaction('✅')
                                addLb(user_response.author.id, user_response.author.name, 'hangman')
                                log_command(user_response.author.id, 'game-station-hangman-correct')
                                correctAnswers += 1
                                ignoredRounds = 0
                                roundResponse = True
                                if guessed.replace(" ", "") == station.replace(" ", ""):
                                    correct = True
                                    await ctx.channel.send("You won!")
                                await ctx.channel.send(f'# Letters: {guessed}\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                            else:
                                await ctx.channel.send(f'Already guessed {user_response.author.mention}! Try again.')
                                log_command(user_response.author.id, 'game-station-hangman-neutral')
                                roundResponse = True
                                if user_response.author not in participants:
                                    participants.append(user_response.author)
                                await ctx.channel.send(f'# Letters: {guessed}\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                        elif user_response.content.lower() == '!skip':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{station}||")
                                log_command(user_response.author.id, 'game-station-hangman-skip')
                                skippedGames += 1
                                roundResponse = True
                                break
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                        elif user_response.content.lower() == '!stop':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Game ended.")
                                log_command(user_response.author.id, 'game-station-hangman-stop')
                                embed = discord.Embed(title=f"Game Summary | {setLine}")
                                embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                                embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                                embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                                embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                                await ctx.channel.send(embed=embed)  
                                for user in participants:
                                    await addGameAchievement(user.name,ctx.channel.id,user.mention, game='hangman')
                                channel_game_status[channel] = False
                                return
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                        # view the image info (admin only) 
                        elif user_response.content.lower() == '!reveal' or user_response.content.lower() == '!release':
                            if user_response.author.id in admin_users :
                                await ctx.channel.send(f"Station: `{station}`")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only reveal the image if you are an admin.")
                        else:
                            if not user_response.content[1:].lower().replace(" ", "") in failed:
                                await user_response.add_reaction('❌')
                                log_command(user_response.author.id, 'game-station-hangman-incorrect')
                                roundResponse = True
                                incorrectAnswers += 1
                                incorrectGuesses += 1
                                addLoss(user_response.author.id, user_response.author.name, 'hangman')
                                if len(user_response.content[1:].lower().replace(" ", "")) == 1:
                                    if failed == "":
                                        failed = user_response.content[1:].lower().replace(" ", "")
                                    else:
                                        failed = failed + f', {user_response.content[1:].lower().replace(" ", "")}'
                                if user_response.author not in participants:
                                    participants.append(user_response.author)
                                await ctx.channel.send(f'# Letters: {guessed}\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                                if incorrectGuesses >= attempts:
                                    await ctx.channel.send('You lost!')
                                    await ctx.channel.send(f"The answer was ||{station}||")
                                    break
                            else:
                                await ctx.channel.send(f'Already guessed {user_response.author.mention}! Try again.')
                                log_command(user_response.author.id, 'game-station-hangman-neutral')
                                roundResponse = True
                                if user_response.author not in participants:
                                    participants.append(user_response.author)
                                await ctx.channel.send(f'# Letters: {guessed}\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')

                
                    # checker for the funnies ( no ! needed)       
                    if await funnyCheck(user_response) == True:
                        # funny ones
                        if 'idk' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'i dont know' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'sorry' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'my bad' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.") 
                        elif 'oops' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'bruh' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} 💀")
                        elif 'shit' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'fuck' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'what' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} its station.")
                        elif 'wtf' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} what?")
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{station}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                await printlog(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds >= 4 and roundResponse == False:
                    await ctx.channel.send("No responses for 4 rounds. Game ended.")
                    embed = discord.Embed(title=f"Game Summary | {setLine}")
                    embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                    embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                    embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                    embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                    await ctx.channel.send(embed=embed)  
                    for user in participants:
                        await addGameAchievement(user.name,ctx.channel.id,user.mention, game='hangman')
                    return
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title=f"Game Summary | {setLine}")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
        await ctx.channel.send(embed=embed)  
        for user in participants:
            await addGameAchievement(user.name,ctx.channel.id,user.mention, game='hangman')
            
    # Run the game in a separate task
    asyncio.create_task(run_game(line))

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
    
async def type_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = types_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
#log train logger
@trainlogs.command(name="train", description="Log a train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', type='Type of train (will be autofilled if a train number is entered)', notes='Any notes you want to add to the log', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.autocomplete(type=type_autocompletion)

# Train logger
async def logtrain(ctx, line:str, number:str, start:str, end:str, date:str='today', type:str='auto', notes:str=None, hidemessage:bool=False):
    channel = ctx.channel
    await ctx.response.defer(ephemeral=hidemessage)
    log_command(ctx.user.id, 'log-train')
    await printlog(date)
    async def log(notes, ctx,line, number, start, end, date, type):
        await printlog("logging the thing")

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

        if 'overland' in line.lower():
            await ctx.edit_original_response(content='''If you're trying to log a trip on the Overland, please use </log adelaide-train:1289843416628330506>. For a comprehensive guide of which of these log commands to use in which situation, open </help:1261177133372280957> and in the "commands" option choose "Which /log command should I use?"''')
            return
            
        # Initialize variables
        set = 'Unknown'
        type_final = 'Unknown'

        # Handle type first
        if type != 'auto':
            type_final = type
            if type == "Tait":
                set = '381M-208T-230D-317M'
            else:
                
                # check if its a known train type and find the set, but if its not known just use the number
                checkTT = trainType(number.upper())
                if checkTT == type:
                    set = setNumber(number.upper())
                    if set == None:
                        set = type
                else:
                    set = number.upper()
        else:
            # if the user puts a vlocity with he letters VL
            if number.upper().startswith('VL') and len(number) == 6:
                print('vlocity with vl')
                number = number.strip('VL').replace(' ', '')
            
            # checking if train number is valid
            if number != 'Unknown':
                set = setNumber(number.upper())
            if set == None:
                await ctx.edit_original_response(content=f'Invalid train number: `{number.upper()}`')
                return
            type_final = trainType(number.upper())
            
        # Strip emojis and newlines from notes if provided
        if notes:
            # Remove emojis using regex
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            # Remove newlines
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'
                
            
        # Add train to the list
        print(f'adding {set} {type_final} {savedate} {line} {start.title()} {end.title()} {notes}')
        id = addTrain(ctx.user.name, set, type_final, savedate, line, start.title(), end.title(), notes, ctx.user.id)
        
        if line in vLineLines:
            embed = discord.Embed(title="Train Logged",colour=vline_map_colour)
        elif line == 'Unknown':
                embed = discord.Embed(title="Train Logged")
        else:
            try:
                embed = discord.Embed(title="Train Logged",colour=lines_dictionary_main[line][1])
            except:
                embed = discord.Embed(title="Train Logged")
        
        embed.add_field(name="Set", value=f'{set} ({type_final})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        if getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), start, end) != 'N/A':
            embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}, {round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), start, end), 1)}km')
        else:
            embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        if notes:
            embed.add_field(name="Notes", value=notes.strip('"'))

        # thing to find image:
        await printlog(f"Finding image for {number}")
        if type_final == 'Tait':
            image = 'https://railway-photos.xm9g.net/photos/317M-6.webp'
        
        try:
            if not '-' in set:
                image = getImage(set)

            else:
                hyphen_index = set.find("-")
                if hyphen_index != -1:
                    first_car = set[:hyphen_index]
                    await printlog(f'First car: {first_car}')
                    image = getImage(first_car)
                    if image == None:
                        last_hyphen = set.rfind("-")
                        if last_hyphen != -1:
                            last_car = set[last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                            await printlog(f'Last car: {last_car}')
                            image = getImage(last_car)
                            if image == None:
                                image = getImage(type_final)
                                await printlog(f'the loco number is: {set}')
            if image != None:
                embed.set_thumbnail(url=image)
            
        except Exception as e:
            await printlog(f"Error getting image: {e}")

        embed.set_footer(text=f"Log {id}")
        
        
        
        await ctx.edit_original_response(embed=embed)
        await addAchievement(ctx.user.name, ctx.channel.id, ctx.user.mention)

        
                        
    # Run in a separate task
    asyncio.create_task(log(notes,ctx,line, number, start, end, date, type))

    
#thing to delete the stuff
@trainlogs.command(name='delete', description='Delete a logged trip. Defaults to the last logged trip.')
@app_commands.describe(id = "The ID of the log that you want to delete.", mode='What mode of log to delete?')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Train", value="train"),
    app_commands.Choice(name="Melbourne Tram", value="tram"), 
    app_commands.Choice(name="NSW Train", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Train", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Tram", value="adelaide-trams"),
    app_commands.Choice(name="Perth Train", value="perth-trains"),
    app_commands.Choice(name="Bus", value="bus"),
])
async def deleteLog(ctx, mode:str, id:str='LAST'):
    class DeleteConfirmation(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your log!", ephemeral=True)
                return
            
            # Delete the log
            idformatted1 = deleteRow(ctx.user.name, idformatted, mode)
            
            # Update message
            if idformatted == 'LAST':
                await interaction.response.edit_message(content=f'Most recent log (`#{idformatted1}`) deleted. The data was:\n`{dataToDelete}`', view=None)
            else:
                await interaction.response.edit_message(content=f'Log `#{idformatted}` deleted. The data was:\n`{dataToDelete}`', view=None)
                
            for child in self.children:
                child.disabled = True
                
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your log!", ephemeral=True)
                return
            
            await interaction.response.edit_message(content="Deletion cancelled.", view=None)
            for child in self.children:
                child.disabled = True

    async def deleteLogFunction():
        log_command(ctx.user.id, 'log-delete')
        
        nonlocal idformatted, dataToDelete  # Make these accessible in button callbacks
        
        if id[0] == '#':
            idformatted = id[1:].upper()
        else:
            idformatted = id.upper()

        if idformatted != 'LAST':
            if not is_hex(idformatted):
                await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </log view:1289843416628330506>.', ephemeral=True)
                return
                
        dataToDelete = universalReadRow(ctx.user.name, idformatted, mode)
        if dataToDelete in ['no data at all', 'no data for user']:
            await ctx.response.send_message(f'You have no logs you can delete!', ephemeral=True)
            return
        elif dataToDelete == 'invalid id did not show up':
            await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </log view:1289843416628330506>.', ephemeral=True)
            return
        
        else:
            # Create confirmation message with buttons
            view = DeleteConfirmation()
            if idformatted == 'LAST':
                await ctx.response.send_message(f'Are you sure you want to delete your most recent log?\nData to be deleted:\n`{dataToDelete}`', view=view, ephemeral=True)
            else:
                await ctx.response.send_message(f'Are you sure you want to delete log `#{idformatted}`?\nData to be deleted:\n`{dataToDelete}`', view=view, ephemeral=True)
            
    # Initialize variables for button callbacks
    idformatted = None  
    dataToDelete = None
    
    asyncio.create_task(deleteLogFunction())
    
# log editor
@trainlogs.command(name='edit',description='Edit a logged trip')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Train", value="train"),
    # coming soon:
    # app_commands.Choice(name="Melbourne Tram", value="tram"),
    # app_commands.Choice(name="NSW Train", value="sydney-trains"),
    # app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    # app_commands.Choice(name="Adelaide Train", value="adelaide-trains"),
    # app_commands.Choice(name="Adelaide Tram", value="adelaide-traMS"),
    # app_commands.Choice(name="Perth Train", value="perth-trains"),
    # app_commands.Choice(name="Bus", value="bus"),
])
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.autocomplete(type=type_autocompletion)
async def editrow(ctx, id:str, mode:str='train', line:str='nochange', number:str='nochange', start:str='nochange', end:str='nochange', date:str='nochange', type:str='auto', notes:str='nochange'):
    await ctx.response.defer()
    log_command(ctx.user.id, 'edit-row')
    
    username = ctx.user.name
    logid = id
    if logid[0] == '#':
        idformatted = logid[1:].upper()
    else:
        idformatted = logid.upper()
    
    # Find old data for the edited row
    dataToDelete = universalReadRow(username, idformatted, mode)
    
    if notes != 'nochange':
            # Remove emojis using regex
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            # Remove newlines
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'
            
    # convert date from DD/MM/YYYY to YYYY-MM-DD
    if date != 'nochange':
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use the format DD/MM/YYYY.')
                return
            except TypeError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nUse the form `dd/mm/yyyy`')
                return
    else:
        savedate = 'nochange'
    
    result = editRow(username, idformatted, mode,line,number,start,end,savedate,type,notes)
    
    if result == 'invalid id did not show up':
        await ctx.edit_original_response(content=f'Invalid log ID entered: `{idformatted}`')
        return
    
    
    await ctx.edit_original_response(content=f'**Successfully edited log `#{idformatted}`**\nOld data:\n`{dataToDelete}`\nNew data:\n`{result}`')

    
  # tram logger goes here
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = tram_stops.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
@trainlogs.command(name="tram", description="Log a Melbourne tram you have been on")
@app_commands.describe(number = "Tram Number", date = "Date in DD/MM/YYYY format", route = 'Tram Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
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

async def logtram(ctx, route:str, number: str, start:str, end:str, date:str='today', notes:str=None, hidemessage:bool=False):
    await ctx.response.defer(ephemeral=hidemessage)
    channel = ctx.channel
    await printlog(date)
    async def log(notes):
        log_command(ctx.user.id, 'log-tram')
        await printlog("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.edit_original_response(f'Invalid date: {date}\nMake sure to use a possible date.')
                return
            except TypeError:
                await ctx.edit_original_response(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`')
                return

        # checking if train number is valid
        if set == None:
            await ctx.edit_original_response(f'Invalid tram number: {number.upper()}')
            return
        type = tramType(number.upper())
        if type == None or type == 'Tram type not found for UNKNOWN':
            type = 'N/A'
            
        if notes != None:
            # Remove emojis using regex
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            # Remove newlines
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'

        # Add train to the list
        id = addTram(ctx.user.name, number, type, savedate, route, start.title(), end.title(), notes)

        embed = discord.Embed(title="Tram Logged",colour=tram_colour)
        
        embed.add_field(name="Number", value=f'{number} ({type})')
        embed.add_field(name="Line", value=route)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        if notes != None:
            embed.add_field(name="Notes", value=notes.strip('"'))
        embed.set_footer(text=f"Log ID #{id}")

        # thing to find image:
        await printlog(f"Finding image for {number}")
        image = getTramImage(number)
        if image != None:
            embed.set_thumbnail(url=image)

        await ctx.edit_original_response(embed=embed)
        
                
    # Run in a separate task
    asyncio.create_task(log(notes))
    
    
    
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
@app_commands.describe(number = "Carrige Number", type = 'Type of train', date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', hidemessage='Hide the message from other users, note this will not make the log private.')
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
async def logNSWTrain(ctx,  line:str, number: str, type:str,start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    async def log():
        log_command(ctx.user.id, 'log-nsw-train')
        await printlog("logging the nsw sydney train")

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

        embed = discord.Embed(title="Train Logged",colour=sydney_train_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
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
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=Adelaidestation_autocompletion)
@app_commands.autocomplete(end=Adelaidestation_autocompletion)
@app_commands.autocomplete(line=Adelaideline_autocompletion)

# Adelaide train logger journey beyond too
async def logSATrain(ctx, line:str, number: str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    log_command(ctx.user.id, 'log-adelaide-train')
    await printlog(date)
    async def log():
        await printlog("logging the adelaide train")

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

        embed = discord.Embed(title="Train Logged",colour=adelaide_metro_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed)
        await addAchievement(ctx.user.name, ctx.channel.id, ctx.user.mention)

                
    # Run in a separate task
    asyncio.create_task(log())


# Adelaide tram logger
async def Adelaidestop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Adelaidestops_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

@trainlogs.command(name="adelaide-tram", description="Log a Adelaide Tram you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Tram Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=Adelaidestop_autocompletion)
@app_commands.autocomplete(end=Adelaidestop_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="Glenelg to Royal Adelaide Hospital Line", value="GLNELG"),
        app_commands.Choice(name="Botanic Gardens to Entertainment Centre Line", value="BTANIC"),
        app_commands.Choice(name="Glenelg to Festival Plaza Line", value="FESTVL"),
        app_commands.Choice(name="Adelaide Loop Line", value="ADLOOP"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="100 Series", value="100 Series"),
        app_commands.Choice(name="200 Series", value="200 Series"),
])
# SYdney tram logger nsw tram
async def logSATram(ctx, line:str, number: str, type:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    async def log():
        log_command(ctx.user.id, 'log-adelaide-tram')
        await printlog("logging the adelaide tram")

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
            await ctx.response.send_message(f'Invalid tram number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addAdelaideTram(ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Tram Logged",colour=adelaide_tram_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
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
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=Perthstation_autocompletion)
@app_commands.autocomplete(end=Perthstation_autocompletion)
@app_commands.autocomplete(line=Perthline_autocompletion)

# Perth logger
async def logPerthTrain(ctx, number: str, line:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    log_command(ctx.user.id, 'log-perth-train')
    await printlog(date)
    async def log():
        await printlog("logging the perth train")

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
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        
        try:
            if 201 <= int(number) <=248:
                type = 'A-Series'
            elif 301 <= int(number) <=348:
                type = 'A-Series'
            elif 4049 <= int(number) <=4126:
                type = 'B-Series'
            elif 6049 <= int(number) <=6126:
                type = 'B-Series'
            elif 5049 <= int(number) <=5126:
                type = 'B-Series'
            elif int(str(number)[-3:]) >= 126:
                type = 'C-Series'
            else:
                type = 'Unknown'
        except:
            type = 'Unknown'
        
        # Add train to the list
        id = addPerthTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Train Logged",colour=transperth_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log())


async def NSWstop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = NSWstops_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

@trainlogs.command(name="sydney-tram", description="Log a Sydney Tram/Light Rail you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Light Rail Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=NSWstop_autocompletion)
@app_commands.autocomplete(end=NSWstop_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="L1 Dulwich Hill Line", value="L1"),
        app_commands.Choice(name="L2 Randwick", value="L2"),
        app_commands.Choice(name="L3 Kingsford Line", value="L3"),
        app_commands.Choice(name="L4 Westmead and Carlingford Line", value="L4"),
        app_commands.Choice(name="NLR Newcastle Light Rail", value="NLR"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="Urbos 3", value="Urbos 3"),
        app_commands.Choice(name="Citadis 305", value="Citadis 305"),
])
# SYdney tram logger nsw tram
async def logNSWTram(ctx, line:str, number: str, type:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    async def log():
        log_command(ctx.user.id, 'log-nsw-tram')
        await printlog("logging the sydney tram")

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

        embed = discord.Embed(title="Tram Logged",colour=sydney_tram_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
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

async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = bus_coach_stops.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="bus", description="Log a Bus you have been on")
@app_commands.describe(number = "Bus number", type = 'Type of bus', date = "Date in DD/MM/YYYY format", line = 'bus route', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(operator=busOpsautocompletion)
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)

async def logBus(ctx, line:str, number: str, start:str, end:str, operator:str='Unknown', date:str='today', type:str='Unknown', notes:str=None, hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    async def log(notes):
        log_command(ctx.user.id, 'log-bus')
        await printlog("logging the bus")

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
        
        # format notes so it dosnt break anything
        if notes:
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            notes = notes.replace('\n', ' ')
            # notes = f'"{notes}"'

        # Add bus to the list
        id = addBus(ctx.user.name, set, type, savedate, line, start.title(), end.title(), operator.title(), notes)

        embed = discord.Embed(title="Bus Logged",colour=bus_colour)
        
        embed.add_field(name="Operator", value=operator)
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        if notes != None:
            embed.add_field(name="Notes", value=notes)
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log(notes))



# train logger reader log view
vLineLines = ['Geelong','Warrnambool', 'Ballarat', 'Maryborough', 'Ararat', 'Bendigo','Echuca', 'Swan Hill','Albury', 'Seymour', 'Shepparton', 'Traralgon', 'Bairnsdale']

@trainlogs.command(name="view", description="View logged trips for a user")
@app_commands.describe(user = "Who do you want to see the data of?", mode = 'Train or tram logs?',id='Leave blank to show all logs')
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="train"),
        app_commands.Choice(name="Melbourne Trams", value="tram"),
        app_commands.Choice(name="Bus", value="bus"),
        app_commands.Choice(name="NSW Trains", value="sydney-trains"),
        app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
        app_commands.Choice(name="Adelaide Trains & Journey Beyond", value="adelaide-trains"),
        app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
        app_commands.Choice(name="Perth Trains", value="perth-trains"),

])
@app_commands.choices(send=[
        app_commands.Choice(name="Web (Victorian Train only)", value="web"),
        app_commands.Choice(name="Thread", value="thread"),
])

async def userLogs(ctx, mode:str='train', user: discord.User=None, id:str=None, send:str='web'):
    async def sendLogs():
        log_command(ctx.user.id, 'view-log')
        
        if mode == 'train' and id == None and send == 'web':
            await ctx.response.send_message('[Click here to view your logs online](https://trackpulse.xm9g.net/logs/viewer)', ephemeral=False)
            return
        
        if user == None:
                userid = ctx.user
        else:
            userid = user
            
        if userid != ctx.user and ctx.user.id not in admin_users:
            await ctx.response.send_message('You cannot view other users logs.', ephemeral=True)
            return
            
        if mode == 'train':
            file_path = 'userdata/trainlogs.db'
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
        if mode == 'adelaide-trams':
            file_path = f'utils/trainlogger/userdata/adelaide-trams/{userid.name}.csv' 
        if mode == 'perth-trains':
            file_path = f'utils/trainlogger/userdata/perth-trains/{userid.name}.csv'   
        
        if id != None:
            # Connect to SQLite database
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            # Query the database
            cursor.execute("""
                SELECT log_id, set_number, train_type, date, line, start, end, notes
                FROM logs
                WHERE log_id = ? AND user_id = ?
            """, (id.upper(),userid.id))
            
            row = cursor.fetchone()

            if row:
                # Extract row data
                og_id, set_number, train_type, date, line, start, end, notes = row

                # Find image
                image = None
                if train_type == 'Tait':
                    image = 'https://railway-photos.xm9g.net/photos/317M-6.webp'
                
                if not '-' in set_number:
                    image = getImage(set_number)
                else:
                    hyphen_index = set_number.find("-")
                    if hyphen_index != -1:
                        first_car = set_number[:hyphen_index]
                        await printlog(f'First car: {first_car}')
                        image = getImage(first_car)
                        if image == None:
                            last_hyphen = set_number.rfind("-")
                            if last_hyphen != -1:
                                last_car = set_number[last_hyphen + 1:]
                                await printlog(f'Last car: {last_car}')
                                image = getImage(last_car)
                                if image == None:
                                    image = getImage(train_type)
                                    await printlog(f'the loco number is: {set_number}')
                
                if image == None:
                    await printlog(f"Finding image for {train_type.replace('-Class','')}.{set_number}")
                    image = getTramImage(f'{train_type.replace("-Class","")}.{set_number}')

                # Create the embed
                if line in vLineLines:
                    embed = discord.Embed(title=f"Log {og_id}", colour=vline_map_colour)
                elif line == 'Unknown':
                    embed = discord.Embed(title=f"Log {og_id}")
                else:
                    try:
                        embed = discord.Embed(title=f"Log `{og_id}`", colour=lines_dictionary_main[line][1])
                    except:
                        embed = discord.Embed(title=f'Log `{id}`')
                
                embed.add_field(name='Set', value=f"{set_number} ({train_type})")
                embed.add_field(name='Line', value=f"{line}")
                embed.add_field(name='Date', value=f"{date}")
                embed.add_field(name='Trip', value=f"{start} to {end}")
                
                if start != 'N/A' and end != 'N/A':
                    distance = getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), start, end)
                    if distance != 'N/A':
                        embed.add_field(name='Distance:', value=f'{round(distance)}km')
                
                if notes:
                    embed.add_field(name='Notes:', value=notes.strip('"'))
                
                try:
                    embed.set_thumbnail(url=image)
                except:
                    await printlog('no image')
                
                await ctx.response.send_message(embed=embed)
            else:
                # If no row is found with the id
                await ctx.response.send_message(f'Cannot find log `{id}`')

            # Close the database connection
            conn.close()
                
        else:
            # Connect to SQLite database
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
           
            # for train
            if mode == 'train':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                # read the db to see if theres any robs
                cursor.execute("SELECT log_id, set_number, train_type, date, line, start, end, notes FROM logs WHERE user_id = ?", (userid.id,))
                data = cursor.fetchall()
                
                if not data:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!", ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!", ephemeral=True)
                    conn.close()
                    return
                
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
                embed=discord.Embed(title='Train Logs', colour=vline_colour)
                embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
                embed.add_field(name='Click here to view your logs:', value=f'<#{logsthread.id}>')
                embed.add_field(name='Click here to view your own logs on the website:', value=f'[Trackpulse Vic Website](https://discord.com/oauth2/authorize?client_id=1214144664513417218&redirect_uri=https%3A%2F%2Ftrackpulse.xm9g.net%2Flogs%2Fviewer&response_type=code&scope=identify)')
                await ctx.response.send_message(embed=embed)
                # await logsthread.send(f'# <:train:1241164967789727744> {userid.name}\'s CSV file', file=file)
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
                                await printlog(f'First car: {first_car}')
                                image = getImage(first_car)
                                if image == None:
                                    last_hyphen = sublist[1].rfind("-")
                                    if last_hyphen != -1:
                                        last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                                        await printlog(f'Last car: {last_car}')
                                        image = getImage(last_car)
                                        if image == None:
                                            image = getImage(sublist[2])
                                            await printlog(f'the loco number is: {sublist[1]}')
                                        
                        #send in thread to reduce spam!
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=vline_colour)
                        elif sublist[4] == 'Unknown':
                                embed = discord.Embed(title=f"Log `{sublist[0]}`")
                        else:
                            try:
                                embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=lines_dictionary_main[sublist[4]][1])
                            except:
                                embed = discord.Embed(title=f"Log {sublist[0]}")
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        if sublist[5] != 'N/A' and sublist[6] != 'N/A':
                            if getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]) != 'N/A':
                                embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km')
                        if sublist[7]:
                            embed.add_field(name='Notes:', value=sublist[7].strip('"'))
                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            await printlog('no image')
                        
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
                await printlog(userid.name)
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
                await logsthread.send(f' # <:tram:1241165701390012476> {userid.name}\'s Tram Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=vline_colour)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=tram_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        if len(sublist) >= 8:
                            embed.add_field(name='Notes:', value=sublist[7].strip('"'))
                        # embed.set_thumbnail(url=image)

                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            await printlog('no image')

                        await logsthread.send(embed=embed)
                        time.sleep(1)
            
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
                await printlog(userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=sydney_tram_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(1) 
            
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
                await printlog(userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=vline_colour)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=sydney_train_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(1)     
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
                await printlog(userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=adelaide_metro_colour)
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Number', value="{} ({})".format(sublist[1], sublist[2]))
    
                        await logsthread.send(embed=embed)
                        time.sleep(0.7)

            # for adelaide tram:
            if mode == 'adelaide-trams':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/adelaide-trams/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readAdelaideTramLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Adelaide Tram Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Tram Logs')
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=adelaide_tram_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(1) 

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
                await printlog(userid.name)
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
                await logsthread.send(f'# <:transperthtrain:1335396329798631477><:TransWA:1335397360255373392> {userid.name}\'s Perth Train Logs')
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=transperth_colour)
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Number', value="{} ({})".format(sublist[1], sublist[2]))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(1)  
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
                await printlog(userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=bus_colour)
                        embed.add_field(name=f'Route', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Operator', value="{}".format(sublist[7]))
                        embed.add_field(name=f'Bus Number', value="{} ({})".format(sublist[1], sublist[2]))
                        if len(sublist) > 8:
                            embed.add_field(name='Notes:', value=sublist[8].strip('"'))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(1) 
            # Close the database connection
            conn.close() 
    asyncio.create_task(sendLogs())

# log export
@trainlogs.command(name='export', description='Export your logs in various formats')
@app_commands.choices(format=[
    app_commands.Choice(name="CSV file (Excel)", value="csv"),
    app_commands.Choice(name="Markdown file", value="md"),
    app_commands.Choice(name="XML file", value="xml"),
    app_commands.Choice(name='HTML file',value='html')
])
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Trains", value="train"),
    app_commands.Choice(name="Melbourne Trams", value="tram"),
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="New South Wales Trains", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Trains", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),
])
async def export(ctx, format:str, mode:str, hidemessage:bool=False):
    try:
        await logExport(ctx, format, mode, hidemessage)
    except FileNotFoundError as e:
        await ctx.response.send_message(f'You have no logs for that mode!')
    except Exception as e:
        await ctx.response.send_message(f"Error: `{e}`")
        
# log import
@trainlogs.command(name='import', description='Import your logs from a CSV file')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Trains", value="train"),
    app_commands.Choice(name="Melbourne Trams", value="tram"), 
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="New South Wales Trains", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Trains", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),
])
async def importlogs(ctx, mode:str, file:discord.Attachment):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'import-log')

    class ImportConfirmation(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            
        @discord.ui.button(label="Confirm Import", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your commend!", ephemeral=True)
                return
            
            try:
                # Download the file
                await file.save(f'temp/{file.filename}')
                if not file.filename.endswith('.csv'):
                    await interaction.response.edit_message(content="Invalid file format! Make sure you're uploading a CSV file.", view=None)
                    return
                
                # Validate CSV format
                with open(f'temp/{file.filename}', 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) < 7:  # Basic validation - ensure minimum columns
                            await interaction.response.edit_message(content="Invalid CSV format! Make sure you're uploading a valid log file.", view=None)
                            return
                
                # Copy to user's log file
                if mode == 'train':
                    save_path = f'utils/trainlogger/userdata/{ctx.user.name}.csv'
                else:
                    save_path = f'utils/trainlogger/userdata/{mode}/{ctx.user.name}.csv'
                    
                shutil.copy(f'temp/{file.filename}', save_path)
                
                await interaction.response.edit_message(content=f"Successfully imported logs for {mode} from `{file.filename}`", view=None)
                
            except Exception as e:
                await interaction.response.edit_message(content=f"Error importing logs: {str(e)}", view=None)
            finally:
                # Cleanup temp file
                try:
                    os.remove(f'temp/{file.filename}') 
                except:
                    pass
                
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your import!", ephemeral=True)
                return
            
            await interaction.response.edit_message(content="Import cancelled.", view=None)

    # Create confirmation message with buttons
    view = ImportConfirmation()
    await ctx.edit_original_response(
        content=f"Are you sure you want to import logs for **{mode}** from `{file.filename}`?\n⚠️ This will overwrite any existing logs you have for this mode.", 
        view=view
    )

# train log stats
@trainlogs.command(name="stats", description="View stats for a logged user's trips.")
@app_commands.describe(stat='Type of stats to view', user='Who do you want to see the data of?', format='Diffrent ways and graphs for showing the data.', mode='Train or Tram logs?', year='Filter by year', global_stats='View global stats?')
@app_commands.choices(stat=[
    app_commands.Choice(name="Lines", value="lines"),
    app_commands.Choice(name="Stations", value="stations"),
    app_commands.Choice(name="Trips", value="pairs"),
    app_commands.Choice(name="Trip Length (Vic train only)", value="length"),
    app_commands.Choice(name='Distance over time (Vic train only)', value='distanceovertime'),
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
    app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),

])
async def statTop(ctx: discord.Interaction, stat: str, mode:str, format: str='l&g', global_stats:bool=False, user: discord.User = None, year:int=0):
    async def sendLogs():
        await ctx.response.defer()
        log_command(ctx.user.id, 'log-stats')
        statSearch = stat
        userid = user if user else ctx.user
        
        if userid.name == 'comeng_17':
            name = 'comeng17'
        else:
            name = userid
            # 
        if user != None:
            if user != ctx.user and ctx.user.id not in admin_users:
                print(f'user {user} is not the same as {ctx.user}')
                await ctx.followup.send('You can only view your own stats!')
                return
            
        if global_stats:
            data = globalTopStats(statSearch)
        else:
            try:
                if stat == 'operators':
                    data = topOperators(userid.name)
                elif stat == 'length':
                    data = getLongestTrips(userid.name)  
                elif stat == 'distanceovertime':
                    data = distanceOverTime(userid.name, year)
                elif mode == 'all':
                    data = allTopStats(userid.name, statSearch, year)
                else:
                    data = topStats(userid.name, statSearch, year, mode)
                
            except:
                await ctx.followup.send('You have no logged trips!')
        count = 1
        message = ''
        
        # top operators thing:
        if stat == 'operators':
            try:
                pieChart(data, f'Top Operators ― {name}', ctx.user.name)
                await ctx.followup.send(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.followup.send('User has no logs!')  
                
        # length
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
                    await ctx.followup.send(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")

                # send reponse message
                pfp = userid.avatar.url
                embed=discord.Embed(title=f"{userid.name}'s longest trips in Victoria", colour=metro_colour)
                embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
                embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
                await ctx.followup.send(embed=embed)
                
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
                    time.sleep(0.7)
                
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
                await log_channel.send(f'Error: ```{e}```\n with trip length run ran by {ctx.user.mention}\n<@{USER_ID}>')
            finally:
                return
        
        # distance over time
        if stat == 'distanceovertime':
            distanceChart(data, name)
            await ctx.followup.send(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
                
        # make temp csv
        csv_filename = f'temp/top{stat.title()}.{userid}-t{time.time()}.csv'
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)  # Use csv.writer on csv_file, not csvs
            for item in data:
                station, times = item.split(': ')
                writer.writerow([station, times.split()[0]])
        
        if format == 'csv':
            try:
                await ctx.followup.send("Here is your file:", file=discord.File(csv_filename))
            except:
                await ctx.followup.send('You have no logs!')
            
        elif format == 'l&g':
            # create thread
            try:
                logsthread = await ctx.channel.create_thread(
                    name=stat.title(),
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
            except Exception as e:
                await ctx.followup.send(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
                
            # send reponse message
            pfp = userid.avatar.url
            embed=discord.Embed(title=stat.title(), colour=metro_colour)
            embed.set_author(name=userid.name, url='https://railway-photos.xm9g.net', icon_url=pfp)
            embed.add_field(name='Click here to view your stats:', value=f'<#{logsthread.id}>')
            await ctx.followup.send(embed=embed)
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
            except FileNotFoundError:
                await logsthread.send(f'User has no logs! {e}')
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
                
        elif format == 'pie':
            try:
                if global_stats:
                    pieChart(csv_filename, f'Top {stat.title()} ― {name}', ctx.user.name)
                else:
                    pieChart(csv_filename, f'Top {stat.title()} ― Global', ctx.user.name)

                await ctx.followup.send(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except FileNotFoundError:
                await ctx.followup.send('You have no logs!')
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
                
        elif format == 'daily':
            if stat != 'dates':
                await ctx.followup.send('Daily chart can only be used with the stat set to Top Dates')
            try:
                dayChart(csv_filename, ctx.user.name)
                await ctx.followup.send(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except FileNotFoundError:
                ctx.followup.send('User has no logs!')
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
    await sendLogs()

@stats.command(name='termini', description='View which line termini you have been to')
async def termini(ctx):
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-termini')
    try:
        data =terminiList(ctx.user.name)
    except:
        data = 'No logs found'
    
    
    if len(data) <= 2000:
        embed = discord.Embed(title=f'Line termini {ctx.user.name} has visited', colour=metro_colour, description=data)
        await ctx.edit_original_response(embed=embed)
        return
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
    app_commands.Choice(name="Summary", value="summary"),
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
    trainTypes = ["X'Trapolis 100", "Comeng", 'Siemens Nexas', 'HCMT', 'VLocity', 'Sprinter', 'N Class']
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-sets')
    
    # summary:
    if train == 'summary':
        embed = discord.Embed(title=f'{userid.name}\'s set completion summary', colour=metro_colour)
        for train in trainTypes:
            try:
                data = setlist(ctx.user.name, train, summary=True)
                embed.add_field(name=f'{getTrainTypeEmoji(train)} {train}', value=data, inline=True)
            except:
                await ctx.edit_original_response(content='No logs found!')
                return
        embed.set_footer(text='Choose a train type to see which sets you have been on.')
        await ctx.edit_original_response(embed=embed)
        return
    # specific traim
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
    embed=discord.Embed(title=f'{train} sets {userid.name} has been on', colour=metro_colour)
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
    app_commands.Choice(name="Western Australia", value="Western Australian"),
])
async def sets(ctx, state:str):
    userid = ctx.user
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-stations')
    try:
        data =stationlist(ctx.user.name, state)
    except Exception as e:
        await ctx.edit_original_response(content='No logs found')
        await printlog(f'ERROR: {e}')
        
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
    embed=discord.Embed(title=f'{state} stations {userid.name} has been to', colour=metro_colour)
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
@app_commands.choices(photofor=[
    app_commands.Choice(name="Railway Photo & Bot train search", value="website"),
    app_commands.Choice(name="Bot/Website Station Photo Guessing Game", value="guesser"),
    app_commands.Choice(name="Both", value="both"),

])
async def submit(ctx: discord.Interaction, photo: discord.Attachment, date: str, location: str, photofor:str, number: str=''):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'submit-photo')
    async def submitPhoto():
        # see if they diddnt put a car number
        if photofor == 'website' and number == '':
            await ctx.edit_original_response(content="Please provide the number for the train in the photo.")
            return
        
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
                    await channel.send(f'# Photo submitted for {photofor} by <@{ctx.user.id}>:\n- Number {number}\n- Date: {date}\n- Location: {location}\n<@780303451980038165> ', file=file) # type: ignore
                    
                    # publically send embed
                    embed = discord.Embed(title='Photo Submission', 
                      description=f'Photo submitted by <@{ctx.user.id}> for {photofor}:\n- Number {number}\n- Date: {date}\n- Location: {location}')
                    file = discord.File(f"./photo-submissions/{photo.filename}", filename=f'{photo.filename}')
                    embed.set_image(url=f"attachment://{photo.filename}")
                    await public_channel.send(embed=embed, file=file) # type: ignore
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
                userid =ctx.user.id
                pfp = ctx.user.avatar.url
            else:
                username = user.name
                userid =user.id
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
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
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


        # adelaide tram Logger
            try:
                lines = topStats(username, 'lines', 0, 'adelaide-trams')
                stations = topStats(username, 'stations', 0, 'adelaide-trams')
                sets = topStats(username, 'sets', 0, 'adelaide-trams')
                trains = topStats(username, 'types', 0, 'adelaide-trams')
                dates = topStats(username, 'dates', 0, 'adelaide-trams')
                trips = topStats(username, 'pairs', 0, 'adelaide-trams')
                
                #other stats stuff:
                eDate =lowestDate(username, 'adelaide-trams')
                LeDate =highestDate(username, 'adelaide-trams')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed.add_field(
        name='<:adelaidetram:1357271311021379644> Adelaide Tram Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Tram Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(username, "adelaide-trams")}'
    )

                                    
            except FileNotFoundError:
                embed.add_field(name="<:adelaidetram:1357271311021379644> Adelaide Tram Log Stats", value=f'{username} has no logged trips in Adelaide!')

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
        name='<:transperthtrain:1335396329798631477><:TransWA:1335397360255373392> Perth Train Log Stats:',
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
                embed.add_field(name="<:transperthtrain:1335396329798631477><:TransWA:1335397360255373392> Perth Train Log Stats", value=f'{username} has no logged trips in Perth!')
            
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
        name='<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:transperthbus:1335396307510235217><:Canberra_Bus:1264885650826465311> Bus Log Stats:',
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
                embed.add_field(name="<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:transperthbus:1335396307510235217><:Canberra_Bus:1264885650826465311> Bus Log Stats", value=f'{username} has no logged bus trips!')

            
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
            if stats[3] != 'no stats':
                item, wins, losses = stats[3]
                embed.add_field(name=':grey_question: Station Hangman', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
            else:
               embed.add_field(name=':grey_question: Station Hangman', value='No data',inline=False)
            
            # other stats
            try:
                embed.set_footer(text=f"favourite command: {getFavoriteCommand(userid)[0]}")
            except FileNotFoundError:
                await printlog('user has no commands used')
            
            await ctx.edit_original_response(embed=embed)
            
        await profiles()
        
    except Exception as e:
        await ctx.edit_original_response(content = f"Error: `{e}`")

# map view command
@maps.command(name='view', description='View the maps the bot uses')
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="time_based_variants/log_train_map_pre_munnel.png"),
        app_commands.Choice(name="Victorian Trains after the Metro Tunnel opens", value="time_based_variants/log_train_map_post_munnel.png"),
        app_commands.Choice(name="Sydney Trains", value="log_sydney-train_map.png"),
        app_commands.Choice(name="NSW Intercity Trains", value="log__sydney-train__map.png"),
        app_commands.Choice(name="NSW Regional and Interstate Trains", value="log___sydney-train___map.png"),
        app_commands.Choice(name="NSW Light Rail", value="log_sydney-tram_map.png"),
])
async def viewMaps(ctx, mode: str):
    await ctx.response.defer()
    log_command(ctx.user.id,'map-view')
    try:
        uncompressed = Image.open(f'utils/trainlogger/map/{mode}')
        legended = legend(uncompressed,f'utils/trainlogger/map/legends/{mode}')
        compressed = compress(legended)
        compressed.save('temp/themap.png')
        file=discord.File('temp/themap.png', filename='map.png')
        if mode == "time_based_variants/log_train_map_pre_munnel.png":
            embed = discord.Embed(title=f"Map of the network covered by </log train:1289843416628330506>", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(1002449671224041502)
            pfp = user.avatar.url
            embed.set_author(name="Map by Comeng17", icon_url=pfp)
            await printlog(f"Retrieved /log train map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "time_based_variants/log_train_map_post_munnel.png":
            embed = discord.Embed(title=f"Future map of the network covered by </log train:1289843416628330506>", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network. This is the map that will be used once the Metro Tunnel opens.")
            user = await bot.fetch_user(1002449671224041502)
            pfp = user.avatar.url
            embed.set_author(name="Map by Comeng17", icon_url=pfp)
            await printlog(f"Retrieved future /log train map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log_sydney-train_map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-train:1289843416628330506> (Sydney Metropolitan Network only)", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved Sydney Trains map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log__sydney-train__map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-train:1289843416628330506> (NSW Intercity Network only)", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved NSW Intercity map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log___sydney-train___map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-train:1289843416628330506> (NSW Regional and Interstate Network only)", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved NSW Regional map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log_sydney-tram_map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-tram:1289843416628330506>", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved NSW Light Rail for {ctx.user.name} in {ctx.channel.mention}")
        embed.set_image(url="attachment://map.png")
        embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
        await ctx.followup.send(embed=embed, file=file)
    except Exception as e:
        await printlog(e)

# map trip command maps trips 
@maps.command(name='trips', description="View a map of all the trips you've logged")
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="time_based_variants/log_train_map_pre_munnel.png"),
        app_commands.Choice(name="Victorian Trains after the Metro Tunnel opens", value="time_based_variants/log_train_map_post_munnel.png"),
        # app_commands.Choice(name="NSW Light Rail", value="log_sydney-tram_map.png"),
])
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.choices(train=[
        app_commands.Choice(name="All", value="all"),
        app_commands.Choice(name="EDI Comeng", value="EDI Comeng"),
        app_commands.Choice(name="Alstom Comeng", value="Alstom Comeng"),
        app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
        app_commands.Choice(name="HCMT", value="HCMT"),
        app_commands.Choice(name="Siemens", value="Siemens Nexas"),
        app_commands.Choice(name="VLocity", value="VLocity"),
        app_commands.Choice(name="N Class", value="N Class"),
        app_commands.Choice(name="Sprinter", value="Sprinter"),
])
async def mapstrips(ctx,mode: str="time_based_variants/log_train_map_pre_munnel.png",line: str='All', train:str='all', year: int=0, user: discord.Member=None,):
    await ctx.response.defer()
    log_command(ctx.user.id, 'maps-trips')
    await printlog(f"Making trip map for {str(ctx.user.id)}")

    async def generate_map():
        if user == None:
            username = ctx.user.name
            target_user = ctx.user.name
        else:
            username = user.name
            target_user = user.name

        if mode == "time_based_variants/log_train_map_pre_munnel.png":
            modeName = 'vic'
            try:
                await asyncio.to_thread(logMap, target_user, lines_dictionary_log_train_map_pre_munnel, mode, line, year, 'vic', train)
            except FileNotFoundError:
                await ctx.followup.send(f'{"You have" if user == None else username + " has"} no logs!')
                return
            except Exception as e:
                await ctx.followup.send(f'An error occurred while generating the map:\n```{e}```')
                print(f'Error generating map for {username}:\n```{str(e)}\n\n{traceback.format_exc()}```\n<@{USER_ID}>')
                return
            # Send the map once generated
            try:
                # make nameextras string
                nameextras = ''
                if train != 'all' and year != 0:
                    nameextras = f' for {train} trains in {year}'
                elif train != 'all':
                    nameextras = f' for ' + train.strip("\'")
                elif year != 0:
                    nameextras = f' in {year}'
                if line != 'All':
                    nameextras += f' on the {line} line'
                
                file = discord.File(f'utils/trainlogger/userdata/maps/{username}-{modeName}-{year}-{train}-{line}.png', filename='map.png')
                line_str = '' if line == 'All' else f' on the {line} Line'
                year_str = '' if year == 0 else f' in {str(year)}'
                imageURL = f"https://trackpulse.xm9g.net/logs/map?img={username}-{modeName}-{year}-{train.replace(' ', '%20')}-{line.replace(' ', '%20')}&name={username}%27s%20Victorian%20train%20map{nameextras.replace(' ', '%20')}"
                embed = discord.Embed(title=f"Map of logs with </log train:1289843416628330506> for @{username}{nameextras}", 
                                    color=0xb8b8b8, 
                                    description=f"[Click here to view in your browser]({imageURL})")
                embed.set_image(url="attachment://map.png")
                user_pic = await bot.fetch_user(1002449671224041502)
                pfp = user_pic.avatar.url
                embed.set_author(name="Map by Comeng17", icon_url=pfp)
                embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
                await ctx.followup.send(embed=embed, file=file)
            except Exception as e:
                await ctx.followup.send(f'Error sending map:\n```{e}```')
        
        if mode == "time_based_variants/log_train_map_post_munnel.png":
            modeName = 'vic-metrotunnel'
            try:
                await asyncio.to_thread(logMap, target_user, lines_dictionary_log_train_map_post_munnel, mode, line, year, 'vic-metrotunnel')
            except FileNotFoundError:
                await ctx.followup.send(f'{"You have" if user == None else username + " has"} no logs!')
                return
            except Exception as e:
                await ctx.followup.send(f'Error:\n```{e}```')
                return
            # Send the map once generated
            try:
                file = discord.File(f'utils/trainlogger/userdata/maps/{username}-{modeName}.png', filename='map.png')
                line_str = '' if line == 'All' else f' on the {line} Line'
                year_str = '' if year == 0 else f' in {str(year)}'
                imageURL = f'https://trackpulse.xm9g.net/logs/map?img={username}-{modeName}&name={username}\'s%20Victorian%20train%20map%20post%20Metro%20Tunnel'
                embed = discord.Embed(title=f"Post Metro Tunnel Map of logs with </log train:1289843416628330506> for @{username}{year_str}{line_str}", 
                                    color=0xb8b8b8, 
                                    description=f"[Click here to view in your browser]({imageURL})")
                embed.set_image(url="attachment://map.png")
                user_pic = await bot.fetch_user(1002449671224041502)
                pfp = user_pic.avatar.url
                embed.set_author(name="Map by Comeng17", icon_url=pfp)
                embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
                await ctx.followup.send(embed=embed, file=file)
            except Exception as e:
                await ctx.followup.send(f'Error sending map:\n```{e}```')
        
        if mode == "log_sydney-tram_map.png":
            modeName = 'sydney-tram'
            try:
                await asyncio.to_thread(logMap, target_user, lines_dictionary_log_sydney_tram_map, mode, line, year, 'sydney-tram')
            except FileNotFoundError:
                await ctx.followup.send(f'{"You have" if user == None else username + " has"} no logs!')
                return
            except Exception as e:
                await ctx.followup.send(f'Error:\n```{e}```')
                return
            # Send the map once generated
            try:
                file = discord.File(f'utils/trainlogger/userdata/maps/{username}-{modeName}.png', filename='map.png')
                line_str = '' if line == 'All' else f' on the {line} Line'
                year_str = '' if year == 0 else f' in {str(year)}'
                imageURL = f'https://trackpulse.xm9g.net/logs/map?img={username}-{modeName}&name={username}\'s%20Sydney%20tram%20map'
                embed = discord.Embed(title=f"Map of logs with </log sydney-tram:1289843416628330506> for @{username}{year_str}{line_str}", 
                                    color=0xb8b8b8, 
                                    description=f"THIS MAP IS NOT FINISHED [Click here to view in your browser]({imageURL})")
                embed.set_image(url="attachment://map.png")
                user_pic = await bot.fetch_user(829535993643794482)
                pfp = user_pic.avatar.url
                embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
                embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
                await ctx.followup.send(embed=embed, file=file)
            except Exception as e:
                await ctx.followup.send(f'Error sending map:\n```{e}```')

    # Start the async map generation
    asyncio.create_task(generate_map())

# achievement commands
@bot.command()
async def refreshachievements(ctx):
    log_command(ctx.author.id, 'refresh-achievements')
    response = await ctx.send('Checking for new Achievements...')
    await addAchievement(ctx.author.name,ctx.channel.id, ctx.author.mention)
    new = checkGameAchievements(ctx.author.name)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await ctx.send(f'<@{ctx.author.id}>',embed=embed)

@bot.command()
async def award(ctx, user: discord.User, achievement:int):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'award-achievement')
        await ctx.send(f'Awarding achievement id `{achievement}` to {user.mention}...')
        awardAchievement(user.name, achievement)
        info = getAchievementInfo(str(achievement))
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await user.send(f'<@{user.id}>',embed=embed)   
    else:
        print('User is not an admin, he cannot give achievements') 

    
@achievements.command(name='view', description='View your achievements.')
@app_commands.describe(user="Who's achievements to show?")
async def viewAchievements(ctx, user: discord.User = None):
    await ctx.response.defer()
    log_command(ctx.user.id, 'view-achievements')

    if user is None:
        user = ctx.user

    # Get user's achievements
    user_achievements = {}  # Change to dict to store dates
    filepath = f'utils/trainlogger/achievements/data/{user.name}.csv'
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # Process achievements in pairs (id, date)
                for i in range(0, len(row), 2):
                    if i+1 < len(row):
                        achievement_id = row[i]
                        achievement_date = row[i+1]
                        user_achievements[achievement_id] = achievement_date

    # Get all achievements from master list with dates
    all_achievements = []
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Skip empty rows
                achievement_id = row[0]
                name = row[1] 
                description = row[2]
                has_achievement = achievement_id in user_achievements
                date = user_achievements.get(achievement_id, None) if has_achievement else None
                all_achievements.append((achievement_id, name, description, has_achievement, date))

    # Get all achievements from master list
    all_achievements = []
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Skip empty rows
                achievement_id = row[0]
                name = row[1]
                description = row[2]
                has_achievement = achievement_id in user_achievements
                all_achievements.append((achievement_id, name, description, has_achievement))

    # Calculate percentage
    total_achievements = len(all_achievements)
    achieved = sum(1 for _, _, _, has_achievement in all_achievements if has_achievement)
    percentage = (achieved / total_achievements) * 100 if total_achievements > 0 else 0

    # Split achievements into pages of 10
    pages = [all_achievements[i:i + 10] for i in range(0, len(all_achievements), 10)]
    current_page = 0

    async def get_page_embed(page_num):
        embed = discord.Embed(title=f"{user.name}'s Achievements", description=f"**Progress:** {achieved}/{total_achievements} ({percentage:.1f}%)", color=achievement_colour)
        embed.set_footer(text=f"Page {page_num + 1}/{len(pages)}")
        
        for achievement in pages[page_num]:
            achievement_id, name, description, has_achievement = achievement
            emoji = "✅" if has_achievement else "🔒"
            value = description
            if has_achievement:
                date = user_achievements.get(achievement_id)
                if date != 'unknown':
                    value += f"\nDate earned: {date}"
            embed.add_field(name=f"{emoji} {name}", value=value, inline=False)
        
        return embed
       # Create buttons
    class NavButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=180)

        @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
        async def previous_button(self, interaction: discord.Interaction, _):
            nonlocal current_page
            if current_page > 0:
                current_page -= 1
                await interaction.response.edit_message(embed=await get_page_embed(current_page), view=self)
            else:
                await interaction.response.defer()

        @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
        async def next_button(self, interaction: discord.Interaction, _):
            nonlocal current_page
            if current_page < len(pages) - 1:
                current_page += 1
                await interaction.response.edit_message(embed=await get_page_embed(current_page), view=self)
            else:
                await interaction.response.defer()
      # Send initial embed with buttons
    await ctx.edit_original_response(embed=await get_page_embed(0), view=NavButtons())
   
    
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
        embed_metro = discord.Embed(title=f'<:train:1241164967789727744> Metro Line Status', color=metro_colour, timestamp=discord.utils.utcnow())
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
                await printlog(e)

            color = genColor(description)
            info = f'{description}'
            embed_metro.add_field(name=f'{route_name}', value=f'{statusEmoji(description)} {info}', inline=True)
            statuses.append(description)

    # Process V/Line lines
    # Made by Comeng17
    elif operator == 'vline':
        embed_vline = discord.Embed(title=f'<:vline:1241165814258729092> V/Line Line Status', color=vline_colour, timestamp=discord.utils.utcnow())
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
                await printlog(e)

            color = genColor(disruption_vline)
            info = f'{disruption_vline}'
            embed_vline.add_field(name=f'{route_name}', value=f'{statusEmoji(disruption_vline)} {info}', inline=True)
            statuses.append(disruption_vline)

    try:
        # Send the response after data is processed
        await ctx.edit_original_response(embed=embed_metro if operator == 'metro' else embed_vline)
    except Exception as e:
        await printlog(f'ERROR: {e}')

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
    embed = discord.Embed(title="About", description="TrackPulse Vic is a Discord bot that allows users to log their train, and tram trips in Victoria, New South Wales, South Australia and Western Australia, along with any bus trips. It also provides the ability to get real-time line status updates for Metro Trains Melbourne, upcoming departures from Melbourne stations and the ability to search for information about a specific train, as well as a range of other features.", color=discord.Color.blue())
    embed.add_field(name="Developed by", value="[Xm9G](https://xm9g.net/)\n[Comeng17](https://github.com/Comeng17)", inline=True)
    embed.add_field(name="Contributions by",value='[domino6658](https://github.com/domino6658)\n[AshKmo](https://github.com/AshKmo)\nAperture',inline=True)
    embed.add_field(name='Photos sourced from',value="[XM9G's Victorian Railway Photos](https://railway-photos.xm9g.net/)")
    embed.add_field(name="Data Sources", value="[Public Transport Victoria](https://www.ptv.vic.gov.au/)\n", inline=True)
    embed.add_field(name='Website', value='https://trackpulse.xm9g.net')
    embed.add_field(name='Discord Server', value='https://discord.gg/nfAqAnceQ5')
    embed.add_field(name='Report issues', value='[Report a bug on github](https://github.com/TrackPulse-Vic/TrackPulse-Vic/issues)')
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
            if unix_time < 1764507600:
                await ctx.edit_original_response(content=f"Your {current_year} year in review will be available <t:1732971600:R>.")
                return
                # pass
        try:
        
            embed = discord.Embed(title=f":bar_chart: {ctx.user.name}'s Victorian Trains Year in Review: {year}", color=discord.Color.blue())
            data = year_in_review(f'utils/trainlogger/userdata/{ctx.user.name}.csv', year)
            
            (lilydale_value, ringwood_value), count = data.get("top_pair")
            embed.add_field(name=f"In {year} {ctx.user.name} went on {str(data['total_trips'])} train trips :chart_with_upwards_trend:", value=f"\n**First Trip:** {data['first_trip'][5]} to {data['first_trip'][6]} on {data['first_trip'][3]} :calendar_spiral: \n**Last Trip:** {data['last_trip'][5]} to {data['last_trip'][6]} on {data['last_trip'][3]} :calendar_spiral: \n\n:star: **favourite Trip:** {lilydale_value} to {ringwood_value} - {count} times\n:metro: {vline_metroprecent(ctx.user.name, year)}", inline=False)
            
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
            embed.set_footer(text="Trains Logged with TrackPulse Vic", icon_url="https://xm9g.net/discord-bot-assets/logo.png")

            await ctx.edit_original_response(embed=embed)
            
        except Exception as e:
            await ctx.edit_original_response(embed=discord.Embed(title="Error", description=f"An error occurred while fetching data: {e}"))
        
    asyncio.create_task(yir())

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
                await printlog(f'Error: {e}')
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

# analytics viewer
@bot.command()
async def analytics(ctx,mode: str=None, user: discord.Member=None):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id,'analytics')
        
        if mode == "commands":
            # Dictionary to store total command counts across all users
            total_commands = {}
            folder_path = 'utils/stats/data'
            
            # Process each user's CSV file
            for filename in os.listdir(folder_path):
                if filename.endswith('.csv'):
                    with open(os.path.join(folder_path, filename), 'r') as f:
                        next(f) # Skip header
                        for line in f:
                            command, count = line.strip().split(',')
                            total_commands[command] = total_commands.get(command, 0) + int(count)
            
            # Sort commands by count
            sorted_commands = sorted(total_commands.items(), key=lambda x: x[1], reverse=True)
            
            # Format output
            output = "Top commands across all users:\n"
            for command, count in sorted_commands:
                output += f"{command}: {count}\n"
                
            # Split into chunks if too long
            if len(output) > 2000:
                chunks = [output[i:i+1990] for i in range(0, len(output), 1990)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(output)
        elif mode == 'servers':
            guild_list = []
            total_users = 0
            
            # Get all guilds
            for guild in bot.guilds:
                member_count = len(guild.members)
                total_users += member_count
                guild_list.append(f"{guild.name}: {member_count} members")
            
            # Format output
            output = f"Bot is in {len(bot.guilds)} servers with {total_users} total users:\n"
            output += "\n".join(guild_list)
            
            # Split into chunks if too long
            if len(output) > 2000:
                chunks = [output[i:i+1990] for i in range(0, len(output), 1990)]
                for chunk in chunks:
                    await ctx.send(f"```{chunk}```")
            else:
                await ctx.send(f"```{output}```")
            
        elif user == None:
            all_files = []
            folder_path = 'utils/stats/data'

            command_counts = []
            for filename in os.listdir(folder_path):
                if filename.endswith('.csv'):
                    # Read command counts for this user
                    total_commands = 0
                    with open(os.path.join(folder_path, filename), 'r') as f:
                        next(f) # Skip header
                        for line in f:
                            count = int(line.strip().split(',')[1])
                            total_commands += count
                    
                    command_counts.append((f'<@{filename.strip(".csv")}>', total_commands))
            
            # Sort by number of commands
            command_counts.sort(key=lambda x: x[1], reverse=True)
            
            output = f"{len(command_counts)} users:\n"
            current_chunk = ""
            chunks = []
            
            for user, count in command_counts:
                line = f'{user} - {count} commands\n'
                if len(current_chunk) + len(line) > 1900: 
                    chunks.append(current_chunk)
                    current_chunk = line
                else:
                    current_chunk += line
            
            if current_chunk:
                chunks.append(current_chunk)

            messages = []
            for _ in chunks:
                msg = await ctx.send('...')
                messages.append(msg)

            for i, chunk in enumerate(chunks):
                prefix = output if i == 0 else ""  
                await messages[i].edit(content=prefix + chunk)
            
        else:
            try:
                file = discord.File(f'utils/stats/data/{user.id}.csv')
                await ctx.send(file=file)
            except FileNotFoundError:
                await ctx.send(content=f'No analytics data found for {user.mention}')

# commands to edit the train info database
@bot.tree.command(name="select-train-for-editing", description="Select a line in the train info database to edit.")
async def select_train(ctx, train: str):
    await ctx.response.defer()
    if ctx.user.id in admin_users:
        log_command(ctx.user.id, 'select-train-for-editing')
        with open('utils/trainsets.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    collumheadings = next(reader)
                    found = False
                    for row in reader:
                        if row[0].lower() == train.lower():
                            found = True
                            break
                    if found:
                        await ctx.edit_original_response(content=f"Found the train in the db,\nplease say the new values for each collum in the same format as the above, or say 'cancel' to cancel the edit.\n{collumheadings}\nCopy and pase the message below to make editing easier:")
                        await ctx.channel.send(f"{','.join(row)}")
                        def check(m):
                            return m.author == ctx.user and m.channel == ctx.channel
                        try:
                            msg = await bot.wait_for("message", check=check, timeout=60)
                            if msg.content.lower() == 'cancel':
                                await ctx.channel.send("Edit cancelled.")
                                return
                            new_values = msg.content.split(',')
                            if len(new_values) != len(collumheadings):
                                await ctx.channel.send(f"Incorrect number of values provided. Expected {len(collumheadings)}, got {len(new_values)}.\n**Most likely this is due to there being a comma in the text somewhere, e.g. the date. Please remove this.**")
                                return
                            
                            rows = []
                            with open('utils/trainsets.csv', 'r', newline='', encoding='utf-8') as csvfile:
                                reader = csv.reader(csvfile)
                                collumheadings = next(reader)
                                for row in reader:
                                    rows.append(row)
                            
                            # Find the row to edit and update it
                            for row in rows:
                                if row[0].lower() == train.lower():
                                    for i, value in enumerate(new_values):
                                        row[i] = value.strip()
                                    break
                            
                            # Write the updated data back to the CSV
                            with open('D:\\Billy\\Douments\\Self made programs\\railway-photos-1\\trainsets.csv', 'w', newline='', encoding='utf-8') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(collumheadings)
                                writer.writerows(rows)
                                
                            # push the file to github
                            await ctx.channel.send("Pushing changes to GitHub...")
                            repo_dir = "D:\\Billy\\Douments\\Self made programs\\railway-photos-1"
                            repo = git.Repo(repo_dir)
                            await ctx.channel.send("Pulling from git...")
                            await printlog("Pulling from git...")
                            try:
                                directory = repo_dir
                                directory = git.cmd.Git(directory)
                                try:
                                    directory.stash('save')  # Stash local changes
                                except Exception as e:
                                    await printlog(f"Potential Error during stash save: ```{e}```")
                                try:
                                    directory.pull()
                                except Exception as e:
                                    await ctx.channel.send(f"Error during git pull: {e}")
                                    await printlog(f"Error during git pull: {e}")
                                    return
                                try:
                                    directory.stash('pop')  # Restore stashed changes
                                except Exception as e:
                                    await printlog(f"Potential Error during stash pop: ```{e}```")
                            except Exception as e:
                                await ctx.channel.send(f"Error initializing git: {e}")
                                await printlog(f"Error initializing git: {e}")
                                return

                            try:
                                repo.git.add('trainsets.csv')
                                repo.git.commit('-m', f'Updated train info for {train} via bot by {ctx.user.name}')
                            except Exception as e:
                                await ctx.channel.send(f"Error committing changes: {e}")
                                await printlog(f"Error committing changes: {e}")
                                return

                            try:
                                repo.git.push('origin', 'main')
                            except Exception as e:
                                await ctx.channel.send(f"Error pushing changes to GitHub: {e}")
                                await printlog(f"Error pushing changes to GitHub: {e}")
                                return
                            
                            await ctx.channel.send("Train info updated successfully!")
                            await printlog(f"Train info for {train} updated successfully by {ctx.user.name}")
                        except asyncio.TimeoutError:
                            await ctx.channel.send("response timed out. edit cancelled.")
                    else:
                        await ctx.edit_original_response(content=f"Train `{train}` not found in the database. Please check the train number and try again.")
    else:
        await ctx.edit_original_response(content="Only TrackPulse Vic admins can edit the train database. If you think this is a mistake, please joing the TrackPulse Vic server.\nhttps://discord.gg/nfAqAnceQ5")
        await printlog(f'{str(ctx.user.id)} tried to edit the train info database.')

# ping command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert latency to ms
    await ctx.send(f"Pong! Latency: {latency} ms")
    log_command(ctx.author.id, 'ping')
    
@bot.command()
async def syncdb(ctx, url='https://railway-photos.xm9g.net/trainsets.csv'):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'sync-db')
        csv_url = url
        save_location = "utils/trainsets.csv"
        await ctx.send(f"Downloading trainset data from {csv_url} to {save_location}")
        await printlog(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            await download_csv(csv_url, save_location)
            await ctx.send(f"Success!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")
    else:
        await printlog(f'{str(ctx.author.id)} tried to sync the database.')
        await ctx.send("You are not authorized to use this command.")
        
@bot.command()
async def syncgame(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'sync-db')
        csv_url = 'https://railway-photos.xm9g.net/botgames/guesser.csv'
        save_location = "utils/game/images/guesser.csv"
        await ctx.send(f"Downloading guesser data from {csv_url} to {save_location}")
        await printlog(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            await download_csv(csv_url, save_location)
            await ctx.send(f"Success!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")
            
        csv_url = 'https://railway-photos.xm9g.net/botgames/ultrahard.csv'
        save_location = "utils/game/images/ultrahard.csv"
        await ctx.send(f"Downloading ultrahard data from {csv_url} to {save_location}")
        await printlog(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            await download_csv(csv_url, save_location)
            await ctx.send(f"Success!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")
    else:
        await printlog(f'{str(ctx.author.id)} tried to sync the database.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def synclists(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'sync-lists')
        await printlog("Downloading stop name data from PTV")
        await ctx.send("Downloading stop name data from PTV")
        try:
            downloader_function(0)
            await ctx.send("Metro stop data downloaded")
            downloader_function(1)
            await ctx.send("Tram stop data downloaded")
            downloader_function(2)
            await ctx.send("Bus stop data downloaded")
            downloader_function(3)
            await ctx.send("V/Line stop data downloaded")
            await ctx.send("Success!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")

    else:
        await printlog(f'{str(ctx.author.id)} tried to update stop data.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def restart(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'restart')
        await ctx.send(f"Restarting bot")
        await printlog("Restarting bot")
        
        with open('restart.txt', 'w') as file:
            file.write(str(ctx.channel.id))
        await bot.close()
        os.system('python bot.py')

    else:
        await printlog(f'{str(ctx.author.id)} tried to restart the bot.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def update(ctx):
    if automatic_updates == True:
        if ctx.author.id in admin_users:
            log_command(ctx.author.id, 'update')
            await ctx.send("Updating bot...")
            await printlog("Pulling from git...")
        
            try:
                directory = Path(__file__).parents[0]
                directory = git.cmd.Git(directory)
                try:
                    directory.stash('save')  # Stash local changes
                except Exception as e:
                    await printlog(f"Potential Error: ```{e}```")
                directory.pull()
                try:
                    directory.stash('pop')  # Restore stashed changes
                except Exception as e:
                    await printlog(f"Potential Error: ```{e}```")

                await ctx.send("The bot has successfully been updated, restart to apply changes.")
                await printlog('Successfully updated bot')
            except Exception as e:
                await ctx.send(f"Update Failed. Error:\n```{e}```")
                await printlog(f"Update Failed. Error:\n```{e}```")

        else:
            await printlog(f'{str(ctx.author.id)} tried to update the bot.')
            await ctx.send("You are not authorized to use this command.")
    else:
        await ctx.send("Remote updates are not enabled")

@bot.command()
async def convertlogs(ctx):
    if ctx.author.id in admin_users:
        for filename in os.listdir('utils/trainlogger/userdata'):
            if filename.endswith('.csv'):
                username = filename[:-4]
                print(f"Converting logs for user: {username}")
                member = discord.utils.find(lambda m: str(m) == username, ctx.guild.members)
                if member:
                    try:
                        await convertLogsToDB(member.id, username)
                        await ctx.send(f"Converted logs for user {username} ({member.id}).")
                    except Exception as e:
                        await ctx.send(f"Error converting logs for user {username}: {e}")
                else:
                    await ctx.send(f"Couldn't get id for user {username}, skipping conversion.")

        
# thing to notify of errors:
# @bot.event
# async def on_command_error(ctx, error):
#     log_channel = bot.get_channel(STARTUP_CHANNEL_ID)
#     if not isinstance(error, commands.CommandNotFound):
#         await log_channel.send(f"{str(error)}\n<@780303451980038165>")
#         await ctx.channel.send(f"An error occurred: {str(error)}")
        
#     await log_channel.send(f"{str(error)}")

# important
bot.run(BOT_TOKEN)