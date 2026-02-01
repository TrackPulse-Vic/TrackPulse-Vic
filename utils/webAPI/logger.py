import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEB_BASE_URL = os.getenv('WEB_BASE_URL')

def logTrip(mode, userid:int, start=None, end=None, line=None, number=None, vType=None, date=None, note=None, tags=None):
    if not WEB_BASE_URL:
        print("WEB_BASE_URL is not set in the environment variables.")
        return 'error'
    
    # format user id
    userid = f'oauth2|discord|{userid}'
    
    data = {
        'mode': mode,
        'userid': userid,
        'start': start,
        'end': end,
        'line': line,
        'number': number,
        'type': vType,
        'date': date,
        'tags': tags
    }
    
    if note != None:
        data['note'] = note

    try:
        response = requests.post(f"{WEB_BASE_URL}/addLog", data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error logging trip: {e}")
        return 'error'
        
    return response.json() if response.status_code == 200 else None
    
def getUserCSV(username, displayName, mode=None, save=True):
    if not WEB_BASE_URL:
        print("WEB_BASE_URL is not set in the environment variables.")
        return 'error'
    
    folder_to_mode = {
        'adelaide-trains': 'satrain',
        'adelaide-trams': 'satram',
        'bus': 'vicbus',  # default to vicbus
        'canberra-trams': 'actlightrail',
        'perth-trains': 'watrain',
        'sydney-trains': 'nswtrain',
        'sydney-trams': 'nswlightrail',
        'tram': 'victram',
        'train': 'victrain'
    }
    if mode in folder_to_mode:
        mode = folder_to_mode[mode]
    
    try:
        response = requests.get(f"{WEB_BASE_URL}/logs.csv", params={'userid': username, 'mode': mode})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving CSV: {e}")
        return 'error'
    
    if save:
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'trainlogger', 'userdata')
        os.makedirs(base_dir, exist_ok=True)
        
        # all the modes
        if mode == 'victrain':
            filename = os.path.join(base_dir, f"{displayName}.csv")
        elif mode == 'victram':
            tram_dir = os.path.join(base_dir, 'tram')
            os.makedirs(tram_dir, exist_ok=True)
            filename = os.path.join(tram_dir, f"{displayName}.csv")
        elif mode == 'satrain':
            satrain_dir = os.path.join(base_dir, 'adelaide-trains')
            os.makedirs(satrain_dir, exist_ok=True)
            filename = os.path.join(satrain_dir, f"{displayName}.csv")
        elif mode == 'satram':
            satram_dir = os.path.join(base_dir, 'adelaide-trams')
            os.makedirs(satram_dir, exist_ok=True)
            filename = os.path.join(satram_dir, f"{displayName}.csv")
        elif mode in ['vicbus', 'nswbus', 'sabus', 'wabus', 'actbus']:
            bus_dir = os.path.join(base_dir, 'bus')
            os.makedirs(bus_dir, exist_ok=True)
            filename = os.path.join(bus_dir, f"{displayName}.csv")
        elif mode == 'nswtrain':
            nswtrain_dir = os.path.join(base_dir, 'sydney-trains')
            os.makedirs(nswtrain_dir, exist_ok=True)
            filename = os.path.join(nswtrain_dir, f"{displayName}.csv")
        elif mode == 'actlightrail':
            actlr_dir = os.path.join(base_dir, 'canberra-trams')
            os.makedirs(actlr_dir, exist_ok=True)
            filename = os.path.join(actlr_dir, f"{displayName}.csv")
        elif mode == 'watrain':
            watrain_dir = os.path.join(base_dir, 'perth-trains')
            os.makedirs(watrain_dir, exist_ok=True)
            filename = os.path.join(watrain_dir, f"{displayName}.csv")
        elif mode == 'nswlightrail':
            nswlr_dir = os.path.join(base_dir, 'sydney-trams')
            os.makedirs(nswlr_dir, exist_ok=True)
            filename = os.path.join(nswlr_dir, f"{displayName}.csv")
              
        
        # Remove the first line (header) from the CSV
        lines = response.text.splitlines()
        csv_content = '\n'.join(lines[1:]) if len(lines) > 1 else ''
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(csv_content)
    # Also return the CSV content without the first line
    lines = response.text.splitlines()
    return '\n'.join(lines[1:]) if response.status_code == 200 and len(lines) > 1 else None

def deleteLogAPI(log_id, userid:int):
    if not WEB_BASE_URL:
        print("WEB_BASE_URL is not set in the environment variables.")
        return 'error'
    
    # format user id
    userid = f'oauth2|discord|{userid}'
    
    data = {
        'id': log_id,
        'userid': userid
    }

    try:
        response = requests.post(f"{WEB_BASE_URL}/deleteLog", data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error deleting log: {e}")
        return 'error'
        
    return response.json() if response.status_code == 200 else None

def getSingleLogID(logId):
    if not WEB_BASE_URL:
        print("WEB_BASE_URL is not set in the environment variables.")
        return 'error'
    
    try:
        response = requests.get(f"{WEB_BASE_URL}/log/{logId}")
        response.raise_for_status()
    except requests.RequestException as e:  
        print(f"Error retrieving log: {e}")
        return 'error'
        
    print(response.json())
    return response.json() if response.status_code == 200 else None