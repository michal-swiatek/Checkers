import Pieces

class Board:
    """Prepares and stores the board state."""
    def __init__(self):
        self.grid = [[None for columns in range(8)] for rows in range(8)]
        #placeholder
        self.grid[0][0] = Pieces.Man("white", 0, 0)
        self.grid[0][2] = Pieces.Man("white", 0, 2)
        self.grid[0][4] = Pieces.Man("white", 0, 4)
        self.grid[0][6] = Pieces.Man("white", 0, 6)
        self.grid[1][1] = Pieces.Man("white", 1, 1)
        self.grid[1][3] = Pieces.Man("white", 1, 3)
        self.grid[1][5] = Pieces.Man("white", 1, 5)
        self.grid[1][7] = Pieces.Man("white", 1, 7)
        self.grid[2][0] = Pieces.Man("white", 2, 0)
        self.grid[2][2] = Pieces.Man("white", 2, 2)
        self.grid[2][4] = Pieces.Man("white", 2, 4)
        self.grid[2][6] = Pieces.Man("white", 2, 6)
        self.grid[5][1] = Pieces.Man("black", 5, 1)
        self.grid[5][3] = Pieces.Man("black", 5, 3)
        self.grid[5][5] = Pieces.Man("black", 5, 5)
        self.grid[5][7] = Pieces.Man("black", 5, 7)
        self.grid[6][0] = Pieces.Man("black", 6, 0)
        self.grid[6][2] = Pieces.Man("black", 6, 2)
        self.grid[6][4] = Pieces.Man("black", 6, 4)
        self.grid[6][6] = Pieces.Man("black", 6, 6)
        self.grid[7][1] = Pieces.Man("black", 7, 1)
        self.grid[7][3] = Pieces.Man("black", 7, 3)
        self.grid[7][5] = Pieces.Man("black", 7, 5)
        self.grid[7][7] = Pieces.Man("black", 7, 7)

    def condense(self):
        """Placeholder name - creates board bitmap"""
        result = [[None for columns in range(8)] for rows in range(8)]
        c = 0
        r = 0
        while r < 8:
            c = 0
            while c < 8:
                if self.grid[r][c] != None:
                    result[r][c] = 1
                else:
                    result[r][c] = 0        #placeholder - debug purposes
                c = c + 1
            r = r + 1

        return result


    def display(self):
        """Draws the board"""
        c = 0
        r = 7
        print("\n", "  ###################", end='')
        while r >= 0:
            c = 0
            print("\n", r, "#", end='')
            while c < 8:
                if self.grid[r][c] == None:
                    if (r + c) % 2 == 0:
                        print(" +", end='')
                    else:
                        print(" .", end='')
                elif self.grid[r][c].alive != 1:
                    print(" *", end='')
                elif self.grid[r][c].owner == "white":
                    print(" @", end='')
                elif self.grid[r][c].owner == "black":
                    print(" %", end='')
                c = c + 1
            print(" #", end='')
            r = r - 1
        print("\n", "  ###################", "\n", "    0 1 2 3 4 5 6 7", "\n")

    def clear_captured(self):
        """Removes captured pieces from the board"""

        c = 0
        r = 0
        while r < 8:
            c = 0
            while c < 8:
                if self.grid[r][c] != None and self.grid[r][c].alive == 0:
                    self.grid[r][c] = None
                c = c + 1
            r = r + 1


#------------------------------------------------------------------------------------------------------------------------------------------

