class Piece:
    """Base piece class"""

    WHITE: bool = True
    BLACK: bool = False

    def __init__(self, white, x, y):
        self.white = white

        self.x = x
        self.y = y

        self.captured = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def generateValidMoves(self, board_bitmap):
        pass

    def displayCharacter(self):
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
        if self.white:
            return 'w'
        else:
            return 'b'


class King(Man):
    """Promoted piece"""

    def checkDirection(self, bitmap, moves, captures, only_captures: bool, dir_x: int, dir_y: int) -> None:
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
        if self.white:
            return 'W'
        else:
            return 'B'
