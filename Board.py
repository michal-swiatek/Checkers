import itertools

from Pieces import Piece, Man, King


class Board:
    """Prepares and stores the board state."""
    def __init__(self):
        self.white_pieces = []
        self.black_pieces = []

        # White pieces
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.white_pieces.append(Man(Piece.WHITE, y, x))

        # Black pieces
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.white_pieces.append(Man(Piece.BLACK, y, x))

    def generateBitmap(self):
        """Creates board bitmap"""
        bitmap = [[None for columns in range(8)] for rows in range(8)]

        for piece in self.white_pieces:
            if not piece.captured:
                bitmap[piece.column][piece.row] = piece.white
            else:
                bitmap[piece.column][piece.row] = not piece.white

        for piece in self.black_pieces:
            if not piece.captured:
                bitmap[piece.column][piece.row] = piece.white
            else:
                bitmap[piece.column][piece.row] = not piece.white

        return bitmap

    def generateBoardState(self):
        """Generates board state as 8x8 matrix"""
        grid = [[None for i in range(8)] for i in range(8)]

        for white_piece, black_piece in itertools.zip_longest(self.white_pieces, self.black_pieces):
            if white_piece is not None:
                grid[white_piece.column][white_piece.row] = white_piece
            if black_piece is not None:
                grid[black_piece.column][black_piece.row] = black_piece

        return grid

    def display(self):
        """Draws the board"""

        grid = self.generateBoardState()

        c = 0
        r = 7
        print("\n", "  ###################", end='')
        while r >= 0:
            c = 0
            print("\n", r, "#", end='')
            while c < 8:
                if grid[c][r] is None:
                    if (r + c) % 2 == 0:
                        print(" +", end='')
                    else:
                        print(" .", end='')
                elif grid[c][r].captured:
                    print(" *", end='')
                elif not grid[c][r].white:
                    print(" %", end='')
                elif grid[c][r].white:
                    print(" @", end='')
                c = c + 1
            print(" #", end='')
            r = r - 1
        print("\n", "  ###################", "\n", "    0 1 2 3 4 5 6 7", "\n")

    def clear_captured(self):
        """Removes captured pieces from the board"""

        pass    # TODO: Implement


#------------------------------------------------------------------------------------------------------------------------------------------

