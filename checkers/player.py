"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek
    Last update: 30.03.2020
"""


class Player:

    def __init__(self, color: bool):
        self.color = color

        self.held_piece = None

    def makeMove(self, board):
        pass


class Human(Player):

    def makeMove(self, board):
        if self.held_piece is not None:
            piece = self.held_piece
            radius = int(board.tile_size / 2)

            self.held_piece = None

            new_x, new_y = board.screenToGrid(piece.screen_x + radius, piece.screen_y + radius)
            players_move = piece.grid_x, piece.grid_y, new_x, new_y

            return players_move
        else:
            return None