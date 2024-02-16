from utils.slot_variables import spin
from utils.helper_functions import add_winnings, bonus_round
from utils.user_variables import add_deposit, withdraw, define_bet
from db.sql import db_main, update_balance_in_db

balance, username = db_main()
total_bet = define_bet(balance)

# getting all winnings from the spin result ...
def winnings(symbols, symbols_per_line, balance, total_bet, winning_symbols):
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

            
    # extra lines
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
    
    # reverse Long w shaped
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

    if amount_won:
        print("\n you have won", amount_won, "\n")


        for i in range(0, len(winning_symbols)):
            print(winning_symbols[i])

        if winning_messages:
            while winning_messages:
                separate_list = [winning_messages.pop(0) for _ in range(3)]

                symbol, message, payout = separate_list

                print("You won on symbol " + symbol.upper() + message + ", payout:",payout)

        balance += amount_won
        update_balance_in_db(username, balance)

        return True, balance
    else:
        balance -= total_bet
        return False, balance


# Main user selection and game
def main(balance, total_bet):
    while True and balance >= total_bet:

        print("Balance: ", balance)

        user_choice = input("do you want to spin? y / n / c to change bet size / d to deposit funds / w to withdraw funds: ")

        if user_choice == "c":
            total_bet = define_bet(balance)
        elif user_choice == "d":
            amount = input("how much do you want to deposit? ")
            try:
                amount = int(amount)
                balance = add_deposit(balance, amount)
                update_balance_in_db(username, balance)
            except ValueError:
                print("Please enter a valid number for bet size and lines")

        elif user_choice == "w":
            amount = input("how much do you want to withdraw? ")
            try:
                amount = int(amount)
                balance = withdraw(balance, amount)
                update_balance_in_db(username, balance)
            except ValueError:
                print("Please enter a valid number for bet size and lines")

        elif user_choice == "n":
            print("leaving game")
            break

        else:
            result, symbols_per_line, winning_symbols = spin()
            is_winner, balance = winnings(result, symbols_per_line, balance, total_bet, winning_symbols)

            if is_winner:
                print("Winner!")
            else:
                print("No win")

        if balance == 0:
                print("insufficient funds")
                user_input = input("press q to quit or d to deposit funds: ")
                if user_input == "q":
                    print("leaving game")
                    quit
                elif user_input == "d":
                    amount = input("how much do you want to deposit? ")
                    try:
                        amount = int(amount)
                        balance = add_deposit(balance, amount)
                        update_balance_in_db(username, balance)
                    except ValueError:
                        print("Please enter a valid number")


main(balance, total_bet)

