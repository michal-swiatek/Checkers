"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek
    Last update: 30.03.2020
"""

import random
import math

from board import Board
from piece import King, Pawn


class Player:

    def __init__(self, color: bool):
        self.color = color

        self.human = None

    # Complete game info
    def makeMove(self, board, held_piece=None, captured_pieces=None, capturing_piece=None):
        pass


class Human(Player):

    def __init__(self, color: bool):
        super(Human, self).__init__(color)

        self.held_piece = None
        self.human = True

    def makeMove(self, board, held_piece=None, captured_pieces=None, capturing_piece=None):
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

    def __init__(self, color: bool):
        super(SimpleAI, self).__init__(color)

        self.human = False

    def makeMove(self, board, held_piece=None, captured_pieces=None, capturing_piece=None):
        pieces = board.getPieces(self.color)
        bitmap = board.getBoardBitmap(captured_pieces, self.color)

        moves, captures = self.generateValidMoves(pieces, bitmap, capturing_piece)
        if len(captures) != 0:
            moves = captures

        move = random.choice(moves)

        return move

    def generateValidMoves(self, pieces, bitmap, capturing_piece=None):
        if capturing_piece is not None:
            moves, captures = capturing_piece.generatePossibleMoves(bitmap, True)

            return [], captures

        valid_moves = []
        valid_captures = []

        for piece in pieces:
            moves, captures = piece.generatePossibleMoves(bitmap, len(valid_captures) != 0)

            if len(captures) != 0:
                valid_captures.extend(captures)
            else:
                valid_moves.extend(moves)

        return valid_moves, valid_captures


class Minimax(SimpleAI):

    MAX_MOVES: int = 100
    STATIC_POINTS: int = 10

    def makeMove(self, board, held_piece=None, captured_pieces=None, capturing_piece=None):
        _, moves = self.minimax(board, captured_pieces, capturing_piece, 8)
        return random.choice(moves)

    def minimax(self, board, captured_pieces, capturing_piece, depth=1, sign=1, alpha=-math.inf, beta=math.inf):
        if depth <= 0:
            return self.evaluateBoard(board, captured_pieces), []

        if sign > 0:
            color = self.color
        else:
            color = not self.color

        moves, captures = self.generateMoves(board, captured_pieces, capturing_piece, color)
        if len(captures) != 0:
            moves = captures

        if len(moves) > Minimax.MAX_MOVES:
            depth /= 2

        # Minimax
        best_evaluation = -math.inf
        best_moves = []
        for move in moves:
            capturing_piece, captured_piece = self.doMove(board, captured_pieces, color, move, len(captures) != 0)

            if capturing_piece is not None:
                evaluation, _ = self.minimax(board, captured_pieces, capturing_piece, depth - 1, sign, alpha, beta)
            else:
                evaluation, _ = self.minimax(board, [], None, depth - 1, -sign, alpha, beta)

            evaluation *= sign

            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_moves = [move]
            elif evaluation == best_evaluation:
                best_moves.append(move)

            self.undoMove(board, captured_pieces, captured_piece, color, move)

            # Alpha beta pruning
            if sign > 0 and best_evaluation > alpha:
                alpha = best_evaluation
            elif sign < 0 and best_evaluation < beta:
                beta = best_evaluation

            if beta <= alpha:
                break

        return sign * best_evaluation, best_moves

    def generateMoves(self, board, captured_pieces, capturing_piece, color):
        if capturing_piece is not None:
            bitmap = board.getBoardBitmap(captured_pieces, color)
            return capturing_piece.generatePossibleMoves(bitmap, True)
        else:
            pieces = board.getPieces(color)
            bitmap = board.getBoardBitmap()

            return self.generateValidMoves(pieces, bitmap)

    def evaluateBoard(self, board, captured_pieces):
        white_pieces = board.getPieces(True)
        red_pieces = board.getPieces(False)

        white_bitmap = board.getBoardBitmap(captured_pieces, True)
        red_bitmap = board.getBoardBitmap(captured_pieces, False)

        white_score = 0
        red_score = 0

        for piece in white_pieces:
            white_score += 2 * piece.getScore(white_bitmap) + (Board.DIMENSIONS - piece.grid_y) + Minimax.STATIC_POINTS
        for piece in red_pieces:
            red_score += 2 * piece.getScore(red_bitmap) + piece.grid_y + Minimax.STATIC_POINTS

        final_score = 0
        if self.color == Board.WHITE:
            final_score = white_score - red_score
        elif self.color == Board.RED:
            final_score = red_score - white_score

        return final_score

    def doMove(self, board, captured_pieces, color, move, capture_occured):
        self.movePiece(board, color, move)

        if capture_occured:
            x, y, captured_piece = self.capturePiece(board, move, not color)
            captured_pieces.append((x, y))

            # Check for multiple capture
            capturing_piece = board.board_state[move[2]][move[3]]  # x2, y2

            bitmap = board.getBoardBitmap(captured_pieces, color)
            moves, captures = capturing_piece.generatePossibleMoves(bitmap, True)

            if len(captures) != 0:
                return capturing_piece, captured_piece
            else:
                return None, captured_piece

        return None, None

    def undoMove(self, board, captured_pieces, captured_piece, color, move):
        self.movePiece(board, color, move, undo=True)

        if captured_piece is not None:
            captured_pieces.pop()

            # Put piece back
            board.board_state[captured_piece.grid_x][captured_piece.grid_y] = captured_piece

    def movePiece(self, board, color, move, undo=False):
        if undo:
            x2, y2, x1, y1 = move
        else:
            x1, y1, x2, y2 = move

        piece = board.board_state[x1][y1]

        piece.grid_x = x2
        piece.grid_y = y2

        board.board_state[x1][y1] = None
        board.board_state[x2][y2] = piece

    def capturePiece(self, board, move, enemy_piece):
        x1, y1, x2, y2 = move

        dir_x = int((x2 - x1) / abs(x2 - x1))
        dir_y = int((y2 - y1) / abs(y2 - y1))

        while x1 != x2 and y1 != y2:
            x1 += dir_x
            y1 += dir_y

            piece = board.board_state[x1][y1]
            if piece and piece.white == enemy_piece:
                # Take piece off board
                board.board_state[x1][y1] = None
                return x1, y1, piece

        return None
