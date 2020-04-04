class Man:
    """Standard piece"""

    def __init__(self, initial_owner, initial_row, initial_column):
        self.owner = initial_owner
        self.row = initial_row
        self.column = initial_column
        self.alive = 1


class King(Man):
    """Promoted piece"""

#---------------------------------------------------------------------------------