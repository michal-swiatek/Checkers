class Piece:
    """Base piece class"""

    WHITE: bool = True
    BLACK: bool = False

    def __init__(self, white, initial_row, initial_column):
        self.white = white
        self.row = initial_row
        self.column = initial_column
        self.captured = False

    def generateValidMoves(self, board_bitmap):
        pass


class Man(Piece):
    """Standard piece"""

    def generateValidMoves(self, bitmap: [[bool]], only_captures: bool = False) -> ([()], [()]):
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
        x = self.column + 2 * dir_x
        y = self.row + 2 * dir_y
        dimensions = len(bitmap)

        # Check capture
        if 0 <= x < dimensions and 0 <= y < dimensions and bitmap[x][y] is None:
            if bitmap[x - dir_x][y - dir_y] is not None and bitmap[x - dir_x][y - dir_y] is not self.white:
                captures.append((self.column, self.row, x, y))
                only_captures = True

        # Only captures are allowed backwards
        if (self.white and dir_y > 0) or (not self.white and dir_y < 0):
            return

        x = self.column + dir_x
        y = self.row + dir_y

        # Check move
        if not only_captures and 0 <= x < dimensions and 0 <= y < dimensions and bitmap[x][y] is None:
            moves.append((self.column, self.row, x, y))


class King(Man):
    """Promoted piece"""

    def checkDirection(self, bitmap, moves, captures, only_captures: bool, dir_x: int, dir_y: int) -> None:
        x = self.column + dir_x
        y = self.row + dir_y
        dimensions = len(bitmap)

        capturing = False

        while 0 <= x < dimensions and 0 <= y < dimensions:
            if bitmap[x][y] is None:
                if capturing:
                    captures.append((self.column, self.row, x, y))
                elif not only_captures:
                    moves.append((self.column, self.row, x, y))
            elif bitmap[x][y] is not self.white:
                if not capturing:
                    capturing = True
                else:
                    break
            elif bitmap[x][y] is self.white:
                break

            x += dir_x
            y += dir_y
