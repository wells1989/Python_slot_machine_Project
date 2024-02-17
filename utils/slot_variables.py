import random
from db.sql import update_balance_in_db

## Helper Functions

# returns a mutliplier based on the symbol in odds dictionary
def get_multiplier(symbol):
    for odd in odds:
        if odd['option'] == symbol:
            return odd["multiplier"]
        

# on a win calculates total winnings
def add_winnings(winning_symbol, total_bet, amount_won):
    multiplier = get_multiplier(winning_symbol)
    winnings = total_bet * multiplier
    amount_won  += winnings
    return amount_won, winnings


# on matching 3 *** symbols enters the bonus round
def bonus_round(total_bet):
    bonus_winnings = 0
    random_values = [50,20,250,500,100,40,70,80,120,30,25,40,50]

    exit_chance = 0
    print("welcome to the bonus round!")
    while True:
        input("Click to choose a random prize!: ")

        index_to_replace = random.randint(0, len(random_values) - 1)

        value = total_bet * random_values.pop(index_to_replace)
        exit_chance + random.randint(1, 10)
        bonus_winnings += value
        print("you have won", value)
        print("total Bonus win:", bonus_winnings)
        
        if exit_chance >= 30 or len(random_values) <= 5:
            break

    return bonus_winnings


## Primary slot variableS 

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


## Primary functions

