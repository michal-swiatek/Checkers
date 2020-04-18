import Pieces


class Player:
    def __init__(self, color):
        self.color = color

    def pass_control(self, board, capturing_piece):
        pass

    def getValidMoves(self, board, capturing_piece, color):
        pieces = board.getPieces(color)
        if capturing_piece is not None:
            pieces = [capturing_piece]

        valid_moves, valid_captures = [], []
        board_bitmap = board.generateBitmap()

        for piece in pieces:
            moves, captures = piece.generateValidMoves(board_bitmap, len(valid_captures) != 0)

            if len(captures) != 0:
                valid_captures.extend(captures)
            else:
                valid_moves.extend(moves)

        if len(valid_captures) != 0:
            return valid_captures
        else:
            return valid_moves


class Human(Player):
    """Human player"""

    def pass_control(self, board, capturing_piece):
        valid_moves = self.getValidMoves(board, capturing_piece, self.color)

        if len(valid_moves) == 0:
            return "game over"

        while True:
            board.display()

            if self.color == Pieces.Piece.WHITE:
                print("\n\tWHITE turn")
            else:
                print("\n\tBLACK turn")

            self.displayValidMoves(valid_moves)

            user_input = input("Enter move: ")
            try:
                index = int(user_input)
                if index == 0:
                    return "surrender"
                else:
                    return valid_moves[index - 1]
            except (ValueError, IndexError):
                continue

    def displayValidMoves(self, valid_moves):
        print("0) Surrender")
        for i, move in enumerate(valid_moves, 1):
            x1, y1, x2, y2, capture_x, capture_y = move

            # Enumeration
            print(i, ')', sep='', end=' ')

            # Coords
            print('(', x1, ' ', y1, ')', sep='', end=" -> ")
            print('(', x2, ' ', y2, ')', sep='', end='')

            # Capture
            if capture_x is not None:
                print(", Capturing:", capture_x, capture_y)
            else:
                print()  # New line


class MinMaxBot(Player):
    """Bot using MinMax algorithm with alpha-beta pruning"""

    def pass_control(self, board_state, capturing_piece):
        pass        #TO DO LATER
