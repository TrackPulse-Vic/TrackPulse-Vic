from utils.trainlogger.map.station_coordinates_log_sydney_tram_map import x_offset, y_offset

line_coordinates = {
    'L1': {
        ('Capitol Square', 'Central'): [
            (9700 + x_offset, 3950 + y_offset, 9800 + x_offset, 4350 + y_offset),
            (9650 + x_offset, 4350 + y_offset, 9800 + x_offset, 4500 + y_offset), # Central Coords
            (9550 + x_offset, 4500 + y_offset, 9750 + x_offset, 4600 + y_offset), # Central Coords
            (9300 + x_offset, 4500 + y_offset, 9550 + x_offset, 4650 + y_offset), # Central Coords
        ],
        ("Paddy's Markets", 'Capitol Square'): [
            (8900 + x_offset, 3750 + y_offset, 8900 + x_offset, 3900 + y_offset),
            (8900 + x_offset, 3800 + y_offset, 9750 + x_offset, 3890 + y_offset),
            (9700 + x_offset, 3800 + y_offset, 9800 + x_offset, 4000 + y_offset),
        ],
        ('Exhibition Centre', "Paddy's Markets"): [
            (8350 + x_offset, 3750 + y_offset, 8950 + x_offset, 3900 + y_offset),
        ],
        ('Convention', 'Exhibition Centre'): [
            (7750 + x_offset, 3750 + y_offset, 8400 + x_offset, 3900 + y_offset),
        ],
        ('Pyrmont Bay', 'Convention'): [
            (7150 + x_offset, 3750 + y_offset, 7800 + x_offset, 3900 + y_offset),
        ],
        ('John Street Square', 'Pyrmont Bay'): [
            (6550 + x_offset, 3750 + y_offset, 7200 + x_offset, 3900 + y_offset),
        ],
        ('Fish Market', 'John Street Square'): [
            (6000 + x_offset, 3750 + y_offset, 6600 + x_offset, 3900 + y_offset),
        ],
        ('Wentworth Park', 'Fish Market'): [
            (5400 + x_offset, 3750 + y_offset, 6050 + x_offset, 3900 + y_offset),
        ],
        ('Glebe', 'Wentworth Park'): [
            (4900 + x_offset, 3750 + y_offset, 5450 + x_offset, 3900 + y_offset),
        ],
        ('Jubilee Park', 'Glebe'): [
            (4450 + x_offset, 3750 + y_offset, 4950 + x_offset, 3900 + y_offset)
        ],
        ('Rozelle Bay', 'Jubilee Park'): [
            (4000 + x_offset, 3750 + y_offset, 4500 + x_offset, 3900 + y_offset),
        ],
        ('Lilyfield', 'Rozelle Bay'): [
            (3550 + x_offset, 3750 + y_offset, 4050 + x_offset, 3900 + y_offset),
        ],
        ('Leichhardt North', 'Lilyfield'): [
            (3050 + x_offset, 3750 + y_offset, 3600 + x_offset, 3900 + y_offset),
        ],
        ('Hawthorne', 'Leichhardt North'): [
            (2800 + x_offset, 3800 + y_offset, 2950 + x_offset, 4000 + y_offset),
            (2800 + x_offset, 3750 + y_offset, 3100 + x_offset, 3900 + y_offset),
        ],
        ('Marion', 'Hawthorne'): [
            (2800 + x_offset, 3950 + y_offset, 2900 + x_offset, 4250 + y_offset),
        ],
        ('Taveners Hill', 'Marion'): [
            (2800 + x_offset, 4200 + y_offset, 2950 + x_offset, 4500 + y_offset),
        ],
        ('Lewisham West', 'Taveners Hill'): [
            (2800 + x_offset, 4450 + y_offset, 2950 + x_offset, 4800 + y_offset),
        ],
        ('Waratah Mills', 'Lewisham West'): [
            (2800 + x_offset, 4750 + y_offset, 2950 + x_offset, 5100 + y_offset),
        ],
        ('Arlington', 'Waratah Mills'): [
            (2800 + x_offset, 5050 + y_offset, 2900 + x_offset, 5400 + y_offset),
        ],
        ('Dulwich Grove', 'Arlington'): [
            (2800 + x_offset, 5350 + y_offset, 2950 + x_offset, 5700 + y_offset),
        ],
        ('Dulwich Hill', 'Dulwich Grove'): [
            (2750 + x_offset, 5650 + y_offset, 2950 + x_offset, 5900 + y_offset),
        ],
    },
    'L2': {
        ('UNSW High Street', 'Randwick'): [
            (10450 + x_offset, 6550 + y_offset, 10600 + x_offset, 7000 + y_offset),
        ],
        ('Wansey Road', 'UNSW High Street'): [
            (10500 + x_offset, 6150 + y_offset, 10600 + x_offset, 6600 + y_offset),
        ],
        ('Royal Randwick', 'Wansey Road'): [
            (10500 + x_offset, 5800 + y_offset, 10600 + x_offset, 6200 + y_offset),
        ],
        ('Moore Park', 'Royal Randwick'): [
            (9400 + x_offset, 5550 + y_offset, 10600 + x_offset, 5850 + y_offset),
        ],
        ('Surrey Hills', 'Moore Park'): [
            (9400 + x_offset, 5250 + y_offset, 9500 + x_offset, 5600 + y_offset),
        ],
        ('Central', 'Surrey Hills'): [
            (9400 + x_offset, 4650 + y_offset, 9500 + x_offset, 5300 + y_offset),
            (9650 + x_offset, 4350 + y_offset, 9800 + x_offset, 4500 + y_offset), # Central Coords
            (9550 + x_offset, 4500 + y_offset, 9750 + x_offset, 4600 + y_offset), # Central Coords
            (9300 + x_offset, 4500 + y_offset, 9550 + x_offset, 4650 + y_offset), # Central Coords
        ],
        ('Haymarket', 'Central'): [
            (9450 + x_offset, 4150 + y_offset, 9500 + x_offset, 4500 + y_offset),
            (9300 + x_offset, 4000 + y_offset, 9550 + x_offset, 4150 + y_offset), # Haymarket Coords
            (9650 + x_offset, 4350 + y_offset, 9800 + x_offset, 4500 + y_offset), # Central Coords
            (9550 + x_offset, 4500 + y_offset, 9750 + x_offset, 4600 + y_offset), # Central Coords
            (9300 + x_offset, 4500 + y_offset, 9550 + x_offset, 4650 + y_offset), # Central Coords
        ],
        ('Chinatown', 'Haymarket'): [
            (9450 + x_offset, 3500 + y_offset, 9550 + x_offset, 3800 + y_offset),
            (9450 + x_offset, 3900 + y_offset, 9500 + x_offset, 4000 + y_offset),
            (9300 + x_offset, 4000 + y_offset, 9550 + x_offset, 4150 + y_offset), # Haymarket Coords
        ],
        ('Town Hall', 'Chinatown'): [
            (9450 + x_offset, 3250 + y_offset, 9550 + x_offset, 3550 + y_offset),
        ],
        ('QVB', 'Town Hall'): [
            (9450 + x_offset, 3000 + y_offset, 9550 + x_offset, 3300 + y_offset),
        ],
        ('Wynyard', 'QVB'): [
            (9450 + x_offset, 2750 + y_offset, 9550 + x_offset, 3050 + y_offset),
        ],
        ('Bridge Street', 'Wynyard'): [
            (9450 + x_offset, 2500 + y_offset, 9550 + x_offset, 2800 + y_offset),
        ],
        ('Circular Quay', 'Bridge Street'): [
            (9450 + x_offset, 2350 + y_offset, 9550 + x_offset, 2550 + y_offset),
            (9300 + x_offset, 2200 + y_offset, 9550 + x_offset, 2350 + y_offset), # Circular Quay Coords
        ],
    },
    'L3': {
        ('Kingsford', 'Juniors Kingsford'): [

        ],
    },
}

def getTotalLines_sydney_tram():
    total_lines = 0
    for line_type in line_coordinates.values():
        for station_pair in line_type.values():
            total_lines += len(station_pair)
    return total_lines

print(getTotalLines_sydney_tram())