# Populating the spin matrix
def spin():

    options = []

    for odd in odds:
        for i in range(0, odd["chance"]):
            options.append(odd['option'])
        
    random.shuffle(options)

    """ DEV ONLY symbols = [
        ['f', 'b', 'f'],
        ['*', '*', '*'],
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


# getting winnings from the spin result ...
def winnings(symbols, symbols_per_line, balance, total_bet, winning_symbols, username):
    amount_won = 0
    winning_messages = []

    # horizontal winnings
    for i, line in enumerate(symbols):
        if all(elem == line[0] for elem in line):
            winning_symbol = line[0]

            for j in range(symbols_per_line):
                winning_symbols[i][j] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings

            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)

            winning_messages += [winning_symbol, " Horizontal Line", winnings]

    # vertical winnings
    for i in range(symbols_per_line):
        if len(set(row[i] for row in symbols)) == 1:
            winning_symbol = symbols[0][i]

            for elem in range(symbols_per_line):
                winning_symbols[elem][i] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)
 

            winning_messages += [winning_symbol, " Vertical Line", winnings]  

    # diagonal winnings
        # top-left to bottom-right
    if all(symbols[i][i] == symbols[0][0] for i in range(symbols_per_line)):
            winning_symbol = symbols[0][0]
            
            for j in range(symbols_per_line):
                winning_symbols[j][j] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)

            
            winning_messages += [winning_symbol, " Diagonal Line", winnings]

       # top-right to bottom-left 
    if all(symbols[i][symbols_per_line - 1 - i] == symbols[0][symbols_per_line - 1] for i in range(symbols_per_line)):
            winning_symbol = symbols[i][symbols_per_line - 1 - i]

            for j in range(symbols_per_line):
                winning_symbols[j][symbols_per_line - 1 - j] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)

            
            winning_messages += [winning_symbol, " Diagonal Line", winnings]

            
    # L shaped 
            """ 1
                    2 3 """ 
    for i in range(0, len(symbols)-1):
        if all(symbols[i+1][j] == symbols[i][0] for j in range (1, symbols_per_line)):
            winning_symbol = symbols[i][0]

            winning_symbols[i][0] = winning_symbol.upper()
            for k in range(1, symbols_per_line):
                winning_symbols[i+1][k] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)


            winning_messages += [winning_symbol, " \\ - - L-shaped Line", winnings]
 
    # Reverse L shaped ...
            """    2  3
                 1                """
    for i in range(1, len(symbols)):
        if all(symbols[i-1][j] == symbols[i][0] for j in range (1, symbols_per_line)):
            winning_symbol = symbols[i][0]

            winning_symbols[i][0] = winning_symbol.upper()
            for k in range(1, symbols_per_line):
                winning_symbols[i-1][k] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)


            winning_messages += [winning_symbol, " / - - L-shaped Line", winnings]

    # W shaped
            """ a         a
                  a  a  a  """
    for i in range(0, len(symbols)-1):
        if all(symbols[i+1][j] == symbols[i][0] for j in range(1, symbols_per_line-1)) and symbols[i][0] == symbols[i][symbols_per_line-1]:
            winning_symbol = symbols[i][0]

            winning_symbols[i][0] = winning_symbol.upper()
            winning_symbols[i][symbols_per_line-1] = winning_symbol.upper()
            for k in range(1, symbols_per_line-1):
                winning_symbols[i+1][k] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)


            winning_messages += [winning_symbol, " \\ - / Long W-shaped Line", winnings]    
    
    # reverse w shaped
            """    b  b  b      
                b           b  """
    for i in range(1, len(symbols)):
        if all(symbols[i-1][j] == symbols[i][0] for j in range(1,symbols_per_line-1)) and symbols[i][0] == symbols[i][symbols_per_line-1]:
            winning_symbol = symbols[i][0]

            winning_symbols[i][0] = winning_symbol.upper()
            winning_symbols[i][symbols_per_line-1] = winning_symbol.upper()
            for k in range(1, symbols_per_line-1):
                winning_symbols[i-1][k] = winning_symbol.upper()

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)
 

            winning_messages += [winning_symbol, " / - \\ Reverse Long W-shaped Line", winnings]  

    # V shaped
            """ e.g.
                ["F", "C", "F"],    
                ["e", "*", "b"],
                ["C", "F", "C"]
                """
        matched_symbols1 = set()
        matched_symbols2 = set()
    for i in range(0, symbols_per_line):
        
        if i % 2 == 0: # even indexes, e.g. index 0 and 2
            matched_symbols1.add(symbols[0][i])
            matched_symbols2.add(symbols[len(symbols)-1][i])

        else: # odd indexes, e.g. 1
            matched_symbols1.add(symbols[len(symbols)-1][i])
            matched_symbols2.add(symbols[0][i])

    if len(matched_symbols1) == 1:
        winning_symbol = symbols[0][0]
        
        for j in range(0, symbols_per_line):
            if j % 2 == 0:
                winning_symbols[0][j] = winning_symbol.upper()
            else:
                winning_symbols[len(symbols)-1][j] = winning_symbol.upper()

        if winning_symbol == "*":
            winnings = bonus_round(total_bet)
            amount_won += winnings
        else:
            amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)

        winning_messages += [winning_symbol, " V shaped line", winnings] 

    if len(matched_symbols2) == 1:
        winning_symbol = symbols[len(symbols)-1][0]

        for j in range(0, symbols_per_line):
            if j % 2 == 0:
                winning_symbols[len(symbols)-1][j] = winning_symbol.upper()
            else:
                winning_symbols[0][j] = winning_symbol.upper()

        if winning_symbol == "*":
            winnings = bonus_round(total_bet)
            amount_won += winnings
        else:
            amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)

        winning_messages += [winning_symbol, " ^ shaped line", winnings] 

    # adding all winnings to balance and updating db
    if amount_won:
        print(f'\n you have won {amount_won} \n')

        for i in range(0, len(winning_symbols)):
            print(winning_symbols[i])

        if winning_messages:
            while winning_messages:
                separate_list = [winning_messages.pop(0) for _ in range(3)]

                symbol, message, payout = separate_list

                print(f'You won on symbol {symbol.upper()} {message}, Payout: {payout}') # "You won on symbol " + symbol.upper() + message + ", payout:",payout

        balance += amount_won
        update_balance_in_db(username, balance)

        return True, balance
    else:
        balance -= total_bet
        update_balance_in_db(username, balance)
        return False, balance
