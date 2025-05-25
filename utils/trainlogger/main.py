import csv
import os
import sqlite3
import discord

def hextodec(hexnum):
    decnum = int(str(hexnum), 16) 
    return decnum

def dectohex(decnum):
    hexnum = hex(decnum)
    return hexnum[2:].upper()

def is_hexadecimal(s):
   for char in s:
      if not char.isalnum(): # Check if the character is a valid hexadecimal digit
         return False
   return True

def addTrain(username, set, date, train_type, line, start, end, note, userid=None):
    conn = sqlite3.connect(f'userdata/trainlogs.db')
    cursor = conn.cursor()
    
    if set.endswith('-'):
        set = set[:-1]
    
    cursor.execute(f'''
            INSERT INTO logs (user_id, og_id, set_number, train_type, date, line, start, end, notes, username)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (userid, 'NULL', set, date, train_type, line, start, end, note, str(username))) # note: date and train type are swapped here due to a bug in the original code

    cursor.execute("SELECT last_insert_rowid()")
    id = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()

    return id

# Tram version:
def addTram(username, date, train_number, train_type, line, start, end, notes):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/tram/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\tram')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/tram')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, notes])


    print(f"Data saved to {filename}")
    return id

def addSydneyTrain(username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/sydney-trains/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\sydney-trains')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/sydney-trains')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addBus(username, date, train_number, train_type, line, start, end, operator, notes=None):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/bus/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\bus')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/bus')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, operator, notes])


    print(f"Data saved to {filename}")
    return id
# B
def addFlight(username, date, train_number, train_type, line, start, end, operator):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/flights/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\flights')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/flights')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, operator])


    print(f"Data saved to {filename}")
    return id


def addSydneyTram(username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/sydney-trams/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\sydney-trams')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/sydney-trams')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addAdelaideTrain(username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/adelaide-trains/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\adelaide-trains')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/adelaide-trains')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addAdelaideTram(username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/adelaide-trams/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\adelaide-trams')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/adelaide-trams')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addPerthTrain(username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/perth-trains/{username}.csv"
    
    if not os.path.exists(filename):
        # Create the file if it does not exist
        with open(filename, 'w') as file:
            file.write('')  
        print(f"File created: {filename}")
    else:
        print(f"File already exists: {filename}")
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\perth-trains')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/perth-trains')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def readLogs(username):


    filename = f"utils/trainlogger/userdata/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1] 
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
 
def readTramLogs(username):

    filename = f"utils/trainlogger/userdata/tram/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readSydneyTrainLogs(username):

    filename = f"utils/trainlogger/userdata/sydney-trains/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    
def readSydneyLightRailLogs(username):

    filename = f"utils/trainlogger/userdata/sydney-trams/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readBusLogs(username):

    filename = f"utils/trainlogger/userdata/bus/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readAdelaideLogs(username):

    filename = f"utils/trainlogger/userdata/adelaide-trains/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readAdelaideTramLogs(username):

    filename = f"utils/trainlogger/userdata/adelaide-trams/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    
def readPerthLogs(username):

    filename = f"utils/trainlogger/userdata/perth-trains/{username}.csv"
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

# same as one above but only reads the row you put in   
def readRow(username, logid):
    try:
        os.listdir('utils\\trainlogger\\userdata')
    except FileNotFoundError:
        return 'no data at all'
    

    filename = f"utils/trainlogger/userdata/{username}.csv"

    # Open the CSV file and read the data
    with open(filename, 'r', newline='') as file:
        data = file.readlines()

        if data == []:
            return 'no data for user'
        else:
            if logid == 'LAST':
                id = data[-1].split(',')[0][1:]
            else:
                id = logid
            row = None
            for r in data:
                if r.split(',')[0] == f'#{id}':
                    row = r
                    break
            if row == None:
                return 'invalid id did not show up'
            else:
                return row

# same as the other but it works for all modes
def universalReadRow(username, logid, mode):
    try:
        os.listdir('utils\\trainlogger\\userdata')
    except FileNotFoundError:
        return 'no data at all'
    

    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"

    # Open the CSV file and read the data
    with open(filename, 'r', newline='') as file:
        data = file.readlines()

        if data == []:
            return 'no data for user'
        else:
            if logid == 'LAST':
                id = data[-1].split(',')[0][1:]
            else:
                id = logid
            row = None
            for r in data:
                if r.split(',')[0] == f'#{id}':
                    row = r
                    break
            if row == None:
                return 'invalid id did not show up'
            else:
                return row
        
def deleteRow(username, logid, mode):

    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        
    # Open the CSV file and read the data
    with open(filename, 'r+', newline='') as file:
        data = file.readlines()

        if logid == 'LAST':
            id = data[-1].split(',')[0][1:]
        else:
            id = logid
        
        file.truncate(0)
        file.seek(0)
        
        for r in data:
            if r.split(',')[0] != f'#{id}':
                file.write(r)
                
        return id
    
def editRow(username, logid, mode, line:str='nochange', number:str='nochange', start:str='nochange', end:str='nochange', date:str='nochange', traintype:str='auto', notes:str='nochange'):
    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"

    # Open the CSV file and read the data
    with open(filename, 'r+', newline='') as file:
        data = file.readlines()

        # Find the row to edit
        row_index = None
        for i, row in enumerate(data):
            if row.split(',')[0] == f'#{logid}':
                row_index = i
                break

        if row_index is not None:
            # Split the row into fields
            fields = data[row_index].strip().split(',')

            # Update fields that aren't 'nochange'
            if line != 'nochange':
                fields[4] = line
            if number != 'nochange':
                fields[1] = number
            if start != 'nochange':
                fields[5] = start
            if end != 'nochange':
                fields[6] = end
            if date != 'nochange':
                fields[3] = date
            if traintype != 'auto':
                fields[2] = traintype
            if notes != 'nochange':
                fields[7] = notes

            # Reconstruct the row
            data[row_index] = ','.join(fields) + '\n'

            # Write all data back to file
            file.seek(0)
            file.truncate()
            file.writelines(data)

            return data[row_index]
        
        return 'invalid id did not show up'

