import random

balance = 10

"""def define_bet():
    while True:
        bet_size = input ("choose your bet size: ")
        bet_lines = input("choose your bet lines: ")
        
        try:
            total_bet = int(bet_size) * int(bet_lines)
        except ValueError:
            print("Please enter a valid number for bet size and lines")
            continue

        if total_bet > balance:
            print("insufficient funds")
        else:
            break
    
    print("total bet is: ", total_bet)
    return int(bet_size), total_bet
           
total_bet, bet_size = define_bet()"""

# dev only
bet_size = 1
bet_lines = 1
total_bet = 1

def bonus_round(total_bet):
    bonus_winnings = 0
    random_values = [50,20,250,500,100,40,70,80,120,30,25,40,50]

    while True:
        input("welcome to the bonus round! Click to choose a prize!: ")

        index_to_replace = random.randint(0, len(random_values) - 1)

        value = total_bet * random_values.pop(index_to_replace)
        bonus_winnings += value
        print("you have won", value)
        print("total winnings:", bonus_winnings)
        
        if len(random_values) <= 7:
            break

    return bonus_winnings

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

def get_multiplier(symbol):
    for odd in odds:
        if odd['option'] == symbol:
            return odd["multiplier"]

def spin():

    options = []

    for odd in odds:
        for i in range(0, odd["chance"]):
            options.append(odd['option'])
        
    random.shuffle(options)

    betting_lines = 3
    symbols_per_line = 3

    symbols = [
        ["f", "a", "d"],
        ["d", "*", "f"],
        ["a", "b", "a"]
    ]
    """
    alt with more lines
    symbols = [
        ["f", "c", "b", "d"],
        ["b", "f", "f", "f"],
        ["c", "b", "b", "b"]
    ]
    """
    """
    symbols = []

    for i in range(0, betting_lines):
        symbols.append([])
        for y in range(0, symbols_per_line):
            # symbols[i].append("a")

            symbols[i].append(random.choice(options))"""

    # now e.g. symbols = [['d', 'd', 'e'], ['a', 'd', 'c'], ['*', 'd', 'b']]
    
    # printing the results
    for i in range(0, len(symbols)):
        print(symbols[i])
    
    return symbols, symbols_per_line

def winnings(symbols, symbols_per_line, balance, total_bet):
    amount_won = 0
    
    winning_messages = []

    # horizontal winnings
    for line in symbols:
        if all(elem == line[0] for elem in line):
            winning_symbol = line[0]

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings

            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings

            winning_messages += [winning_symbol, "Horizontal Line", winnings]

    # vertical winnings
    for i in range(symbols_per_line):
        if len(set(row[i] for row in symbols)) == 1:
            winning_symbol = symbols[0][i]

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings  

            winning_messages += [winning_symbol, "Vertical Line", winnings]  

    # diagonal winnings
        # top-left to bottom-right
    if all(symbols[i][i] == symbols[0][0] for i in range(symbols_per_line)):
            winning_symbol = symbols[0][0]

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings 
            
            winning_messages += [winning_symbol, "Diagonal Line", winnings]

       # top-right to bottom-left 
    if all(symbols[i][symbols_per_line - 1 - i] == symbols[0][symbols_per_line - 1] for i in range(symbols_per_line)):
            winning_symbol = symbols[i][symbols_per_line - 1 - i]

            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings
            
            winning_messages += [winning_symbol, "Diagonal Line", winnings]

            
    # extra lines
    # L shaped 
            """ 1
                2 3 """ 
    for i in range(0, len(symbols)-1):
        if all(symbols[i+1][j] == symbols[i][0] for j in range (1, symbols_per_line)):
            winning_symbol = symbols[i][0]
            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings

            winning_messages += [winning_symbol, "\ - - L-shaped Line", winnings]
 
    # Reverse L shaped ...
            """    2  3
                 1                """
    for i in range(1, len(symbols)):
        if all(symbols[i-1][j] == symbols[i][0] for j in range (i, symbols_per_line)):
        
            winning_symbol = symbols[i][0]
            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings

            winning_messages += [winning_symbol, " / - - L-shaped Line", winnings]

    # W shaped
            """ a         a
                  a  a  a  """
    for i in range(0, len(symbols)-1):
        if all(symbols[i+1][j] == symbols[i][0] for j in range(1, symbols_per_line-1)) and symbols[i][0] == symbols[i][symbols_per_line-1]:
            winning_symbol = symbols[i][0]
            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings  

            winning_messages += [winning_symbol, "\ - / Long W-shaped Line", winnings]    
    
    # reverse Long w shaped
            """    b  b  b      
                b           b  """
    for i in range(1, len(symbols)):
        if all(symbols[i-1][j] == symbols[i][0] for j in range(1,symbols_per_line-1)) and symbols[i][0] == symbols[i][symbols_per_line-1]:
            winning_symbol = symbols[i][0]
            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings  

            winning_messages += [winning_symbol, " / - \ Reverse Long W-shaped Line", winnings]  

    # V / short W shaped
            """ e.g.
                ["F", "C", "F"],    
                ["b", "*", "b"],
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
        if winning_symbol == "*":
            winnings = bonus_round(total_bet)
            amount_won += winnings
        else:
            multiplier = get_multiplier(winning_symbol)
            winnings = total_bet * multiplier
            amount_won  += winnings  

        winning_messages += [winning_symbol, "V shaped line", winnings] 

    if len(matched_symbols2) == 1:
        winning_symbol = symbols[len(symbols)-1][0]
        if winning_symbol == "*":
            winnings = bonus_round(total_bet)
            amount_won += winnings
        else:
            multiplier = get_multiplier(winning_symbol)
            winnings = total_bet * multiplier
            amount_won  += winnings  

        winning_messages += [winning_symbol, "^ shaped line", winnings] 


    if amount_won:
        print("you have won", amount_won)

        if winning_messages:
            while winning_messages:
                separate_list = [winning_messages.pop(0) for _ in range(3)]

                symbol, message, payout = separate_list

                print("You won on symbol " + symbol + " < - > " + message + ", payout:",payout)

        balance += amount_won
        return True, balance
    else:
        balance -= total_bet
        return False, balance
    

while True and balance >= total_bet:
    user_choice = input("do you want to spin? y/n")

    if user_choice == "n":
        print("leaving game")
        break
    result, symbols_per_line = spin()
    is_winner, balance = winnings(result, symbols_per_line, balance, total_bet)

    if is_winner:
        print("Winner")
        print("New balance:", balance)
    else:
        print("No win")
        print("New balance:", balance)

        if balance == 0:
            print("insufficient funds")
