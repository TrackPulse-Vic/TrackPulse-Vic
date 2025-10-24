"""
ASCII Art representations of Victorian trains
Fun feature for TrackPulse Vic bot
"""

import random

# ASCII art for different train types
TRAIN_ART = {
    "comeng": r"""
    _____________________
   | [] [] [] [] [] [] |
   |___________________|
   |  o   o   o   o    |
  =|_o___o___o___o____|=
    O   O   O   O   O
   ~~~~~ COMENG ~~~~~
""",
    
    "siemens": r"""
    ______________________
   /                      \
  | [][][] [][][] [][][] |
  |______________________|
  |  o    o    o    o    |
 =|__o____o____o____o____|=
   O    O    O    O    O
  ~~~~~ SIEMENS NEXAS ~~~~~
""",
    
    "xtrapolis": r"""
    _____________________
   /[]  []  []  []  []  \
  |_____________________|
  |   o    o    o    o   |
 =|___o____o____o____o___|=
    O    O    O    O    O
   ~~~~~ X'TRAPOLIS ~~~~~
""",
    
    "hcmt": r"""
    ________________________
   /========================\
  | [][][] [][][] [][][] |
  |________________________|
  |   o     o     o     o   |
 =|___o_____o_____o_____o___|=
    O     O     O     O     O
   ~~~~~~~ HCMT ~~~~~~~
""",
    
    "vlocity": r"""
    _______________________
   /  V                 V  \
  | [][][] [][][] [][][] |
  |_______________________|
  |   o     o     o     o   |
 =|___o_____o_____o_____o___|=
    O     O     O     O     O
   ~~~~~~ VLocity ~~~~~~
""",
    
    "sprinter": r"""
    __________________
   /   __________    \
  |  /          \   |
  | []  []  []  [] |
  |________________|
  |  o    o    o   |
 =|__o____o____o___|=
   O    O    O    O
  ~~~~ SPRINTER ~~~~
""",
    
    "generic": r"""
    ___________________
   |[]  []  []  []  []|
   |___________________|
   |  o   o   o   o   |
  =|__o___o___o___o___|=
    O   O   O   O   O
   ~~~~ TRAIN ~~~~
"""
}

# Fun train facts for Victorian trains
TRAIN_FACTS = {
    "comeng": [
        "Comeng trains have been running in Melbourne since 1981!",
        "The Comeng fleet is split between EDI-built and Alstom-built units.",
        "Comeng trains were the first air-conditioned trains in Melbourne.",
        "At their peak, there were 95 3-car Comeng sets in service.",
        "Comeng trains are named after Commonwealth Engineering, who designed them."
    ],
    "siemens": [
        "Siemens Nexas trains entered service in 2002.",
        "The Siemens fleet consists of 18 3-car sets.",
        "Siemens trains were the first in Melbourne to have LED destination displays.",
        "These trains can operate as 3-car or 6-car formations.",
        "Siemens trains have a top speed of 115 km/h."
    ],
    "xtrapolis": [
        "X'Trapolis 100 trains started service in 2002.",
        "The X'Trapolis fleet is the largest in Melbourne with 72 trains.",
        "These trains were built by Alstom in France.",
        "X'Trapolis trains have a unique blue interior lighting.",
        "Each X'Trapolis train can carry up to 798 passengers."
    ],
    "hcmt": [
        "HCMT stands for High Capacity Metro Train.",
        "HCMTs entered service in 2019, the newest addition to Melbourne's fleet.",
        "Each HCMT is 160 meters long and can carry 1,380 passengers!",
        "HCMTs have 20% more capacity than previous train types.",
        "The fleet consists of 65 7-car sets, all built by Bombardier/Alstom."
    ],
    "vlocity": [
        "VLocity trains are V/Line's diesel multiple unit fleet.",
        "VLocity trains were manufactured by Bombardier Transportation.",
        "First VLocity trains entered service in 2005.",
        "VLocity trains can travel at speeds up to 160 km/h.",
        "The fleet serves regional Victoria with over 60 sets in operation."
    ],
    "sprinter": [
        "Sprinter trains are V/Line's diesel railcars.",
        "Sprinters have been in service since 1993.",
        "These trains were built by Walkers Limited in Maryborough.",
        "Sprinters typically operate as single-car units.",
        "They serve regional Victorian routes and can reach 130 km/h."
    ]
}


def get_train_art(train_type: str = None) -> str:
    """
    Get ASCII art for a specific train type.
    
    Args:
        train_type: Type of train (comeng, siemens, xtrapolis, hcmt, vlocity, sprinter)
                   If None, returns a random train.
    
    Returns:
        ASCII art string of the train
    """
    if train_type is None:
        train_type = random.choice(list(TRAIN_ART.keys()))
    
    train_type = train_type.lower().replace("'", "").replace(" ", "")
    
    # Handle variations in naming
    if "xtrap" in train_type:
        train_type = "xtrapolis"
    elif "nexas" in train_type:
        train_type = "siemens"
    
    return TRAIN_ART.get(train_type, TRAIN_ART["generic"])


def get_train_fact(train_type: str = None) -> str:
    """
    Get a random fun fact about a train type.
    
    Args:
        train_type: Type of train (comeng, siemens, xtrapolis, hcmt, vlocity, sprinter)
                   If None, returns a fact about a random train.
    
    Returns:
        A fun fact string
    """
    if train_type is None:
        train_type = random.choice(list(TRAIN_FACTS.keys()))
    
    train_type = train_type.lower().replace("'", "").replace(" ", "")
    
    # Handle variations in naming
    if "xtrap" in train_type:
        train_type = "xtrapolis"
    elif "nexas" in train_type:
        train_type = "siemens"
    
    facts = TRAIN_FACTS.get(train_type, ["Trains are cool!"])
    return random.choice(facts)


def get_all_train_types() -> list:
    """
    Get list of all available train types.
    
    Returns:
        List of train type names
    """
    return list(TRAIN_ART.keys())
