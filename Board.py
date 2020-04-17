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
                    self.white_pieces.append(Man(Piece.WHITE, x, y))

        # Black pieces
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.black_pieces.append(Man(Piece.BLACK, x, y))

    def getPieces(self, color):
        if color == Piece.WHITE:
            return self.white_pieces
        else:
            return self.black_pieces

    def generateBitmap(self):
        """Creates board bitmap"""
        bitmap = [[None for columns in range(8)] for rows in range(8)]

        for white_piece, black_piece in itertools.zip_longest(self.white_pieces, self.black_pieces):
            if white_piece is not None:
                if not white_piece.captured:
                    bitmap[white_piece.x][white_piece.y] = white_piece.white
                else:
                    bitmap[white_piece.x][white_piece.y] = not white_piece.white

            if black_piece is not None:
                if not black_piece.captured:
                    bitmap[black_piece.x][black_piece.y] = black_piece.white
                else:
                    bitmap[black_piece.x][black_piece.y] = not black_piece.white

        return bitmap

    def generateBoardState(self):
        """Generates board state as 8x8 matrix"""
        grid = [[None for i in range(8)] for i in range(8)]

        for white_piece, black_piece in itertools.zip_longest(self.white_pieces, self.black_pieces):
            if white_piece is not None:
                grid[white_piece.x][white_piece.y] = white_piece

            if black_piece is not None:
                grid[black_piece.x][black_piece.y] = black_piece

        return grid

    def display(self):
        """Draws the board"""

        grid = self.generateBoardState()

        c = 0
        r = 7
        print("  ###################", end='')
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
                    print(" @", end='')
                else:
                    print(' ', grid[c][r].displayCharacter(), sep='', end='')
                c = c + 1
            print(" #", end='')
            r = r - 1
        print("\n", "  ###################", "\n", "    0 1 2 3 4 5 6 7")

    def clear_captured(self):
        """Removes captured pieces from the board"""

        for i in range(len(self.white_pieces) - 1, -1, -1):
            if self.white_pieces[i].captured:
                self.white_pieces.remove(self.white_pieces[i])

        for i in range(len(self.black_pieces) - 1, -1, -1):
            if self.black_pieces[i].captured:
                self.black_pieces.remove(self.black_pieces[i])
