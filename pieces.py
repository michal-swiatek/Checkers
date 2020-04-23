"""
    Authors: Michal Swiatek, Jan Wasilewski
    Github: https://github.com/michal-swiatek/Checkers
"""


class Piece:
    """
        Base piece class

        Holds piece color, position on the board and information
        whether the piece is captured
    """

    WHITE: bool = True
    BLACK: bool = False

    def __init__(self, white, x, y):
        self.white = white

        self.x = x
        self.y = y

        self.captured = False

    def generateValidMoves(self, board_bitmap, only_captures: bool = False) -> ([()], [()]):
        """
            Generates a list of possible moves given a specific board bitmap

            All moves generated are valid and obey game rules

        :param board_bitmap: current board state represented as bitmap
        :param only_captures: flag specifying to ignore normal moves
        :return: list of valid moves
        """
        pass

    def displayCharacter(self):
        """
            Defines printable character of a piece

        :return: character
        """
        pass


class Man(Piece):
    """
        Standard checkers piece

        Man can move only forward, when end of the board is reached Man
        gets promoted and becomes a King
        Man can capture adjacent enemy pieces in any of four directions
        if a tile directly behind them is empty
    """

    def generateValidMoves(self, bitmap: [[bool]], only_captures: bool = False) -> ([()], [()]):
        """ Generates Man valid moves """

        moves = []
        captures = []

        # Left up
        self.checkDirection(bitmap, moves, captures, only_captures or len(captures) != 0, -1, -1)
        # Left down
        self.checkDirection(bitmap, moves, captures, only_captures or len(captures) != 0, -1, 1)
        # Right up
        self.checkDirection(bitmap, moves, captures, only_captures or len(captures) != 0, 1, -1)
        # Right down
        self.checkDirection(bitmap, moves, captures, only_captures or len(captures) != 0, 1, 1)

        if only_captures or len(captures) != 0:
            return [], captures
        else:
            return moves, []

    def checkDirection(self, bitmap, moves, captures, only_captures: bool, dir_x: int, dir_y: int):
        """
            Helper function that checks all possible moves in specific direction

            If captures have been detected only_capture flag is set True and normal
            moves are ignored - Player has to capture enemy piece if possible

        :param bitmap: current board bitmap representation
        :param moves: reference to list of possible moves
        :param captures: reference to lis of possible captures
        :param only_captures: flag specifying whether normal moves should be accounted
        :param dir_x: x direction of movement
        :param dir_y: y direction of movement
        :return: None
        """

        x = self.x + 2 * dir_x
        y = self.y + 2 * dir_y
        dimensions = len(bitmap)

        # Check capture
        if 0 <= x < dimensions and 0 <= y < dimensions and bitmap[x][y] is None:
            if bitmap[x - dir_x][y - dir_y] is not None and bitmap[x - dir_x][y - dir_y] is not self.white:
                captures.append((self.x, self.y, x, y, x - dir_x, y - dir_y))
                only_captures = True

        # Only captures are allowed backwards
        if (self.white and dir_y < 0) or (not self.white and dir_y > 0):
            return

        x = self.x + dir_x
        y = self.y + dir_y

        # Check move
        if not only_captures and 0 <= x < dimensions and 0 <= y < dimensions and bitmap[x][y] is None:
            moves.append((self.x, self.y, x, y, None, None))

    def displayCharacter(self):
        """ Lower case letter represent Man """

        if self.white:
            return 'w'
        else:
            return 'b'


class King(Man):
    """
        Promoted piece

        King can move any number of tiles in any of four directions and can
        capture pieces that are not adjacent to it. After capture it can land
        on any empty tile as long as there is no other pieces between captured
        piece and destination tile
    """

    def checkDirection(self, bitmap, moves, captures, only_captures: bool, dir_x: int, dir_y: int) -> None:
        """ King implementation of move generation """

        x = self.x + dir_x
        y = self.y + dir_y
        dimensions = len(bitmap)

        capturing = None

        while 0 <= x < dimensions and 0 <= y < dimensions:
            if bitmap[x][y] is None:
                if capturing is not None:
                    captures.append((self.x, self.y, x, y, capturing[0], capturing[1]))
                elif not only_captures:
                    moves.append((self.x, self.y, x, y, None, None))
            elif bitmap[x][y] is not self.white:
                if capturing is None:
                    capturing = x, y
                else:
                    break
            elif bitmap[x][y] is self.white:
                break

            x += dir_x
            y += dir_y

    def displayCharacter(self):
        """ Upper case letter represent King """

        if self.white:
            return 'W'
        else:
            return 'B'
