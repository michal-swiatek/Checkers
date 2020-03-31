"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek
    Last update: 30.03.2020
"""

import random


class Player:

    def __init__(self, color: bool):
        self.color = color

    # Complete game info
    def makeMove(self, board, held_piece=None, captured_pieces=None):
        pass


class Human(Player):

    def __init__(self, color: bool):
        super(Human, self).__init__(color)

        self.held_piece = None

    def makeMove(self, board, held_piece=None, captured_pieces=None):
        if held_piece is None and self.held_piece is not None:
            piece = self.held_piece
            radius = int(board.tile_size / 2)

            self.held_piece = None

            new_x, new_y = board.screenToGrid(piece.screen_x + radius, piece.screen_y + radius)
            players_move = piece.grid_x, piece.grid_y, new_x, new_y

            return players_move
        else:
            self.held_piece = held_piece
            return None


class SimpleAI(Player):

    def makeMove(self, board, held_piece=None, captured_pieces=None):
        pieces = board.getPieces(self.color)
        bitmap = board.getBoardBitmap(captured_pieces, self.color)

        moves = self.generateValidMoves(pieces, bitmap)
        move = random.choice(moves)

        return move

    def generateValidMoves(self, pieces, bitmap):
        valid_moves = []
        valid_captures = []

        for piece in pieces:
            moves, captures = piece.generatePossibleMoves(bitmap, len(valid_captures) != 0)

            if len(captures) != 0:
                valid_captures.extend(captures)
            else:
                valid_moves.extend(moves)

        if len(valid_captures) != 0:
            valid_moves = valid_captures

        return valid_moves
