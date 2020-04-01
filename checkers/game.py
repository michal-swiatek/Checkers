"""
    Created by michal-swiatek on 29.03.2020
    Github: https://github.com/michal-swiatek
    Last update: 31.03.2020
"""

import copy

import pygame

import player
from board import Board
from piece import King


class Game:
    FILL_COLOR = 218, 165, 32  # goldenrod

    FONT_SIZE: int = 30
    TEXT_COLOR = 0, 0, 0  # black

    def __init__(self, width: int = 640, height: int = 480):
        pygame.init()
        pygame.font.init()

        self.running = True
        self.screen = pygame.display.set_mode((width, height))

        #
        # Game
        #
        self.game_finished = False

        self.board = Board(width, height)

        # Players
        self.white_player = player.Minimax(Board.WHITE)
        self.red_player = player.Human(Board.RED)

        # Available moves (including players turns)
        self.valid_moves = []

        self.turn = Board.WHITE

        # Multiple capture
        self.captured_pieces = []
        self.capturing_piece = None

        # Animation
        self.held_piece = None

        # Info display
        self.font = pygame.font.SysFont("Arial", Game.FONT_SIZE, True)

        self.turn_texture = self.font.render("Turn: ", False, Game.TEXT_COLOR)
        self.white_texture = self.font.render("WHITE", False, Game.TEXT_COLOR)
        self.red_texture = self.font.render("RED", False, Game.TEXT_COLOR)
        self.wins_texture = self.font.render("WINS!", False, Game.TEXT_COLOR)

        self.updateValidMoves()

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

                    if not self.canBeHighlighted(grid_x, grid_y) or self.game_finished:
                        continue

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

            #
            # Game logic
            #
            if not self.game_finished:
                self.update()

            # Drawing
            self.screen.fill(Game.FILL_COLOR)

            self.board.show(self.screen, self.held_piece)

            if not self.game_finished:
                self.showPossibleMoves()
                self.showHints()

            self.showGameInfo()

            # Show held piece
            if self.held_piece is not None:
                self.held_piece.show(self.screen)

            pygame.display.update()

    def update(self):
        move = None

        # Get move from player
        if self.turn == Board.WHITE:
            move = self.white_player.makeMove(self.board, self.held_piece, self.captured_pieces, self.capturing_piece)
        elif self.turn == Board.RED:
            move = self.red_player.makeMove(self.board, self.held_piece, self.captured_pieces, self.capturing_piece)

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

                if self.turn == Board.RED and not self.red_player.human:
                    pygame.time.delay(500)
                elif self.turn == Board.WHITE and not self.white_player.human:
                    pygame.time.delay(500)

            # At the end of capture clear the table and change turns
            if self.capturing_piece is None:
                for capture in self.captured_pieces:
                    x, y = capture
                    self.board.board_state[x][y] = None

                self.captured_pieces = []
                self.turn = not self.turn

            self.updateValidMoves()

        if len(self.valid_moves) == 0:
            self.game_finished = True

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

        self.updateValidMoves()

        for valid_move in self.valid_moves:
            if move == valid_move:
                return True

        return False

    def updateValidMoves(self):
        # Multiple capture
        if len(self.captured_pieces) != 0:
            bitmap = self.board.getBoardBitmap(self.captured_pieces, self.turn)
            moves, captures = self.capturing_piece.generatePossibleMoves(bitmap, True)

            self.valid_moves = captures
        else:
            white_moves, red_moves = self.board.getPossibleMoves()

            if self.turn == Board.WHITE:
                self.valid_moves = white_moves
            elif self.turn == Board.RED:
                self.valid_moves = red_moves

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

    def showPossibleMoves(self):
        for move in self.valid_moves:
            x1, y1, x2, y2 = move

            x = x2 * self.board.tile_size + self.board.tile_offset
            y = y2 * self.board.tile_size

            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.board.tile_size, self.board.tile_size), 2)

    def showHints(self):
        if self.held_piece is None or not self.canBeHighlighted(self.held_piece.grid_x, self.held_piece.grid_y):
            return

        bitmap = self.board.getBoardBitmap(self.captured_pieces, self.turn)
        moves, captures = self.held_piece.generatePossibleMoves(bitmap)

        if len(captures) != 0:
            moves = captures

        for move in moves:
            if move not in self.valid_moves:
                continue

            x1, y1, x2, y2 = move

            x = x2 * self.board.tile_size + self.board.tile_offset
            y = y2 * self.board.tile_size

            pygame.draw.rect(self.screen, (255, 255, 0), (x, y, self.board.tile_size, self.board.tile_size), 4)

    def canBeHighlighted(self, piece_x, piece_y):
        if len(self.valid_moves) == 0:
            return True

        for move in self.valid_moves:
            x1, y1, x2, y2 = move

            if piece_x == x1 and piece_y == y1:
                return True

        return False

    def showGameInfo(self):
        turn_x = Board.TEXT_WIDTH + Board.DIMENSIONS * self.board.tile_size + 10
        turn_y = 15

        self.screen.blit(self.turn_texture, (turn_x, turn_y))

        turn_x += self.turn_texture.get_size()[0]

        if self.turn == Board.WHITE:
            self.screen.blit(self.white_texture, (turn_x, turn_y + 1))
        elif self.turn == Board.RED:
            self.screen.blit(self.red_texture, (turn_x, turn_y + 1))

        # Show game result
        if self.game_finished:
            if self.turn == Board.WHITE:
                winner_texture = self.red_texture
            elif self.turn == Board.RED:
                winner_texture = self.white_texture

            texture_x = Board.TEXT_WIDTH + Board.DIMENSIONS * self.board.tile_size + 10
            texture_y = 100

            self.screen.blit(winner_texture, (texture_x, texture_y))
            self.screen.blit(self.wins_texture, (texture_x + winner_texture.get_size()[0] + 5, texture_y))
