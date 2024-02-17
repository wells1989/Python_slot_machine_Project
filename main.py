from utils.slot_variables import spin, winnings
from utils.user_variables import add_deposit, withdraw, define_bet
from db.sql import db_main, update_balance_in_db

# Main user selection and game
def main():

    # User log in and authentication
    balance, username = db_main()

    if balance == 0:
        amount = input("Insufficient funds. Need to deposit to play, enter deposit amount: ")
        try:
            amount = float(amount)
            balance = add_deposit(balance, amount)
            update_balance_in_db(username, balance)
        except ValueError:
            print("Please enter a valid number")

    # User setting total_bet
    total_bet = define_bet(balance)

    while True and balance >= total_bet:

        print("Balance: ", balance)

        user_choice = input("do you want to spin? y / n / c to change bet size / d to deposit funds / w to withdraw funds: ")

        if user_choice == "c":
            total_bet = define_bet(balance)
        elif user_choice == "d":
            amount = input("how much do you want to deposit? ")
            try:
                amount = float(amount)
                balance = add_deposit(balance, amount)
                update_balance_in_db(username, balance)
            except ValueError:
                print("Please enter a valid number")

        elif user_choice == "w":
            while True:
                try:
                    amount = float(input("how much do you want to withdraw? "))

                    if amount > balance:
                        print(f'unable to withdraw {amount}, current balance is {balance}')
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number")

            
            balance = withdraw(balance, amount)
            update_balance_in_db(username, balance)
            

        elif user_choice == "n":
            print("leaving game")
            break

        else:
            symbols, symbols_per_line, winning_symbols = spin()
            is_winner, balance = winnings(symbols, symbols_per_line, balance, total_bet, winning_symbols, username)

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

main()

