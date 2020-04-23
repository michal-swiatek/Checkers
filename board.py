"""
    Authors: Michal Swiatek, Jan Wasilewski
    Github: https://github.com/michal-swiatek/Checkers
"""


import itertools

from pieces import Piece, Man


class Board:
    """
        Represents current board state

        Board holds all currently active pieces and generates representation
        of current game state
    """

    def __init__(self):
        """
            Initializes board with predefined set of pieces
        """

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
        """ Returns list of pieces of specified color """

        if color == Piece.WHITE:
            return self.white_pieces
        else:
            return self.black_pieces

    def generateBitmap(self):
        """
            Generates bitmap representation of current board state

            Bitmap consists of True/False values representing
            WHITE and BLACK pieces as well as None values that
            represent empty tile

        :return: 8x8 matrix
        """

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
        """
            Generates current board representation that holds all board info

            Builds an 8x8 grid holding pieces at their positions and None
            values representing empty tiles

        :return: 8x8 matrix
        """

        grid = [[None for i in range(8)] for i in range(8)]

        for white_piece, black_piece in itertools.zip_longest(self.white_pieces, self.black_pieces):
            if white_piece is not None:
                grid[white_piece.x][white_piece.y] = white_piece

            if black_piece is not None:
                grid[black_piece.x][black_piece.y] = black_piece

        return grid

    def display(self):
        """ Draws the board in console """

        grid = self.generateBoardState()

        row = 7
        print("   ###################", end='')
        while row >= 0:
            column = 0
            print("\n", row, "#", end='')
            while column < 8:
                if grid[column][row] is None:
                    if (row + column) % 2 == 0:
                        print(" +", end='')
                    else:
                        print(" .", end='')
                elif grid[column][row].captured:
                    print(" @", end='')
                else:
                    print(' ', grid[column][row].displayCharacter(), sep='', end='')
                column = column + 1
            print(" #", end='')
            row = row - 1
        print("\n", "  ###################", "\n", "    0 1 2 3 4 5 6 7")

    def clearCaptured(self):
        """ Removes captured pieces from the board """

        for i in range(len(self.white_pieces) - 1, -1, -1):
            if self.white_pieces[i].captured:
                self.white_pieces.remove(self.white_pieces[i])

        for i in range(len(self.black_pieces) - 1, -1, -1):
            if self.black_pieces[i].captured:
                self.black_pieces.remove(self.black_pieces[i])
