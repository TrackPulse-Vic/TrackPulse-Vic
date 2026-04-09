import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import random
label_colors = {
    'Lilydale': '#01528b',
    'Belgrave': '#01528b',
    'Glen Waverley': '#01528b',
    'Alamein': '#01528b',
    'Cranbourne': '#00a8e4',
    'Pakenham': '#00a8e4',
    'Hurstbridge': '#d1202f',
    'Mernda': '#d1202f',
    'Craigieburn': '#fdb917',
    'Upfield': '#fdb917',
    'Sunbury': '#00a8e4',
    'Frankston': '#009645',
    'Stony Point': '#009645',
    'Werribee': '#f27fb2',
    'Williamstown': '#f27fb2',
    'Sandringham': '#f27fb2',
    'Flemington Racecourse': '#949797',
    'City Circle': '#313338',
    'Summer Start Metro Tunnel Service': '#00a8e4',
    'N/A': '#949797',
    'Other': '#949797',
    
    'Albury': '#7f3f98',
    'Ballarat': '#7f3f98',
    'Maryborough': '#7f3f98',
    'Ararat': '#7f3f98',
    'Bendigo': '#7f3f98',
    'Echuca': '#7f3f98',
    'Swan Hill': '#7f3f98',
    'Geelong': '#7f3f98',
    'Warrnambool': '#7f3f98',
    'Seymour': '#7f3f98',
    'Shepparton': '#7f3f98',
    'Traralgon': '#7f3f98',     
    'Bairnsdale': '#7f3f98',     
    
    '1': '#b6c527',     
    '3': '#89d1ef',     
    '5': '#e04138',     
    '6': '#004c6d',     
    '11': '#85c5a2',     
    '12': '#008896',     
    '16': '#ffda66',     
    '19': '#8e4b79',     
    '30': '#4f4a9f',     
    '35': '#713c1f',     
    '48': '#434244',     
    '57': '#33bdca',     
    '58': '#83898e',     
    '59': '#4a815a',     
    '64': '#16ab6f',     
    '67': '#ac7963',     
    '70': '#f38bb9',     
    '72': '#9fb5a5',     
    '75': '#009fdb',     
    '78': '#887bb9',     
    '82': '#bdd739',     
    '86': '#feba12',     
    '96': '#e33686',     
    '109': '#f58022',   
     
    'A-Class': '#72bf44', 
    'Z-Class': '#72bf44', 
    'B-Class': '#72bf44', 
    'C-Class': '#72bf44', 
    'E-Class': '#72bf44', 
    'D1-Class': '#72bf44', 
    'D2-Class': '#72bf44', 
    'C2-Class': '#72bf44', 
    'E2-Class': '#72bf44', 

    'Metro': '#008cce',     
    'V/Line': '#7d4295', 
    'Sydney Trains': '#f47a0b',
    'NSW Trainlink': '#e26d23',
    'Yarra Trams': '#72bf44',
    'Sydney Light Rail': '#ed2438',
    'Sydney Metro': '#04959e',
    'Heritage': '#b30303',
    'Adelaide Metro': '#1e3056',
    'Journey Beyond': '#405664',
    'Transperth': '#088a3b',
            
    'Blue Mountains Line': '#f99d1c', 
    'Central Coast & Newcastle Line': '#d11f2f',
    'Hunter Line': '#833134',
    'South Coast Line': '#005aa3',
    'Southern Highlands Line': '#008846',
    'North Coast Region': '#f6891f',
    'North Western Region': '#f6891f',
    'Southern Region': '#f6891f',
    'Western Region': '#f6891f',
    'T1': '#f99d1c',
    'T2': '#0098cd',
    'T3': '#f37021',
    'T4': '#005aa3',
    'T5': '#c4258f',
    'T6': '#7d3f21',
    'T7': '#6f818e',
    'T8': '#00954c',
    'T9': '#c81e2d',
    'Metro North West Line': '#049098',
    'L1': '#ee1f35',
    'L2': '#ee1f35',
    'L3': '#ee1f35',
    
    'Belair': '#509e2f',
    'Gawler': '#c23b33',
    'Grange': '#007dc3',
    'Outer Harbor': '#007dc3',
    'Port Dock': '#007dc3',
    'Seaford': '#fe5000',
    'Flinders': '#fe5000',
    'The Ghan': '#a1233d',
    'Indian Pacific': '#00467c',
    'Great Southern': '#e17f30',
    'The Overland': '#00543d',

    "X'Trapolis 100": '#008cce',
    "EDI Comeng": '#008cce',
    "Alstom Comeng": '#008cce',
    "Siemens Nexas": '#008cce',
    "HCMT": '#008cce',
    "X'Trapolis 2.0": '#008cce',
    'Tait': '#b30303',
    'K Class': '#b30303',

    "N Class": '#7d4296',
    "VLocity": '#7d4296',
    "Sprinter": '#7d4296',

    "Waratah": '#f47913',
    "Tangara": '#f47913',
    "Millennium": '#f47913',
    "OSCAR": '#f47913',
    "A set": '#f47913',
    "B set": '#f47913',
    "V set": '#f47913',
    "D set": '#f47913',
    "K set": '#f47913',
    "Endeavour railcar": '#f47913',
    "Hunter railcar": '#f47913',
    "XPT": '#f47913',
    "Xplorer": '#f47913',
    "Metropolis Stock": '#04959e',
    
    "Urbos 3": '#ed2438',
    "Urbos 100": '#ed2438',
    "Citadis 305": '#ed2438',
    
    # perth lines
    "Fremantle": '#003a79',
    'Midland': "#960048",
    "Armadale": '#f6a800',
    'Yanchep': '#959300',
    'Thornlie': '#f6a800',
    'Mandurah': '#d25f15',
    'Airport': '#44c2b2',
    'Ellenbrook': '#d2222c',
    
    }



