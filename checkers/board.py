"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek
    Last update: 31.03.2020
"""

import copy

import pygame

from piece import Pawn


class Board:

    DIMENSIONS: int = 8
    STARTING_ROWS: int = 3

    WHITE: bool = True
    RED: bool = False

    def __init__(self, width, height):
        self.board_state = [[None for i in range(Board.DIMENSIONS)] for i in range(Board.DIMENSIONS)]

        self.tile_size = int(height / Board.DIMENSIONS)
        self.tile_offset = int((width - 8 * self.tile_size) / 2)

        # White pieces
        for y in range(Board.DIMENSIONS - Board.STARTING_ROWS, Board.DIMENSIONS):
            for x in range((y + 1) % 2, Board.DIMENSIONS, 2):
                screen_x = x * self.tile_size + self.tile_offset
                screen_y = y * self.tile_size
                self.board_state[x][y] = Pawn(x, y, screen_x, screen_y, self.tile_size, Board.WHITE)

        # Red pieces
        for y in range(0, Board.STARTING_ROWS):
            for x in range((y + 1) % 2, Board.DIMENSIONS, 2):
                screen_x = x * self.tile_size + self.tile_offset
                screen_y = y * self.tile_size
                self.board_state[x][y] = Pawn(x, y, screen_x, screen_y, self.tile_size, Board.RED)

    def getPieces(self, color: bool):
        pieces = []

        for x in range(Board.DIMENSIONS):
            for y in range(Board.DIMENSIONS):
                piece = self.board_state[x][y]
                if piece is not None and piece.white == color:
                    pieces.append(copy.copy(piece))

        return pieces

    def getBoardBitmap(self, captured_pieces=None, captured_color=True):
        if captured_pieces is None:
            captured_pieces = []

        board_state = [[None for i in range(Board.DIMENSIONS)] for i in range(Board.DIMENSIONS)]
        for x in range(Board.DIMENSIONS):
            for y in range(Board.DIMENSIONS):
                if self.board_state[x][y] is not None:
                    board_state[x][y] = self.board_state[x][y].white

        for piece in captured_pieces:
            x, y = piece
            board_state[x][y] = captured_color

        return board_state

    def getPossibleMoves(self) -> (([], []), ([], [])):
        white_moves = []
        white_captures = []

        red_moves = []
        red_captures = []

        bitmap = self.getBoardBitmap()
        white_pieces = self.getPieces(Board.WHITE)
        red_pieces = self.getPieces(Board.RED)

        for piece in white_pieces:
            only_captures = len(white_captures) != 0

            moves, captures = piece.generatePossibleMoves(bitmap, only_captures)

            if only_captures or len(captures) != 0:
                white_captures.extend(captures)
            else:
                white_moves.extend(moves)

        for piece in red_pieces:
            only_captures = len(red_captures) != 0

            moves, captures = piece.generatePossibleMoves(bitmap, only_captures)

            if only_captures or len(captures) != 0:
                red_captures.extend(captures)
            else:
                red_moves.extend(moves)

        if len(white_captures) != 0:
            white_moves = white_captures
        if len(red_captures) != 0:
            red_moves = red_captures

        return white_moves, red_moves

    def getValidMoves(self, pieces, captured_pieces=None, captured_color=True):
        valid_moves = []
        captures = []

        bitmap = self.getBoardBitmap(captured_pieces, captured_color)

        for piece in pieces:
            only_captures = len(captures) != 0

            moves, captures = piece.generatePossibleMoves(bitmap, only_captures)

            if only_captures or len(captures) != 0:
                captures.extend(captures)
            else:
                valid_moves.extend(moves)

        return valid_moves, captures

    #
    # Drawing
    #
    def show(self, screen, held_piece=None):
        # Draw board
        for x in range(Board.DIMENSIONS):
            for y in range(Board.DIMENSIONS):
                if (x + y) % 2 == 1:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)

                x_coord = int(x * self.tile_size + self.tile_offset)
                y_coord = int(y * self.tile_size)

                # Draw checker pattern
                pygame.draw.rect(screen, color, (x_coord, y_coord, self.tile_size, self.tile_size))

        # Draw pieces
        for x in range(Board.DIMENSIONS):
            for y in range(Board.DIMENSIONS):
                piece = self.board_state[x][y]
                if held_piece is None and piece is not None:
                    piece.show(screen)
                elif held_piece is not None and piece is not None and piece != held_piece:
                    piece.show(screen)

        # Draw outline
        pygame.draw.rect(screen, (0, 0, 0), (self.tile_offset, 0, 8 * self.tile_size, 8 * self.tile_size), 4)

    def screenToGrid(self, screen_x, screen_y):
        grid_x = int((screen_x - self.tile_offset) / self.tile_size)
        grid_y = int(screen_y / self.tile_size)

        return grid_x, grid_y

    def gridToScreen(self, grid_x, grid_y):
        screen_x = int(grid_x * self.tile_size + self.tile_offset)
        screen_y = int(grid_y * self.tile_size)

        return screen_x, screen_y
