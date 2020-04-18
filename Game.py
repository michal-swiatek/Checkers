import Board
import Pieces
import Players
import copy


class Game:
    """ Game instance """

    def __init__(self):
        self.running = True

        self.board = Board.Board()

        self.white_player = Players.Human(Pieces.Piece.WHITE)
        self.black_player = Players.MinMaxBot(Pieces.Piece.BLACK)

        self.current_player = Pieces.Piece.WHITE

        self.capturing_piece = None

    def mainLoop(self):
        """ Game loop """

        while self.running:
            if self.current_player == Pieces.Piece.WHITE:
                next_move = self.white_player.pass_control(self.board, self.capturing_piece)
            else:
                next_move = self.black_player.pass_control(copy.deepcopy(self.board), self.capturing_piece)
                print("Optimal move value:  ", next_move)
                self.current_player = not self.current_player
                input("Continue?")
                continue

            if next_move == "surrender":
                if self.current_player == Pieces.Piece.WHITE:
                    print("Black player wins! (White surrendered)")
                else:
                    print("White player wins! (Black surrendered)")

                self.running = False
            elif next_move == "game over":
                if self.current_player == Pieces.Piece.WHITE:
                    print("Black player wins!")
                else:
                    print("White player wins!")

                self.running = False
            else:
                self.updateBoard(next_move)

                if self.capturing_piece is None:
                    self.current_player = not self.current_player

    def updateBoard(self, move):
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
                        self.capturing_piece = pieces[i]
                    else:
                        self.capturing_piece = None
                        self.board.clear_captured()

                break

    def capturePiece(self, piece_x, piece_y):
        pieces = self.board.getPieces(not self.current_player)

        for i, piece in enumerate(pieces):
            if piece_x == piece.x and piece_y == piece.y:
                pieces[i].captured = True

    def checkPossibleCaptures(self, piece):
        board_bitmap = self.board.generateBitmap()
        moves, captures = piece.generateValidMoves(board_bitmap, True)

        if len(captures) != 0:
            return piece
        else:
            return None
