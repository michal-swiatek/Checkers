"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek
    Last update: 30.03.2020
"""

import pygame


class Piece:
    DRAW_BIAS: int = 5

    def __init__(self, grid_x, grid_y, screen_x, screen_y, tile_size, white):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.white = white

        # Drawing
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.tile_size = tile_size

    def __eq__(self, other):
        return self.grid_x == other.grid_x and self.grid_y == other.grid_y

    def show(self, screen) -> None:
        pass

    def generatePossibleMoves(self, bitmap: [[bool]], only_captures: bool = False) -> ([()], [()]):
        pass

    def getScore(self):
        pass


class Pawn(Piece):

    def show(self, screen):
        if self.white:
            color = (255, 255, 255)
        else:
            color = (255, 0, 0)

        radius = int(self.tile_size / 2)

        x = self.screen_x + radius
        y = self.screen_y + radius

        pygame.draw.circle(screen, color, (x, y), radius - Piece.DRAW_BIAS)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), radius - Piece.DRAW_BIAS, 1)

    def generatePossibleMoves(self, bitmap: [[bool]], only_captures: bool = False) -> ([()], [()]):
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
        x = self.grid_x + 2 * dir_x
        y = self.grid_y + 2 * dir_y
        dimensions = len(bitmap)

        # Check capture
        if 0 <= x < dimensions and 0 <= y < dimensions and bitmap[x][y] is None:
            if bitmap[x - dir_x][y - dir_y] is not None and bitmap[x - dir_x][y - dir_y] is not self.white:
                captures.append((self.grid_x, self.grid_y, x, y))
                only_captures = True

        # Only captures are allowed backwards
        if (self.white and dir_y > 0) or (not self.white and dir_y < 0):
            return

        x = self.grid_x + dir_x
        y = self.grid_y + dir_y

        # Check move
        if not only_captures and 0 <= x < dimensions and 0 <= y < dimensions and bitmap[x][y] is None:
            moves.append((self.grid_x, self.grid_y, x, y))

    def getScore(self, bitmap):
        moves, captures = self.generatePossibleMoves(bitmap)

        if len(captures) != 0:
            moves = captures

        return len(moves)


class King(Pawn):

    def show(self, screen):
        super(King, self).show(screen)

        radius = int(self.tile_size / 2)

        x = self.screen_x + radius
        y = self.screen_y + radius

        pygame.draw.circle(screen, (0, 0, 0), (x, y), int(radius / 1.5) - Piece.DRAW_BIAS, 1)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), int(radius / 2) - Piece.DRAW_BIAS, 1)

    def checkDirection(self, bitmap, moves, captures, only_captures: bool, dir_x: int, dir_y: int) -> None:
        x = self.grid_x + dir_x
        y = self.grid_y + dir_y
        dimensions = len(bitmap)

        capturing = False

        while 0 <= x < dimensions and 0 <= y < dimensions:
            if bitmap[x][y] is None:
                if capturing:
                    captures.append((self.grid_x, self.grid_y, x, y))
                elif not only_captures:
                    moves.append((self.grid_x, self.grid_y, x, y))
            elif bitmap[x][y] is not self.white:
                if not capturing:
                    capturing = True
                else:
                    break
            elif bitmap[x][y] is self.white:
                break

            x += dir_x
            y += dir_y
