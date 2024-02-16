import random

odds = [
    # working on chances out of 100
    {"option": "*", "chance": 3},
    {"option": "a", "chance": 6, "multiplier": 8},
    {"option": "b", "chance": 13, "multiplier": 5},
    {"option": "c", "chance": 17, "multiplier": 3.5},
    {"option": "d", "chance": 19, "multiplier": 3},
    {"option": "e", "chance": 20, "multiplier": 2.5},
    {"option": "f", "chance": 22, "multiplier": 2},
]

vertical_lines = 3 # vertical axis
symbols_per_line = 3 # horizontal axis

# Populating the spin matrix
def spin():

    options = []

    for odd in odds:
        for i in range(0, odd["chance"]):
            options.append(odd['option'])
        
    random.shuffle(options)

    """symbols = [
        ['f', 'b', 'f'],
        ['a', '*', 'a'],
        ['b', 'f', 'b']
    ]"""

    winning_symbols = [
        ['X', 'X', 'X'],
        ['X', 'X', 'X'],
        ['X', 'X', 'X']
    ]

    symbols=[]

    for i in range(0, vertical_lines):
        symbols.append([])
        for y in range(0, symbols_per_line):
            # symbols[i].append("a")

            symbols[i].append(random.choice(options))

    # now e.g. symbols = [['d', 'd', 'e'], ['a', 'd', 'c'], ['*', 'd', 'b']]
    
    for i in range(0, len(symbols)):
        print(symbols[i])
    
    return symbols, symbols_per_line, winning_symbols
