import discord

async def helpCommand(ctx,category,command):
    file = None # image file
    categories = {
        "search": [
            "</search train:1240101357847838814> - Shows information about a specific train. For multiple units use the carriage number otherwise use the locomotive number. Will show live tracking info if avaliable",
            "</departures:1288002114466877529> - Shows the next Metro trains departing a station. Includes information about which exact train is running the service.",
            "</search run:1240101357847838814> - Shows the run for a TD number. You can find a TDN from the departures command. Currently only Metro is supported.",
            "</search tram:1240101357847838814> - Shows information about a specific tram.",
            "</line-status:1322429532757819473> - Shows disruption information for Rail Operator",
            "</disruptions:1331565431965745186> - Shows disruption information for a Train line.",
            "</search route:1240101357847838814> - Shows disruption information for a Tram or Bus route.",
            "</search train-photo:1240101357847838814> - Shows photos of a specific train from https://railway-photos.xm9g.net\nIncludes the option to search for all carriages in a set.",
            "</search station:1240101357847838814> - Shows information about a specific railway station.",
            "</search ptv:1240101357847838814> - Searches PTV for stations, routes or myki outlets.",
            "/search victorianrailphotos - Searches Victorianrailphotos.com for photos.",
            "</wongm:1288004355475111939> - Searches Wongm's Rail Gallery",

        ],
        "general": [
            "</about:1322339128121102357> - Shows information about the bot.",
            "</submit-photo:1240999419470413875> - Submit a photo to the bot and [website](https://railway-photos.xm9g.net)",
            "</queue:1397528751536996372> - See which of your photos are yet to be submitted",
            "</alias:1404379454955978865> - Choose the alias you want to credited as for your submitted photos.",
            "<accept:1404061643867951154> - An admin command that allows adding of photos to the bot's photo archive.",
            "</stats profile:1240101357847838815> - View your profile with key stats from your logs and games.",
            "</year-in-review:1294634052099375155> - View your year in review with key stats from your logs.",
            "</schedule add:1394221058890010635 - Add a train to be sent in a channel every 30 minutes.",
            "</schedule remove:1394221058890010635> - Remove a train to stop being sent in a channel.",
            "</schedule list:1394221058890010635> - List all the trains that are being sent in a channel.",
        ],
        "fun": [
            "</games station-guesser:1240101357847838813> - Play a game where you guess what station a photo was taken at.",
            "</games station-order:1240101357847838813> - Play a game where you recall which stations are up or down from a specific station.",
            "</games station-hangman:1240101357847838813> - Play a game where you a station name, letter by letter.",
            "</stats leaderboard:1240101357847838815> - Shows the leaderboards for the games.",
            "/train-art - Display ASCII art of Victorian trains with fun facts!",
        ],
        "logs":
        [
            "</log train:1289843416628330506> - Log a Melbourne/Victorian train you have been on. The full set and type will be autofilled by inputting a carriage number, for locomotive serviced use the locomotive number. If you don't know any of the information you can type 'Unknown'.",
            "</log tram:1289843416628330506> - Log a Melbourne tram, works in a similar way to log train.",
            "</log sydney-train:1289843416628330506> - Log a NSW train, works in a similar way to log train however the set and type will not be autofilled.",
            "</log sydney-tram:1289843416628330506> - Log a NSW tram, works the exact same as the log sydney-train.",
            "</log adelaide-train:1289843416628330506> - Log an Adelaide train. The type will be autofilled from the carriage number.",
            "</log adelaide-tram:1289843416628330506> - Log an Adelaide tram, works the exact same as the log adelaide-train.",
            "</log perth-train:1289843416628330506> - Log a Perth train. The type will be autofilled from the carriage number.",
            "</log bus:1289843416628330506> - Log any bus or coach.",
            'For a comprehensive guide of which of these log commands to use in which situation, open </help:1261177133372280957> and in the "commands" option choose "Which /log command should I use?"',
            "</log stats:1289843416628330506> - View stats for your logs such as top lines, stations, sets etc. You can view your stats in many diffrent ways.",
            "</log view:1289843416628330506> - View your logs",
            "</log delete:1289843416628330506> - Delete a log you've made.",
            "</log edit:1289843416628330506> - Edit a log you've made.",
            "</log export:1289843416628330506> - Export a file containing all your logs for a specific mode.",
            "</log import:1289843416628330506> - Import a file containing all your logs for a specific mode. Note that this will override existing logs!",
            "</completion sets:1304404972229623829> - View which sets you have been on for a specific train.",
            "</completion stations:1304404972229623829> - View which stations you have been to.",
            "</stats termini:1240101357847838815> - View which Victorian ail termini you've been to.",
            "</achievements view:1327085604789551134> - View the achievements you've unlocked by logging Victorian Trains.",
            "</maps trips:1340254752461819934> - View a map of the trips you've logged.",
            "</maps view:1340254752461819934> - View the maps this bot uses to display your trips.",
        ],
        "myki":
        [
            "</myki calculate-fare:1289843416628330507> - Calculate the cost of a trip on the Myki network.",
            # "Please note that the following commands are currently broken and won't work:",
            # "</myki save-login:1289843416628330507> - Save your username and password for PTV so you can view your Mykis on this bot.",
            # "</myki view:1289843416628330507> - View your Mykis and their balance.".
        ]
    }
    
    commands = {
        'Which /log command should I use?': '''Depending on which region you're in and which type of public transport you are using, you will use a different command to log your trips.''',
        '/about': '''</about:1322339128121102357> is a command that displays a brief summary of this bot and credits''',
        '/achievements view': '''</achievements view:1327085604789551134> is a command that allows you to view all of the achievements you've unlocked. You unlock achievements every time you add a log that meets the requirement for the achievement. Note that achievements are currently only for logs in Victoria.

**Options:**

Optional:
    User: pick a the user who's logs you're looking at the achievements for. By default it's set to you.''',
        '/completion sets': '''</completion sets:1304404972229623829> is a command that allows you to view which trains of a certain train type you've ridden on. Note that this command is are currently only for Metro and V/Line trains.

**Options:**

Required:
    Train: input the type of train you want to see your completion of.''',
        '/completion stations': '''</completion stations:1304404972229623829> is a command that allows you to view which stations you've been to in a certain state. Note that this command is currently only for trains.

**Options:**

Required:
    State: input the state you want to see the stations of.''',
        '/departures': '''</departures:1288002114466877529> is a command that allows you to view the next 9 services departing from a station/stop. This is currently only for Metro Trains, Yarra Trams and PTV Buses

**Options:**

Required:
    Stop: the station/stop you wish to see the departures from. You must choose from the list.

Optional:
    Time: if you want to see departures starting at a certain time, you can select that time.
    Line: if you wish to only see departures for services going along a specific line, you may select that line. You must choose from the list.''',
        '/favourite add': '''</favourite add:1332262464867536906> is a command that allows you to "favourite" a station or stop so that you can easily find it in the /log commands and the </departures:1288002114466877529> command.
**Options:**

Required:
    Stop: input the station/stop you wish to favourite. You can choose from the list or type your own.''',
        '/favourite remove': '''</favourite remove:1332262464867536906> is a command that allows you to remove your "favourite" a station or stop.
**Options:**

Required:
    Stop: input the station/stop you wish to remove the favourite for. You can choose from the list or type your own.''',
        '/games station-guesser': '''</games station-guesser:1240101357847838813> is a command that allows you to play a game where you have to guess the station where a photo was taken at. The photos are divided into difficulty levels, although all difficulty levels except "Ultrahard" are mixed into one set. The game is divided into rounds, each round one photo is shown and you have to guess the station before the time runs out. To add a guess, type "@TrackPulse Vic" followed by the station name. To skip a round, type "@TrackPulse Vicskip". To end the game, type "@TrackPulse Vicstop".

**Options:**

Optional:
    Rounds: input the number of rounds you want to play. The default is 1. The range is 1 to 100.
    Line: if you wish to only see photos for stations going along a specific line, you may select that line. You must choose from the list.
    Ultrahard: True or False. False by default. If you choose true, the photos will only be photos in the "Ultrahard" category that do not appear in the normal mode.''',
        '/games station-order': '''</games station-order:1240101357847838813> is a command that allows you to play a game where you have to guess the next stations in a certain direction from a given station. The direction is either "Up", towards the city, or "Down", away from the city. The game is divided into rounds, each round one station and the direction are named and you have to guess the other stations before the time runs out. To add a guess, type "@TrackPulse Vic" followed by the station names in order, seperated by a ", ". To skip a round, type "@TrackPulse Vicskip". To end the game, type "@TrackPulse Vicstop".

**Options:**

Optional:
    Direction: if you wish to only play with a certain direction from the station, you may select that station. You must choose from the list. By default it is set to "Up or Down"
    Rounds: input the number of rounds you want to play. The default is 1. The range is 1 to 10.''',
        '/games station-hangman': '''</games station-hangman:1240101357847838813> is a command that allows you to play a game where you have to guess a station name, letter by letter. To skip a round, type "@TrackPulse Vicskip". To end the game, type "@TrackPulse Vicstop".

**Options:**

Optional:
    Rounds: input the number of rounds you want to play. The default is 1. The range is 1 to 10.
    Attempts: input the number of wrong guesses allowed before a round is lost. The default is 10''',
        '/help': '''</help:1261177133372280957> is a command... wait a minute. If you've gotten this far I think you know how to use this command. And besides, just /help by itself gives the tutorial for this command.''',
        '/line-status': '''</line-status:1322429532757819473> is a command that allows you to view the current distruption status of all the lines ran by a certain rail operator. This is currently only for Metro and V/Line.

**Options:**

Required:
    Operator: choose the operator you want to view the line status for. You must choose from the list.''',
        '/log adelaide-train': '''</log adelaide-train:1289843416628330506> is a command to log any Adelaide Metro and Journey Beyond train trips. This is the command to use even if your Journey Beyond train doesn't go through South Australia. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Line: which line you rode on. You have to choose one of the options or type a custom one. If you don't know, type "Unknown". Note that the "----" option isn't meant to be used and just is a seperator to seperate the Adelaide Metro and Journey Beyond lines.
    Number: which carriage you rode. Examples include "3005", "3115", "4001", "NR18". If you don't know, type "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log adelaide-tram': '''</log adelaide-tram:1289843416628330506> is a command to log any Adelaide tram trips. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Line: which tram line you rode on. You have to choose one of the options.
    Number: which carriage you rode. Examples include "101", "201". If you don't know, type "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log bus': '''</log bus:1289843416628330506> is a command to log any bus trips. This is the most versatile log of the log commands as you can log any bus from anywhere. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Line: which bus route you rode on.
    Number: which bus you rode.
    Start: the starting stop of your trip. You can choose from the list or type your own.
    End: the ending stop of your trip. You can choose from the list or type your own.
                        
Optional:
    Operator: the operator of the bus.
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Type: if there are multiple buses with the same number, or you didn't input a number, specify which bus type you rode on. You generally don't need this if you know the bus number.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log delete': '''</log delete:1289843416628330506> is a command that allows you to delete a log you've made. You can only delete logs you've made, and you can only delete one log at a time.

**Options:**

Required:
    Mode: choose the mode of transport you want to view the distruption status for. You must choose from the list.
    
Optional:
    Id: the ID of the log you want to delete. You can find this ID in the log view command. By default it's set to your most recent log.''',     
        '/log edit': '''</log edit:1289843416628330506> is a command that allows you to edit a log you've made. You can only edit logs you've made, and you can only edit one log at a time. This is currently only for Victorian Trains.

**Options:**

Required:
    Id: the ID of the log you want to delete. You can find this ID in the log view command.
    Mode: choose the mode of transport you want to view the distruption status for. You must choose from the list.
    
Optional:
    Line: which line you rode on. You have to choose one of the options or type a custom one. If you don't know, type "Unknown".
    Number: which carriage you rode. Examples include "1M", "2111", "N452", "9026". If you don't know, type "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Type: if there are multiple trains with the same number, or you didn't input a number, specify which train type you rode on. You generally don't need this if you know the train number, it's generally only needed for heritage trips.
    Notes: add any notes you want to add to your log.''',        
        '/log export': '''</log export:1289843416628330506> is a command that allows you to export a file containing all the logs you've made for a specific mode. You can only export your own logs.

**Options:**

Required:
    Format: the format you want the exported file to be.
    Mode: what set of logs are you accessing.

Optional:
    Hidemessage: True or False. False by default. If you choose true, it will make the response message containing your file only visible to you.''',
        '/log import': '''</log import:1289843416628330506> is a command that allows you to import a file containing all the logs you've made for a specific mode. You can only import to your own logs. NOTE THAT THIS WILL OVERRIDE YOUR EXISTING LOGS FOR THIS MODE UNRECOVERABLY!

**Options:**

Required:
Mode: what set of logs are you accessing
File: attach the file you would like to import. It has to be a CSV in the same format as the ones you can export with </log export:1289843416628330506>.''',
        '/log perth-train': '''</log perth-train:1289843416628330506> is a command to log any Transperth and Transwa train trips. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Number: which carriage you rode. Examples include "201", "320", "6050", "1127". If you don't know, type "Unknown".
    Line: which line you rode on. You have to choose one of the options or type a custom one. If you don't know, type "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log stats': '''</log stats:1289843416628330506> is a command to view statistics drawn from a person's logs. There are many statistics you can view, many ways of displaying the graphs, and you can view the statistics of any person who has used the bot.

**Options:**

Required:
    Stat: choose a statistic to view from the list. The choices are:\n"Lines": which lines you've riden and how many times you've riden them,\n"Stations": which stations you've gotten on/off at and how many times you've gotten on/off at them,\n"Trips": which trips you've taken and how many times you've taken them,\n"Trip Length (VIC Train Only)": every VIC Train trip you've taken, with the first log it appears in, sorted by length,\n"Sets": which train sets you've riden and how many times you've riden them,\n"Dates": which dates you've logged and how many logs you logged that day,\n"Types": which types of train you've riden and how many times you've riden them and\n"Operators": which Public Transport Operators you've used and how many times you've used them

Optional:
    Format: what format you want the statistic to be displayed in.\nEach statistic has a default format, generally chosen to display the data in the most convenient way. Choose from the list to override the default format 
    Global_stats: True or False. False by default. If you choose true, it will use all the logs in the system instead of one specific person.
    User: pick a the user who's logs you're looking at the statistic for. By default it's set to you.
    Mode: what set of logs are you accessing. By default it's set to "All": all of the logs for that user.''',
        '/log sydney-train': '''</log sydney-train:1289843416628330506> is a command to log any Sydney Trains, Sydney Metro and NSW Trainlink train trips. This is the command to use even if your NSW Trainlinl train doesn't go through New South Wales. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Line: which line you rode on. You have to choose one of the options. If you don't know, select "Unknown".
    Number: which carriage you rode. Examples include "1801", "2402", "D6360", "N1930". If you don't know, type "Unknown".
    Type: which type of train you rode on. You have to choose one of the options. If you don't know, select "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log sydney-tram': '''</log sydney-tram:1289843416628330506> is a command to log any Sydney Light Rail tram trips. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Line: which Light Rail line you rode on. You have to choose one of the options.
    Number: which carriage you rode. Examples include "001", "2112". If you don't know, type "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log train': '''</log train:1289843416628330506> is a command to log any Metro and V/Line train trips. You can also log some heritage trips in Victoria. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Line: which line you rode on. You have to choose one of the options or type a custom one. If you don't know, type "Unknown".
    Number: which carriage you rode. Examples include "1M", "2111", "N452", "9026". If you don't know, type "Unknown".
    Start: the starting station of your trip. You can choose from the list or type your own.
    End: the ending station of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Type: if there are multiple trains with the same number, or you didn't input a number, specify which train type you rode on. You generally don't need this if you know the train number, it's generally only needed for heritage trips.
    Notes: add any notes you want to add to your log.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log tram': '''</log tram:1289843416628330506> is a command to log any Yarra Trams tram trips. Make sure to log each different leg of your trip seperately.

**Options:**

Required:
    Route: which tram route you rode on. You have to choose one of the options.
    Number: which tram you rode. Examples include "856", "123", "2003", "6001". If you don't know, type "Unknown".
    Start: the starting stop of your trip. You can choose from the list or type your own.
    End: the ending stop of your trip. You can choose from the list or type your own.

Optional:
    Date: if the trip is a trip from the past, input the date here, otherwise, the current date will be added.
    Hidemessage: True or False. False by default. If you choose true, it will make the response message only visible to you.''',
        '/log view': '''</log view:1289843416628330506> is a command allows you to view all the logs recorded by a user. [It has an equivalent in the website](https://discord.com/oauth2/authorize?client_id=1214144664513417218&redirect_uri=https%3A%2F%2Ftrackpulse.xm9g.net%2Flogs%2Fviewer&response_type=code&scope=identify).

**Options:**

Optional:
    Mode: which set of logs you want to view. By default it is set to "Victorian Trains"
    User: pick a user who's logs you wish to view. By default it's set to you.
    Id: if you wish to view a specific log instead of all of your logs, input that log's ID. Examples include "#18A", "#1", "#F"''',        
        '/disruptions': '''</disruptions:1331565431965745186> is a command that allows you to view the current distruption status of a rail line. This is currently only for Metro.

**Options:**

Required:
    Line: choose the line you want to view the distruption status for. You must choose from the list.''',
        '/maps view': '''</maps view:1340254752461819934> is a command that allows you to the maps this bot uses to display your logs.

**Options:**

Required:
    Map_choice: the map you wish to view. You must choose from the list.''',
'/maps trips': '''</maps trips:1340254752461819934> generates a map of the trips you've logged. This is currently only for Victorian Train logs.

**Options:**

Optional:
    Mode: the map you wish to view. You must choose from the list.
    User: pick a user who's logs you wish to view. By default it's set to you.
    Year: the year you wish to view the trips for. By default it is set to the current year.''',
        '/myki calculate-fare': '''</myki calculate-fare:1289843416628330507> is a command that allows you to calculate the cost of trip in Victoria to your myki.

**Options:**

Required:
    Start_zone: the fare zone your trip started in. This has to be an integer from 1 to 15.
    End_zone: the fare zone your trip ended in. This has to be an integer from 1 to 15.''',
        # '/myki save-login': '''Unfortunately the entry for this command hasn't been completed. In fact, this command shouldn't even be functional.''',
        # '/myki view': '''Unfortunately the entry for this command hasn't been completed. In fact, this command shouldn't even be functional.''',
        '/search tv': '''</search tv:1240101357847838814> is a command that allows you to search Transport Victoria for stations, routes or myki outlets.

**Options:**

Required:
    Search: input your search.
    Type: what type of results you want, stations/stops ("stops"), lines/routes ("routes") or myki outlets ("myki outlets"). You have to choose from the list.

Optional:        
    Maxmimum_responses: How many responses for each mode of transport you want. Note that if you set it too high it might not be able to return your results, and if you're using the myki outlet mode, the maximum is 25.''',
        '/search route': '''</search route:1240101357847838814> is a command that allows you to view the current distruption status of a bus or tram route. This is currently only for Yarra Trams and PTV buses.

**Options:**

Required:
    Mode: choose the mode of transport you want to view the distruption status for. You must choose from the list.
    Number: input the number of the route you want to view the distruption status for.''',
        '/search station':'''</search station:1240101357847838814> is a command to look up any railway station in Victoria.

**Options:**

Required:
    Station: input the Number of the train you're searching. You can choose from the list or type your own.''',
        '/search run': '''</search run:1240101357847838814> is a command that allows you to search the details of a specific Metro service that ran/is running/will run today. You can get the TDN for the service from </departures:1288002114466877529>.

**Options:**

Required:
    Td: input the TDN for the run.

Optional:
    Mode: choose which Operator you would like to search the run for. It is set to Metro by default. Currently Metro is also the only option.''',
        '/search train': '''</search train:1240101357847838814> is a command to look up any Victorian train (except locomotive hauled carriages or freight cars) and some NSW Trains . It will give you a overview of the train, including photos and status, along with the ability to see the current runs for Metro trains.

**Options:**

Required:
    Train: input the Number of the train you're searching. Examples include "1M", "9026", "N452", "2111".

Optional:
    State: choose the state the train you want to search belongs to. This is not required except for when a number is used by multiple states. You must choose from the list.
    Hide_run_info: True or False. False by default. If you choose true, it will not show the run info for the train.''',
        '/search train-photo': '''</search train-photo:1240101357847838814> is a command to view the all the photos in the Xm9G photo archive for a specific train.

**Options:**

Required:
    Number: input the number of the train you're searching. Examples include "1M", "9026", "N452", "2111".

Optional:
    Search_set: True or False. False by default. If you choose true, it will include the photos from the other carriages in the train set (if there are others).''',
        '/search tram': '''</search tram:1240101357847838814> is a command to look up any Melbourne tram. It will give you a overview of the tram.

**Options:**

Required:
    Train: input the Number of the tram you're searching. Examples include "856", "123", "2003", "6001".''',
        '/stats leaderboard': '''</stats leaderboard:1240101357847838815> is a command allows you to view a leaderboard for the games on the bot. It shows the top 7 players and their stats.

**Options:**

Optional:
    Game: pick which game you want to view the leaderboard for. You have to choose from the list. By default it's set to "Station Guesser".''',
        '/stats profile': '''</stats profile:1240101357847838815> is a command allows you to view an overview of a user's interaction with this bot.

**Options:**

Optional:
    User: pick a user who's profile you wish to view. By default it's set to you.''',
        '/stats termini': '''</stats termini:1240101357847838815> is a command allows you to view a what Metro and V/Line Termini you've been to.''',
        '/submit-photo': '''</submit-photo:1240999419470413875> is a command that allows you to submit a photograph of a train or a station to the archive this bot pulls from.\nThese photos will be used by the bot in the </search train:1240101357847838814> and </search train-photo:1240101357847838814> commands to represent a specific trainset for trains or the </departures:1288002114466877529> and </search station-photo:1240101357847838814> commands to represent a specific railway station for stations, and will be available for viewing on the [Xm9G photo gallery website](https://railway-photos.xm9g.net).\nIn all of these uses, credit will be provided in the form of "photo by [your name]". If you would like to choose your name, use </alias:1404379454955978865>, otherwise it will use your Discord username.

**Options:**

Required:
    Photo: attach the photo you would like to submit.
    Date: the date the photo was taken. YYYY-MM-DD is the preferred format. Note that Xm9G manually reads this so any info in any understandable form is acceptable.
    Location: input the name of the location the photo was taken. Note that Xm9G manually reads this so any info in any understandable form is acceptable.
    Photofor: input which use your photo is to be used for. You must choose between Railway Photo & Bot train search, Bot/Website Station Photo Guessing Game or both.

Optional:
    Number: input the ID of the train the photo is of, or the name of the railway station. Examples for trains include "1M", "9026", "N452", "2111", "ACN9", although they do not have to be Victorian trains. If there are multiple trains, include as many of them as you want, with each ID seperated by a comma. Note that Xm9G manually reads this so any info in any understandable form is acceptable.''',
        '/wongm': '''</wongm:1288004355475111939> is a command that allows you to search the Wongm Rail Gallery. It provides a link to the results.

**Options:**

Required:
    Search: input your search.''',
        '/year-in-review': '''</year-in-review:1294634052099375155> is a command allows you to view an overview of your trips in a certain year.

**Options:**

Optional:
    Year: pick a year you wish to view. By default it's set to "2024".''',
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
            if command == 'Which /log command should I use?': 
                file = discord.File("assets/comparison.png", filename="comparison.png")
                embed.add_field(name="", value="""**Victoria:**
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
Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""**New South Wales:**
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
Other Bus/Coach: </log bus:1289843416628330506>"""); embed.add_field(name="", value="""**New South Wales Cont.:**
Heritage Train On Mainline: Currently Not Available
Heritage Railway: Currently Not Available
Heritage Tram On Mainline: Currently Not Available
Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""**South Australia:**
Adelaide Metro Rail: </log adelaide-train:1289843416628330506>
Journey Beyond Rail: </log adelaide-train:1289843416628330506>
Adelaide Metro Tram: </log adelaide-tram:1289843416628330506>
Adelaide Metro Bus: </log bus:1289843416628330506>
Adelaide Metro Regional Bus and Coach: </log bus:1289843416628330506>
V/Line Coach: </log bus:1289843416628330506>
NSW TrainLink Coach: </log bus:1289843416628330506>
Other Bus/Coach: </log bus:1289843416628330506>
Heritage Train On Mainline: Currently Not Available
Heritage Railway: Currently Not Available
Heritage Tram On Mainline: Currently Not Available
Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""**Western Australia:**
Transperth Rail: </log perth-train:1289843416628330506>
Transwa Rail: </log perth-train:1289843416628330506>
Journey Beyond Rail: </log adelaide-train:1289843416628330506>
Transperth Ferries: Currently Not Available
Transperth Bus: </log bus:1289843416628330506>
Transwa Coach: </log bus:1289843416628330506>
Other Bus/Coach: </log bus:1289843416628330506>
Heritage Train On Mainline: Currently Not Available
Heritage Railway: Currently Not Available
Heritage Tramway: Currently Not Available"""); embed.add_field(name="", value="""**Northern Territory**
Journey Beyond Rail: </log adelaide-train:1289843416628330506>
Darwinbus: </log bus:1289843416628330506>
Other Bus/Coach: </log bus:1289843416628330506>"""); embed.add_field(name="", value="""**Other regions:**
NSW TrainLink Rail: </log sydney-train:1289843416628330506>
NSW TrainLink Coach: </log bus:1289843416628330506>
Any Bus/Coach: </log bus:1289843416628330506>"""); 
                embed.set_image(url="attachment://comparison.png")
        else:
            embed = discord.Embed(title="Invalid Command", description="Please choose a valid command.", color=discord.Color.red())  # Corrected title for clarity
    else: 
        ctx.response.send_message('You cant choose both a category and a command!')
        return
    
    if file is not None:
        await ctx.response.send_message(embed=embed, file=file)
    else:
        await ctx.response.send_message(embed=embed)