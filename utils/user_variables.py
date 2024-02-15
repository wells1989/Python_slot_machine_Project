balance = 20

""" dev only
bet_size = 1
bet_coins = 1
total_bet = 4"""

# Takes user input and returns a total_bet amount
def define_bet(balance):
    while True:
        bet_size = input ("choose your bet size: ")
        bet_coins = input("choose your coin size: ")
        
        try:
            total_bet = int(bet_size) * int(bet_coins)
        except ValueError:
            print("Please enter a valid number for bet size and lines")
            continue

        if total_bet > balance:
            print("insufficient funds")
        else:
            break
    
    print("total bet is: ", total_bet)

    return total_bet


def add_deposit(balance, amount):
    balance += amount
    print("new balance after deposit: ", balance)
    return balance


def withdraw(balance, amount):
    balance -= amount
    print("new balance after withdrawal: ", balance)
    return balance

