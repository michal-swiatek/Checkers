class Player:
    """Human player"""

    def pass_control(self, boardstate):
        boardstate.display()
        print("Instruction prompt:")       #  ---  placeholder for prompt - (surrender or move - temporary format:  1 2 3 4; where 1 2 - start coordinates,  3 4 - end coordinates)
        while   1 == 1:
            user_input = input("Enter command:  ")
            if user_input == "surrender":
                return "surrender"
            elif user_input == "wrong":    #      --- placeholder - input verification
                print("\n", "Wrong input placeholder message", "\n")
            else:
                return user_input


class MinMaxBot(Player):
    """Bot using MinMax algorithm with alpha-beta pruning"""

    def pass_control(self, boardstate):
        pass        #TO DO LATER
