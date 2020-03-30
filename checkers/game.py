"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek

    Last update: 30.03.2020
"""

import copy

import pygame

from board import Board
from piece import King
import player


class Game:

    def __init__(self, width: int = 640, height: int = 480):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((width, height))

        #
        # Game
        #
        self.board = Board(width, height)

        # Players
        self.white_player = player.Human(Board.WHITE)
        self.red_player = player.Human(Board.RED)

        self.turn = Board.WHITE

        # Multiple capture
        self.captured_pieces = []
        self.capturing_piece = None

        # Animation
        self.held_piece = None

    def __del__(self):
        pygame.quit()

    def mainLoop(self):
        while self.running:
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                #
                # Animation
                #
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != pygame.BUTTON_LEFT:
                        continue

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = self.board.screenToGrid(mouse_x, mouse_y)

                    # Take piece off board
                    try:
                        self.held_piece = self.board.board_state[grid_x][grid_y]
                    except IndexError:
                        pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button != pygame.BUTTON_LEFT or self.held_piece is None:
                        continue

                    # Pass copy to players
                    if self.turn == Board.WHITE:
                        self.white_player.held_piece = copy.copy(self.held_piece)
                    elif self.turn == Board.RED:
                        self.red_player.held_piece = copy.copy(self.held_piece)

                    self.held_piece.screen_x = self.held_piece.grid_x * self.board.tile_size + self.board.tile_offset
                    self.held_piece.screen_y = self.held_piece.grid_y * self.board.tile_size

                    # Put piece back
                    self.held_piece = None
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Update held piece position
                    if self.held_piece is not None:
                        self.held_piece.screen_x = mouse_x - int(self.board.tile_size / 2)
                        self.held_piece.screen_y = mouse_y - int(self.board.tile_size / 2)

            # Game logic
            self.update()

            # Drawing
            self.screen.fill((255, 255, 255))  # White

            self.board.show(self.screen, self.held_piece)

            # Show held piece
            if self.held_piece is not None:
                self.held_piece.show(self.screen)

            pygame.display.update()

    def update(self):
        move = None

        if self.turn == Board.WHITE:
            move = self.white_player.makeMove(self.board)
        elif self.turn == Board.RED:
            move = self.red_player.makeMove(self.board)

        if self.validMove(move):
            self.movePiece(move)

            capture = self.checkCapture(move)

            if capture is not None:
                self.captured_pieces.append(capture)
                capturing_piece = self.board.board_state[move[2]][move[3]]  # x2, y2

                # Check if this piece can continue capture
                bitmap = self.board.getBoardBitmap(self.captured_pieces, self.turn)
                moves, captures = capturing_piece.generatePossibleMoves(bitmap, True)

                if len(captures) != 0:
                    self.capturing_piece = capturing_piece
                else:
                    self.capturing_piece = None

            # At the end of capture clear the table and change turns
            if self.capturing_piece is None:
                for capture in self.captured_pieces:
                    x, y = capture
                    self.board.board_state[x][y] = None

                self.captured_pieces = []
                self.turn = not self.turn

    def validMove(self, move):
        if move is None:
            return False

        # Multiple capture, only this piece can move
        if self.capturing_piece is not None:
            bitmap = self.board.getBoardBitmap(self.captured_pieces, self.turn)
            moves, captures = self.capturing_piece.generatePossibleMoves(bitmap, True)

            for capture in captures:
                if move == capture:
                    return True

            return False

        white_moves, red_moves = self.board.getPossibleMoves()

        if self.turn == Board.WHITE:
            for valid_move in white_moves:
                if move == valid_move:
                    return True
        elif self.turn == Board.RED:
            for valid_move in red_moves:
                if move == valid_move:
                    return True

        return False

    def checkCapture(self, move):
        x1, y1, x2, y2 = move
        dir_x = int((x2 - x1) / abs(x2 - x1))
        dir_y = int((y2 - y1) / abs(y2 - y1))

        enemy_piece = not self.turn

        while x1 != x2 and y1 != y2:
            x1 += dir_x
            y1 += dir_y

            piece = self.board.board_state[x1][y1]
            if piece and piece.white == enemy_piece:
                return x1, y1

        return None

    def movePiece(self, move):
        x1, y1, x2, y2 = move

        piece = self.board.board_state[x1][y1]

        # Transform to King if reached end of table
        if (piece.white and y2 == 0) or (not piece.white and y2 == Board.DIMENSIONS - 1):
            piece = King(None, None, None, None, self.board.tile_size, piece.white)

        piece.grid_x = x2
        piece.grid_y = y2

        piece.screen_x = x2 * self.board.tile_size + self.board.tile_offset
        piece.screen_y = y2 * self.board.tile_size

        self.board.board_state[x2][y2] = piece
        self.board.board_state[x1][y1] = None
