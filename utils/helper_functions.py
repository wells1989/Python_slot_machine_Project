from utils.slot_variables import odds
import random

# Helper Functions

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


# winning line logic functions
def horizontal_line_win(symbols, total_bet, winning_messages, amount_won):
    for line in symbols:
            if all(elem == line[0] for elem in line):
                winning_symbol = line[0]

                if winning_symbol == "*":
                    winnings = bonus_round(total_bet)
                    amount_won += winnings

                else:
                    amount_won, winnings = add_winnings(winning_symbol, total_bet, amount_won)
                
                winning_messages += [winning_symbol, "Horizontal Line", winnings]

                return amount_won, winning_messages