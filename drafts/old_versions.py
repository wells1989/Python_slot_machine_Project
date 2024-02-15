

"""
L-shaped lines

   old version, only works with 3 * 3 grids

   1
                2 3

            for i in range(0, len(symbols)-1):
                if symbols[i][i] == symbols[i+1][i+1] == symbols[i+1][i+2]:
                    print("new line matched")

                    winning_symbol = symbols[i][i]
                    if winning_symbol == "*":
                        winnings = bonus_round(total_bet)
                        amount_won += winnings
                    else:
                        multiplier = get_multiplier(winning_symbol)
                        winnings = total_bet * multiplier
                        amount_won  += winnings 
                        

            old version, only works on 3 * 3 grids
            1
                2 3
                   
            for i in range(1, len(symbols) - 1):
                if symbols[i][0] == symbols[i-1][i] == symbols[i-1][i+1]:
                    winning_symbol = symbols[i][0]
                    if winning_symbol == "*":
                        winnings = bonus_round(total_bet)
                        amount_won += winnings
                    else:
                        multiplier = get_multiplier(winning_symbol)
                        winnings = total_bet * multiplier
                        amount_won  += winnings
                        """ 