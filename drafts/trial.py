""" INCORRECTLY ADDING UP TOTALS, TRYING TO ADJUST IT TO WORK WITH MORE THAN 3 LINES ...

            1 
              2 3
for i in range(0, len(symbols)-1):
        if all(symbols[i+1][j] == symbols[i][0] for j in range (i+1, symbols_per_line - 1)):

            winning_symbol = symbols[i][i]
            if winning_symbol == "*":
                winnings = bonus_round(total_bet)
                amount_won += winnings
            else:
                multiplier = get_multiplier(winning_symbol)
                winnings = total_bet * multiplier
                amount_won  += winnings

                2  3
                 1          
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
        

    if amount_won:
        print("you have won", amount_won)
        balance += amount_won
        return True, balance
    else:
        balance -= total_bet
        return False, balance"""
