import Board
import Pieces
import Players
import copy
import heuristics


class Game:
    """
        Represent single game instance

        Holds game info as current board state, currently capturing piece
        and implements game logic such as move validation and performing,
        control flow, surrender/game over.
    """

    def __init__(self):
        self.running = True

        self.board = Board.Board()  # current game state

        self.white_player = None
        self.black_player = None
        self.initPlayers()

        self.current_player = Pieces.Piece.WHITE

        self.capturing_piece = None

    def mainLoop(self):
        while self.running:
            # Get next move from player
            if self.current_player == Pieces.Piece.WHITE:
                next_move = self.white_player.pass_control(self.board, self.capturing_piece)
            else:
                next_move = self.black_player.pass_control(copy.deepcopy(self.board), self.capturing_piece)

            # Check whether it is a valid surrender or game over
            if next_move == Players.Player.SURRENDER:
                if self.current_player == Pieces.Piece.WHITE:
                    print("Black player wins! (White surrendered)")
                else:
                    print("White player wins! (Black surrendered)")

                self.running = False
            elif next_move == Players.Player.GAME_OVER:
                if self.current_player == Pieces.Piece.WHITE:
                    print("\nBlack player wins!\n")
                    self.board.display()
                else:
                    print("\nWhite player wins!\n")
                    self.board.display()

                self.running = False
            else:
                # If move is valid perform it
                self.updateBoard(next_move)

                # Pass control to other player only if no more chained capture are possible
                if self.capturing_piece is None:
                    self.current_player = not self.current_player

    def updateBoard(self, move):
        """
            Updates board state by performing specified move

        :param move: move formatted as tuple containing 6 integers
        :return: None
        """

        x1, y1, x2, y2, capture_x, capture_y = move
        pieces = self.board.getPieces(self.current_player)

        for i, piece in enumerate(pieces):
            if x1 == piece.x and y1 == piece.y:
                # Promote piece
                if (piece.white and y2 == 7) or (not piece.white and y2 == 0):
                    pieces[i] = Pieces.King(piece.white, piece.x, piece.y)

                # Move piece to new position
                pieces[i].x = x2
                pieces[i].y = y2

                # Capture occurred
                if capture_x is not None:
                    self.capturePiece(capture_x, capture_y)

                    # Chain capture condition
                    if self.checkPossibleCaptures(pieces[i]):
                        self.capturing_piece = pieces[i]  # set currently capturing piece
                    else:
                        self.capturing_piece = None  # reset currently capturing piece
                        self.board.clearCaptured()   # clear all captured pieces

                break

    def capturePiece(self, piece_x, piece_y):
        """ Marks specified piece as captured, board is then responsible for removing that piece """

        pieces = self.board.getPieces(not self.current_player)

        for i, piece in enumerate(pieces):
            if piece_x == piece.x and piece_y == piece.y:
                pieces[i].captured = True

    def checkPossibleCaptures(self, piece):
        board_bitmap = self.board.generateBitmap()
        moves, captures = piece.generateValidMoves(board_bitmap, True)

        if len(captures) != 0:
            return True
        else:
            return False

    def initPlayers(self):
        while True:
            print("0. Human vs Bot (heuristic 1)")
            print("1. Human vs Bot (heuristic 2)")
            print("2. Bot vs Bot (heuristic 2 vs 1)")

            choice = input("Enter choice: ")
            depth = input("Enter search depth: ")

            try:
                choice = int(choice)
                depth = int(depth)

                if choice < 0 or choice > 2:
                    raise ValueError("Please enter choice in range 0-2")

                if depth < 1:
                    raise ValueError("Depth must be a positive integer")
            except ValueError as e:
                print(e)
                print("Invalid input!")
                continue

            if choice == 0:
                self.white_player = Players.Human(Pieces.Piece.WHITE)
                self.black_player = Players.MinMaxBot(Pieces.Piece.BLACK, depth, heuristics.h1)
            elif choice == 1:
                self.white_player = Players.Human(Pieces.Piece.WHITE)
                self.black_player = Players.MinMaxBot(Pieces.Piece.BLACK, depth, heuristics.h2)
            elif choice == 2:
                self.white_player = Players.MinMaxBot(Pieces.Piece.BLACK, depth, heuristics.h2)
                self.black_player = Players.MinMaxBot(Pieces.Piece.BLACK, depth, heuristics.h1)

            break
