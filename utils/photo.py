import csv
import requests
import io

def getPhotoCredits(train, state='VIC'):
    # image credits:
    if state == 'VIC':
        url = 'https://victorianrailphotos.com/credit.csv'
    elif state == 'NSW':
        url = 'https://victorianrailphotos.com/nswcredit.csv'
        
    search_value = train.strip().upper()

    response = requests.get(url)
    response.raise_for_status() 

    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))

    result_value = None
    for row in csv_reader:
        if row[0].strip().upper() == search_value:
            result_value = row[1]
            break
    if result_value == None:
        result_value = "Billy Evans"
    return result_value