def barChart(file_path, dataType, heading, uname, limit=False):
    # Lists to store data from the file
    labels = []
    values = []

    # Read the file and extract data
    with open(file_path, 'r') as file:
        print(f"Reading data from {file_path}")
        data = []
        for line in file:
            parts = line.strip().split(',')
            label = parts[0]
            value = int(parts[1])
            data.append((label, value))

    if limit:
        # Filter out values less than or equal to 5
        filtered_data = [(label, value) for label, value in data if value > 5]

        if len(filtered_data) == 0:
            # if theres nothing abovve 5 then sort all data
            sorted_data = sorted(data, key=lambda item: item[1], reverse=True)
        else:
            sorted_data = sorted(filtered_data, key=lambda item: item[1], reverse=True)

        top_10_data = sorted_data[:10]
        labels, values = zip(*top_10_data) if top_10_data else ([], [])

    else:
        labels, values = zip(*data) if data else ([], [])
    
    colors = [label_colors.get(label, 'white') for label in labels]

    # Create the bar graph
    # plt.xkcd()
    plt.style.use('dark_background')
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=colors)
    plt.xlabel(dataType)
    plt.title(heading)
    plt.xticks(rotation=45, ha='right')
      # only whole numbers
    max_value = max(values)
    plt.yticks(np.arange(0, max_value + 1, step=2))
    plt.tight_layout()

    # sabe  graph
    plt.savefig(f'temp/Graph{uname}.png')
    
def pieChart(file_path, heading, uname):
    # Lists to store data from the file
    labels = []
    values = []

    # Read the file and extract data
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line into label and value
            parts = line.strip().split(',')
            labels.append(parts[0])
            values.append(int(parts[1]))
    
    def get_random_color():
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    colors = [label_colors.get(label, get_random_color()) for label in labels]
    
    plt.style.use('dark_background')
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')  
    plt.title(heading)
    plt.tight_layout()

    # Save the graph
    plt.savefig(f'temp/Graph{uname}.png')
    
def dayChart(csv_file, uname):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, names=['Date', 'Number'])

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Create a new DataFrame with a daily frequency and fill missing values with 0
    daily_df = df.asfreq('D', fill_value=0)

    # Plotting
    plt.style.use('dark_background')  
    plt.figure(figsize=(10, 6))
    plt.plot(daily_df.index, daily_df['Number'], color='cyan')
    plt.xlabel('Date', color='white')
    plt.ylabel('Trips', color='white')
    plt.title(f'Trips per day - {uname}', color='white')
    plt.grid(True, color='gray')
    plt.xticks(rotation=45, color='white')
    plt.tight_layout()
    
    plt.savefig(f'temp/Graph{uname}.png')

def distanceChart(csv_file, uname):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, names=['Date', 'Distance'])

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Plotting
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Distance'], color='cyan', linewidth=2)
    plt.xlabel('Date', color='white')
    plt.ylabel('Distance (km)', color='white')
    plt.title(f'Cumulative Distance', color='white')
    plt.grid(True, color='gray', alpha=0.3)
    plt.xticks(rotation=45, color='white')
    plt.tight_layout()
    
    plt.savefig(f'temp/Graph{uname}.png')