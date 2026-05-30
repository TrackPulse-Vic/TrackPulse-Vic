import os
import csv
from tabnanny import check
from datetime import datetime, timedelta

def checkAchievements(user):
    vline_trains = ['VLocity', 'Sprinter', 'N Class']
    metro_trains = ["X'Trapolis 100", 'EDI Comeng', 'Alstom Comeng', 'Siemens Nexas', 'HCMT']
    filepath = f"utils/trainlogger/userdata/{user}.csv"
    Adelaidefilepath = f"utils/trainlogger/userdata/adelaide-trains/{user}.csv"
    
    # Check if required files exist
    if not os.path.exists(filepath):
        filepath = None
        return []
    
    if not os.path.exists(Adelaidefilepath):
        Adelaidefilepath = None

    print('checking for first log...')
    new_achievements = []
    
    # first log checker

    if os.path.exists(filepath):
        new_achievements.append('1')
        print('First log achievement added')
    else:
        print('First log achievement not added')
    
    # all metro trains checker
    print('checking for all metro trains...')
    items_found = set()
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 1: 
                item = row[2]  
                if item in metro_trains:
                    items_found.add(item)
        
        if items_found == set(metro_trains):
            new_achievements.append('2')
            print('All Metro trains achievement added')
        else:
            print('All Metro trains achievement not added')
            print(f"Items missing: {set(metro_trains) - items_found}")
            
    # all vline trains checker
    print('Checking for all v/line trains...')
    items_found = set()
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:        
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 1: 
                item = row[2]  
                if item in vline_trains:
                    items_found.add(item)
        
        if items_found == set(vline_trains):
            new_achievements.append('3')
            print('All V/Line trains achievement added')
        else:
            print('All V/Line trains achievement not added')
            print(f"Items missing: {set(vline_trains) - items_found}")
            
    # all lines  checker
    print('Checking for all lines...')
    items_found = set()
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        mtrains = ["Lilydale", 'Belgrave', 'Alamein',"Glen Waverley", 'Bairnsdale', 'Traralgon', 'Pakenham', 'Cranbourne', 'Frankston', 'Stony Point', 'Sandringham', 'Williamstown', 'Werribee', 'Geelong', 'Warrnambool', 'Ballarat', 'Ararat', 'Marybourough', 'Swan Hill', 'Echuca', 'Bendigo', 'Seymour', 'Sunbury', 'Craigieburn', 'Upfield', 'Shepparton', 'Albury', 'Mernda', 'Hurstbridge']
        
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 1: 
                item = row[4]  
                if item in mtrains:
                    items_found.add(item)
        
        if items_found == set(mtrains):
            new_achievements.append('3')
            print('All lines achievement added')
        else:
            print('All lines achievement not added')
            print(f"Items missing: {set(mtrains) - items_found}")
            
    # Check for specific stations visited
    print('Checking for specific stations visited...')
    specific_station_groups = {
        'Metro Tunnel': {
            'stations': {'Arden', 'Parkville', 'State Library', 'Town Hall', 'Anzac'},
            'achievement': '43'
        },
    }

    visited_stations = set()
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                visited_stations.add(row[5])  # From station
                visited_stations.add(row[6])  # To station
                
        for group_name, group_data in specific_station_groups.items():
            print(f'Checking {group_name} group...')
            if any(station in visited_stations for station in group_data['stations']):
                new_achievements.append(group_data['achievement'])
                print(f'{group_name} group achievement added')
            else:
                print(f'{group_name} group achievement not added')
                print(f"No stations from {group_name} visited yet")
            
    # 10 trips in a day checker
    print('Checking for 10 trips in a day...')
    dates = {}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 3:  # Make sure row has enough columns
                date = row[3]  # Date is in column 4
                dates[date] = dates.get(date, 0) + 1
        
        # Check if any date has 10 or more trips
        if any(count >= 10 for count in dates.values()):
            new_achievements.append('5')
            print('10 trips in a day achievement added')
        else:
            print('10 trips in a day achievement not added')
            print(f"Maximum trips in a day: {max(dates.values()) if dates else 0}")
        
    # end of line checker
    print('Checking for end of line stations...')
    end_stations = {
        'Lilydale', 'Belgrave', 'Alamein', 'Glen Waverley', 'East Pakenham', 'Cranbourne', 
        'Frankston', 'Stony Point', 'Sandringham', 'Williamstown', 'Werribee', 'Sunbury', 
        'Craigieburn', 'Upfield', 'Mernda', 'Hurstbridge', 'Warrnambool', 'Bairnsdale', 'Swan Hill', 'Echuca', 'Albury', 'Shepparton', 'Ararat', 'Maryborough'
    }

    visited_stations = set()
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 5:  # Make sure row has enough columns
                visited_stations.add(row[5])  # From station
                visited_stations.add(row[6])  # To station

        # Check if user has visited any end stations
        if any(station in end_stations for station in visited_stations):
            new_achievements.append('7')
            print('End of line achievement added')
        else:
            print('End of line achievement not added')
            print(f"End stations visited: {visited_stations & end_stations}")
            
    # check for a group of staitons visited
    print('Checking for station groups...')

    station_groups = {
        'City Loop': {
            'stations': {'Southern Cross', 'Flinders Street', 'Parliament', 'Melbourne Central', 'Flagstaff'},
            'achievement': '37'
        },
        'Geelong': {
            'stations': {'Corio', 'North Shore','North Geelong', 'Geelong', 'South Geelong', 'Marshall', 'Waurn Ponds'},
            'achievement': '38'
        },
        'Altona Loop': {
            'stations': {'Altona','Seaholme', 'Westona'},
            'achievement': '39'
        },
        'Metro Tunnel': {
            'stations': {'Parkville', 'State Library', 'Town Hall', 'Anzac'},
            'achievement': '41'
        }
    }

    visited_stations = set()
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                visited_stations.add(row[5])  # From station
                visited_stations.add(row[6])  # To station
                
        for group_name, group_data in station_groups.items():
            print(f'Checking {group_name} group...')
            if visited_stations.issuperset(group_data['stations']):
                new_achievements.append(group_data['achievement'])
                print(f'{group_name} group achievement added')
            else:
                print(f'{group_name} group achievement not added')
                print(f"Stations missing: {group_data['stations'] - visited_stations}")
    
    # 1 year of logging checker
    print('Checking for 1 year of logging...')

    oldest_date = None
    newest_date = None

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 3:  # Make sure row has enough columns
                try:
                    date = datetime.strptime(row[3], '%Y-%m-%d')
                    if oldest_date is None or date < oldest_date:
                        oldest_date = date
                    if newest_date is None or date > newest_date:
                        newest_date = date
                except ValueError:
                    continue

    if oldest_date and newest_date:
        time_diff = newest_date - oldest_date
        if time_diff >= timedelta(days=365):
            new_achievements.append('11')
            print('1 year of logging achievement added')
        else:
            print('1 year of logging achievement not added')
            print(f"Current logging duration: {time_diff.days} days")
            
    # Check for log count achievements
    print('Checking for log count achievements...')
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        log_count = sum(1 for row in csv.reader(csvfile))
        
        if log_count >= 1000:
            new_achievements.extend(['12', '13', '14'])
            print('1000 logs achievement added')
        elif log_count >= 500:
            new_achievements.extend(['12', '13'])
            print('500 logs achievement added')
        elif log_count >= 100:
            new_achievements.append('12')
            print('100 logs achievement added')
        
        print(f"Current log count: {log_count}")
        
    # Check for Aboriginal train set numbers
    print('Checking for Aboriginal trains...')
    special_sets = ['853M-1627T-854M', '933M-1667T-934M', '9024-9124-9224-9324-9724-9824-9924']

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] in special_sets:
                new_achievements.append('9')
                print('Aboriginal train achievement added')
                break
        else:
            print('Aboriginal train achievement not added')
            
    # Check for V/Line trains at Metro stations achievement
    print('Checking for V/Line trains at Metro stations...')
    metro_stations = {'Pakenham', 'Sunbury'}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:  # Ensure row has enough columns
                train_type = row[2]
                from_station = row[5]
                to_station = row[6]
                if (train_type in vline_trains and 
                    (from_station in metro_stations or to_station in metro_stations)):
                    new_achievements.append('16')
                    print('V/Line at Metro stations achievement added')
                    break
        else:
            print('V/Line at Metro stations achievement not added')
            
    # Check for SG trains
    print('Checking for SG trains...')
    pride_sets = ['1193-1593-1293', '1194-1594-1294', '1195-1595-1295', '1196-1596-1296', '1197-1597-1297']

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] in pride_sets:
                new_achievements.append('17')
                print('SG set achievement added')
                break
        else:
            print('SG set achievement not added')
    
    # # Check for 7005 (removed cause its no longer in that livery)
    # print('Checking for 7005')
    # vline_train_7005 = '7005'

    # with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
    #     csv_reader = csv.reader(csvfile)
    #     for row in csv_reader:
    #         if len(row) > 1 and row[1] == vline_train_7005:
    #             new_achievements.append('18')
    #             print('7005 train achievement added')
    #             break
    #     else:
    #         print('7005 train achievement not added')
            
    # Check for heratige train types
    print('Checking for heratige train types...')
    heariatage = {'Tait', 'K Class', 'R Class', 'S Class', 'A2 Class', 'D3 Class', 'Y Class', 'T Class'}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 2 and row[2] in heariatage:
                new_achievements.append('8')
                print('heratige train achievement added')
                if row[5] or row[6] == 'Newport':
                    new_achievements.append('40')
                    print('heratige from/to newport achievement added')
                break
        else:
            print('heratige train achievement not added')
            
    # Check for 100 visits to a single station
    print('Checking for 100 visits to a single station...')
    station_visits = {}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                from_station = row[5]
                to_station = row[6]
                station_visits[from_station] = station_visits.get(from_station, 0) + 1
                station_visits[to_station] = station_visits.get(to_station, 0) + 1
        
        if any(visits >= 100 for visits in station_visits.values()):
            new_achievements.append('19')
            print('100 visits to a single station achievement added')
        else:
            print('100 visits to a single station achievement not added')
            print(f"Most visited station count: {max(station_visits.values()) if station_visits else 0}")
    
    # Check for trains running on unusual lines
    print('Checking for trains running on unusual lines...')
    line_train_map = {
        'Lilydale': ["X'Trapolis 100"], 'Belgrave': ["X'Trapolis 100"], 'Alamein': ["X'Trapolis 100"], 
        'Glen Waverley': ["X'Trapolis 100"], 'Hurstbridge': ["X'Trapolis 100"], 'Mernda': ["X'Trapolis 100"], 
        'Pakenham': ['HCMT'], 'Cranbourne': ['HCMT'], 
        'Frankston': ["X'Trapolis 100", "X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'], 
        'Werribee': ["X'Trapolis 100", "X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'], 
        'Williamstown': ["X'Trapolis 100", "X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'], 
        'Sandringham': ['Siemens Nexas', 'Alstom Comeng', 'EDI Comeng'], 
        'Upfield': ['Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "X'Trapolis 2.0"], 
        'Craigieburn': ['Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "X'Trapolis 2.0"], 
        'Sunbury': ['HCMT']
    }
    
    ptv_trains = ['Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "HCMT", "X'Trapolis 100", "X'Trapolis 2.0", 'VLocity', 'Sprinter', 'N Class']

    unusual_trains_found = False

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 4:
                train_type = row[2]
                line = row[4]
                if line in line_train_map and train_type in line_train_map[line]:
                    continue
                elif line in line_train_map and train_type not in line_train_map[line] and train_type in ptv_trains:
                    new_achievements.append('15')
                    unusual_trains_found = True
                    print(f'Unusual train {train_type} on line {line} achievement added')
                    break

    if not unusual_trains_found:
        print('Unusual train on line achievement not added')
        
    # Check for all stations visited
    print('Checking for all stations visited...')
    stations_visited = set()

    # Read all stations from the file
    all_stations = set()
    try:
        with open('utils/datalists/stations.txt', 'r', encoding='utf-8') as f:
            all_stations = {line.strip() for line in f if line.strip()}

        # Read visited stations from user data
        with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) > 6:
                    stations_visited.add(row[5])  # From station
                    stations_visited.add(row[6])  # To station

        if stations_visited.issuperset(all_stations):
            new_achievements.append('10')
            print('All stations achievement added')
        else:
            print('All stations achievement not added')
            print(f"Stations missing: {all_stations - stations_visited}")
    except FileNotFoundError:
        print('Stations list file not found')
        
    # Check for 5 days straight of logging
    print('Checking for 5 consecutive days of logging...')
    dates = set()

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 3:  # Make sure row has enough columns
                try:
                    date = datetime.strptime(row[3], '%Y-%m-%d')
                    dates.add(date)
                except ValueError:
                    continue

    dates = sorted(dates)
    max_consecutive = 1
    current_consecutive = 1

    for i in range(1, len(dates)):
        if dates[i] - dates[i-1] == timedelta(days=1):
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    if max_consecutive >= 5:
        new_achievements.append('20')
        print('5 consecutive days achievement added')
        print(f"Maximum consecutive days: {max_consecutive}")
    else:
        print('5 consecutive days achievement not added')
        print(f"Maximum consecutive days: {max_consecutive}")
        
    
    # Check for trips on different line groups
    print('Checking for trips on line groups...')
    
    # Define line groups and their achievement IDs
    line_groups = {
        'Burnley': {
            'lines': {'Lilydale', 'Belgrave', 'Glen Waverley', 'Alamein'},
            'achievement': '21'
        },
        'Cross City': {
            'lines': {'Sandringham', 'Werribee', 'Williamstown'},
            'achievement': '22'
        },
        'Sandringham': {
            'lines': {'Sandringham'},
            'achievement': '23'
        },
        'Northern': {
            'lines': {'Craigieburn', 'Upfield'},
            'achievement': '24'
        },
        'Clifton Hill': {
            'lines': {'Mernda', 'Hurstbridge'},
            'achievement': '25'
        },
        'Dandenong': {
            'lines': {'Pakenham', 'Cranbourne', 'Sunbury'},
            'achievement': '26'
        }
    }

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for group_name, group_data in line_groups.items():
            print(f'Checking {group_name} group...')
            csvfile.seek(0)  # Reset file pointer for each group
            for row in csv_reader:
                if len(row) > 4 and row[4] in group_data['lines']:
                    new_achievements.append(group_data['achievement'])
                    print(f'{group_name} group achievement added')
                    break
            else:
                print(f'{group_name} group achievement not added')
                
    # Check for all train types in one day
    print('Checking for all train types in one day...')
    train_types_by_date = {}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 3:
                date = row[3]
                train_type = row[2]
                if date not in train_types_by_date:
                    train_types_by_date[date] = set()
                train_types_by_date[date].add(train_type)

        standard_train_types = {"X'Trapolis 100","X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', 'HCMT', 'VLocity', 'N Class', 'Sprinter'}
        
        for date, types in train_types_by_date.items():
            if types.issuperset(standard_train_types):
                new_achievements.append('27')
                print('All train types in one day achievement added')
                break
        else:
            print('All train types in one day achievement not added')
            max_types = max(len(types) for types in train_types_by_date.values()) if train_types_by_date else 0
            print(f"Maximum train types in one day: {max_types}")
            
    # Check for station pairs
    print('Checking for station pairs...')
    station_pairs = {
        ('Southern Cross', 'Swan Hill'): '28',
        ('Riversdale', 'Willison'): '34',
        ('Werribee', 'Sandringham'): '36',
        ('Sunbury', 'East Pakenham'): '42'

    }

    achievement_pairs_found = set()
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                from_station = row[5]
                to_station = row[6]
                for (station1, station2), achievement_id in station_pairs.items():
                    if achievement_id not in achievement_pairs_found and \
                       ((from_station == station1 and to_station == station2) or \
                        (from_station == station2 and to_station == station1)):
                        new_achievements.append(achievement_id)
                        achievement_pairs_found.add(achievement_id)
                        print(f'Station pair achievement {achievement_id} added')
                        break
                    
    # Check for specific line combinations
    print('Checking for specific line combinations...')
    line_achievements = {
        'Flemington Racecourse': '29',
        'City Circle': '30',
        'Stony Point': '31',
    }

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        lines_visited = set()
        for row in csv_reader:
            if len(row) > 4:
                line = row[4]
                if line in line_achievements and line_achievements[line] not in new_achievements:
                    new_achievements.append(line_achievements[line])
                    print(f'Achievement added for line: {line}')
                    lines_visited.add(line)

    missing_lines = set(line_achievements.keys()) - lines_visited
    if missing_lines:
        print(f"Lines not yet visited: {missing_lines}")
        
    # Check for V/Line trains at Essendon or Berwick
    print('Checking for V/Line trains at Essendon or Berwick...')
    special_stations = {'Essendon', 'Berwick'}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                train_type = row[2]
                from_station = row[5]
                to_station = row[6]
                if (train_type in vline_trains and 
                    (from_station in special_stations or to_station in special_stations)):
                    new_achievements.append('32')
                    print('V/Line at Essendon/Berwick achievement added')
                    break
        else:
            print('V/Line at Essendon/Berwick achievement not added')
            
    print('Checking for overland in Victoria')
    required_stations = {'Southern Cross', 'North Shore', 'Ararat', 'Stawell', 'Horsham', 'Dimboola', 'Nhill'}  
    required_train_type = 'NR Class'  
    achievement_id = '33'

    if Adelaidefilepath != None:
        with open(Adelaidefilepath, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) > 6:
                    train_type = row[2]
                    from_station = row[5]
                    to_station = row[6]
                    if (train_type == required_train_type and 
                        from_station in required_stations and 
                        to_station in required_stations):
                        new_achievements.append(achievement_id)
                        print('Specific train and station combo achievement added')
                        break
            else:
                print('Specific train and station combo achievement not added')
    else:
        print('No adelaide logs')
        
    # check for all metro lines in 1 day
    print('Checking for all metro lines in 1 day...')
    metro_end_stations = {
        'Lilydale': 'Lilydale',
        'Belgrave': 'Belgrave', 
        'Alamein': 'Alamein',
        'Glen Waverley': 'Glen Waverley',
        'Pakenham': 'East Pakenham',
        'Cranbourne': 'Cranbourne',
        'Frankston': 'Frankston',
        'Sandringham': 'Sandringham',
        'Williamstown': 'Williamstown',
        'Werribee': 'Werribee',
        'Sunbury': 'Sunbury',
        'Craigieburn': 'Craigieburn',
        'Upfield': 'Upfield',
        'Mernda': 'Mernda',
        'Hurstbridge': 'Hurstbridge'
    }

    end_stations_by_date = {}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                date = row[3]
                from_station = row[5]
                to_station = row[6]
                
                if date not in end_stations_by_date:
                    end_stations_by_date[date] = set()
                    
                # Check if either station is an end station
                for station in [from_station, to_station]:
                    if station in metro_end_stations.values():
                        end_stations_by_date[date].add(station)
        
        # Check if any date has all end stations
        all_end_stations = set(metro_end_stations.values())
        for date, stations in end_stations_by_date.items():
            if stations == all_end_stations:
                new_achievements.append('35')
                print('All end stations in one day achievement added')
                break
        else:
            print('All end stations in one day achievement not added')
            if end_stations_by_date:
                max_stations = max(len(stations) for stations in end_stations_by_date.values())
                print(f"Maximum end stations visited in one day: {max_stations}")
    
    # Check which achievements are actually new
    userCSV = f'utils/trainlogger/achievements/data/{user}.csv'
    existing_achievements = {}
    
    if os.path.exists(userCSV):
        with open(userCSV, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                for i in range(0, len(row), 2):
                    if i + 1 < len(row):
                        existing_achievements[row[i]] = row[i + 1]
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    truly_new = [ach for ach in new_achievements if ach not in existing_achievements]
    new_with_dates = {ach: current_date for ach in truly_new}
    
    # Combine existing and new achievements
    all_achievements = existing_achievements.copy()
    all_achievements.update(new_with_dates)
    
    # Write all achievements with dates to CSV
    if all_achievements:
        with open(userCSV, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            flat_list = [item for pair in all_achievements.items() for item in pair]
            csv_writer.writerow(flat_list)
    
    if truly_new:
        print(f"Added the following achievements on {current_date}: {truly_new}")
    else:
        print("No new achievements to add.")
    
    return truly_new

def checkGameAchievements(user):
    mode = 'guesser'
    print(f'Checking for guesser achievements for {user}')
    filepath = f"utils/game/scores/{mode}.csv"
    mode = 'ultrahard'
    UltrahardFilepath = f"utils/game/scores/{mode}.csv"

    new_achievements = []

    if not os.path.exists(filepath):
        print('Data file does not exist!')
        return []

    # Track stats from game file
    wins = 0
    losses = 0
    uhwins = 0
    uhlosses = 0

    with open(filepath, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] == user:
                wins = int(row[2])
                losses = int(row[3])
                break
            
    with open(UltrahardFilepath, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] == user:
                uhwins = int(row[2])
                uhlosses = int(row[3])
                break
            
    total_games = wins + losses
    total_uhgames = uhwins + uhlosses
    
    print(f'{user} guesser stats: {wins} wins, {losses} losses, {total_games} total')

    # Check for first game achievement
    if total_games > 0:
        new_achievements.append('100')
    if total_uhgames > 0:
        new_achievements.append('108')

    # Check for accuracy achievements
    if total_games >= 50:
        accuracy = (wins / total_games) * 100
        if accuracy >= 90:
            new_achievements.append('106')
        if accuracy >= 75:
            new_achievements.append('107')
        if accuracy >= 99:
            new_achievements.append('109')
    if total_uhgames >= 50:
        accuracy = (uhwins / total_uhgames) * 100
        if accuracy >= 90:
            new_achievements.append('115')
        if accuracy >= 75:
            new_achievements.append('116')
        if accuracy >= 99:
            new_achievements.append('117')

    # Check for streak-related achievements (if applicable)
    if wins >= 1000:
        new_achievements.append('105')
    if wins >= 100:
        new_achievements.append('103')
    if wins >= 10:
        new_achievements.append('104')
    
    if uhwins >= 1000:
        new_achievements.append('114')
    if uhwins >= 100:
        new_achievements.append('113')
    if uhwins >= 10:
        new_achievements.append('112')

    # Check for games played achievements
    if total_games >= 100:
        new_achievements.append('102')
    if total_games >= 10:
        new_achievements.append('101')
    
    if total_uhgames >= 100:
        new_achievements.append('111')
    if total_uhgames >= 10:
        new_achievements.append('110')

    # Check which achievements are actually new
    userCSV = f'utils/trainlogger/achievements/data/{user}.csv'
    existing_achievements = {}  # Dictionary to store achievement ID: date
    
    # Read existing achievements with dates
    if os.path.exists(userCSV):
        with open(userCSV, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                for i in range(0, len(row), 2):  # Assuming format: [id, date, id, date, ...]
                    if i + 1 < len(row):
                        existing_achievements[row[i]] = row[i + 1]
    
    # Determine truly new achievements with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    truly_new = [ach for ach in new_achievements if ach not in existing_achievements]
    new_with_dates = {ach: current_date for ach in truly_new}
    
    # Combine existing and new achievements
    all_achievements = existing_achievements.copy()
    all_achievements.update(new_with_dates)
    
    # Write all achievements with dates to CSV
    if all_achievements:
        with open(userCSV, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Flatten dictionary into list: [id1, date1, id2, date2, ...]
            flat_list = [item for pair in all_achievements.items() for item in pair]
            csv_writer.writerow(flat_list)
    
    if truly_new:
        print(f"Added the following game achievements on {current_date}: {truly_new}")
    else:
        print("No new game achievements to add.")
    
    return truly_new

def checkHangmanAchievements(user):
    filepath = f"utils/game/scores/hangman.csv"
    new_achievements = []
    
    print(f'Checking for hangman achievements for {user}')
    
    if not os.path.exists(filepath):
        print('Data file does not exist!')
        return []
    
    # Track stats from game file
    wins = 0
    losses = 0

    with open(filepath, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] == user:
                wins = int(row[2])
                losses = int(row[3])
                break
    total_games = wins + losses
    print(f'{user} hangman stats: {wins} wins, {losses} losses, {total_games} total')
    
    # amount of games achievement
    if total_games > 0:
        new_achievements.append('200')
    if total_games >= 25:
        new_achievements.append('201')
    if total_games >= 100:
        new_achievements.append('202')
    
    # wins achievement
    if wins >= 10:
        new_achievements.append('203')
    if wins >= 50:
        new_achievements.append('204')
    if wins >= 100:
        new_achievements.append('205')
    if wins >= 1000:
        new_achievements.append('206')
        
    # accuracy achievements
    if total_games >= 50:
        accuracy = (wins / total_games) * 100
        if accuracy >= 90:
            new_achievements.append('207')
        if accuracy >= 75:
            new_achievements.append('208')
        if accuracy >= 99:
            new_achievements.append('209')

    # Check which achievements are actually new
    userCSV = f'utils/trainlogger/achievements/data/{user}.csv'
    existing_achievements = {}  # Dictionary to store achievement ID: date
    
    # Read existing achievements with dates
    if os.path.exists(userCSV):
        with open(userCSV, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                for i in range(0, len(row), 2):  # Assuming format: [id, date, id, date, ...]
                    if i + 1 < len(row):
                        existing_achievements[row[i]] = row[i + 1]
    
    # Determine truly new achievements with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    truly_new = [ach for ach in new_achievements if ach not in existing_achievements]
    new_with_dates = {ach: current_date for ach in truly_new}
    
    # Combine existing and new achievements
    all_achievements = existing_achievements.copy()
    all_achievements.update(new_with_dates)
    
    # Write all achievements with dates to CSV
    if all_achievements:
        with open(userCSV, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Flatten dictionary into list: [id1, date1, id2, date2, ...]
            flat_list = [item for pair in all_achievements.items() for item in pair]
            csv_writer.writerow(flat_list)
    
    if truly_new:
        print(f"Added the following game achievements on {current_date}: {truly_new}")
    else:
        print("No new game achievements to add.")
        
    return truly_new
    

def returnAchievements(user):
    filepath = f'utils/trainlogger/achievements/data/{user}.csv'
    achievements = []

    # Read user's achievements
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                achievements.extend(row)

    # Get achievement details from master list
    achievement_details = []
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] in achievements:
                achievement_details.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                })

    return achievement_details

def getAchievementInfo(id):
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == id:
                return {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                }
        return None
    
def awardAchievement(user, id):
    filepath = f'utils/trainlogger/achievements/data/{user}.csv'
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    existing_achievements = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                for i in range(0, len(row), 2):
                    if i + 1 < len(row):
                        existing_achievements[row[i]] = row[i + 1]
    
    if id not in existing_achievements:
        with open(filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id, current_date])
        print(f"Awarded achievement {id} to {user} on {current_date}")
    else:
        print(f"{user} already has achievement {id}")
    