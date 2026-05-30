import requests
import os
import dotenv
dotenv.load_dotenv()

VRP_BASE_URL = os.getenv('VRP_BASE_URL', 'http://victorianrailphotos.com')
# THIS IS DIFFRNT TO THE ONE USED IN THE TRAIN PHOTO COMMAND!
# THIS ONE ONLY RETURNS THE FIRST IMAGE AND ALSO REQUIRS CORRECT FORMATTING!!
def getImage(number, thumbnail=False, mode='train'):
    if mode == 'train':
        apiURL = f"{VRP_BASE_URL}/api/photos/{number}"
    elif mode == 'bus':
        apiURL = f"{VRP_BASE_URL}/api/photos/bus/{number}"
    
    if thumbnail:
        thummy = 'thumbnail'
    else:
        thummy = 'url'
    
    # Make a GET request to fetch the photo data
    try:
        response = requests.get(apiURL)
        if response.status_code != 200:
            return None, None
        
        photos = response.json().get('photos', [])
        
        # featured_photos = [photo for photo in photos if photo.get('featured') == 1]
        
        # if featured_photos:
        #     photo = featured_photos[-1]
        #     photo_url = photo[f'{thummy}']
        #     photographer = photo.get('photographer', 'Unknown')
        #     url_response = requests.head(photo_url)
        #     if url_response.status_code == 200:
        #         return photo_url, photographer
        #     return None, None
        
        if photos:
            photo = photos[-1]
            photo_url = photo[f'{thummy}']
            photographer = photo.get('photographer', 'Unknown')
            url_response = requests.head(photo_url)
            if url_response.status_code == 200:
                return photo_url, photographer
            return None, None
        
        return None, None
    
    except requests.RequestException:
        return None, None
    
    
def getNSWImage(number):
    photo_url = f"{VRP_BASE_URL}/photos/nsw/{number}.webp"

    # Make a HEAD request to check if the photo exists
    URLresponse = requests.head(photo_url)
    if URLresponse.status_code == 200:
        return(photo_url)
    else:
        return(None)
    
    
def getTramImage(number, thumbnail=False):
    apiURL = f"{VRP_BASE_URL}/api/photos/tram/{number}"
    
    if thumbnail:
        thummy = 'thumbnail'
    else:
        thummy = 'url'
    
    # Make a GET request to fetch the photo data
    try:
        response = requests.get(apiURL)
        if response.status_code != 200:
            return None, None
        
        photos = response.json().get('photos', [])
        featured_photos = [photo for photo in photos if photo.get('featured') == 1]
        
        if featured_photos:
            photo = featured_photos[-1]
            photo_url = photo[f'{thummy}']
            photographer = photo.get('photographer', 'Unknown')
            url_response = requests.head(photo_url)
            if url_response.status_code == 200:
                return photo_url, photographer
            return None, None
        
        if photos:
            photo = photos[-1]
            photo_url = photo[f'{thummy}']
            photographer = photo.get('photographer', 'Unknown')
            url_response = requests.head(photo_url)
            if url_response.status_code == 200:
                return photo_url, photographer
            return None, None
        
        return None, None
    
    except requests.RequestException:
        return None, None


def getIcon(type):
    cleaned_type = type.replace(' ', '-').replace("'", '')
    url = f"https://xm9g.net/discord-bot-assets/MPTB/{cleaned_type}.png"
    return(url)

def getStationImage(station):
    type = station.title()
    cleaned_type = type.replace(' ', '%20')
    url = f"{VRP_BASE_URL}/stations/photos/{cleaned_type}.jpg"
    URLresponse = requests.head(url)
    if URLresponse.status_code == 200:
        return(url)

    return(None)

# get VICSIG URL
def vicSigURL(carriageNumber, trainType):
    if trainType == 'VLocity':
        url = f'https://vicsig.net/passenger/railmotor/{carriageNumber}/VLocity'
    elif trainType == 'Sprinter':
        url = f'https://vicsig.net/passenger/railmotor/{carriageNumber}/Sprinter'
    elif trainType == 'N Class':
        url = f'https://vicsig.net/index.php?page=locomotives&number={carriageNumber}&class=N&type=Diesel-Electric&orgstate=V'
        
    else:
        if trainType in ['HCMT', "X'Trapolis 2.0"]:
            url = ''
        if trainType == "X'Trapolis 100":
            name = 'X%27Trapolis'
        elif trainType == "EDI Comeng" or trainType == "Alstom Comeng":
            name = 'Comeng'
        elif trainType == 'Siemens Nexas':
            name = 'Siemens'
        elif trainType == 'HCMT':
            name = 'HCMT'
            
        if carriageNumber.endswith('M'):
            carType = 'M'
        elif carriageNumber.endswith('T'):
            carType = 'T'
        
            
        url = f'https://vicsig.net/index.php?page=suburban&carriage={carriageNumber}&cartype={carType}&traintype={name}'
    
    return(url)

