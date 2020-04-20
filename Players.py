import Pieces
import copy


class Player:
    """
        Represents one of two players who can be a Human or Bot

        Player holds a color of his pieces that are held by Game instance
    """

    SURRENDER: str = "surrender"
    GAME_OVER: str = "game over"

    def __init__(self, color):
        """
        :param color: color of Player pieces
        """
        self.color = color

    def pass_control(self, board, capturing_piece):
        """
            Passes control in order for Player to make next move

            Move is formatted as 6 values:
            source_x, source_y, destination_x, destination_y, capture_x, capture_y

            Source coords represent piece on a board that is chosen for move
            Destination coords represent new position on the board of chosen piece
            Capture coords if specified represent position of captured piece and are
            set None if no capture occurred during that move

        :param board: current board state
        :param capturing_piece: piece performing chain capture
        :return: move formatted as 6 numbers tuple
        """
        pass

    def getValidMoves(self, board, capturing_piece, color):
        """
            Generates all valid moves for all pieces of specified color

        :param board: current board state
        :param capturing_piece: piece performing chain capture
        :param color: specifies for which pieces moves should be generated
        :return: list of valid moves
        """

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
    """ Human player """

    def pass_control(self, board, capturing_piece):
        """
            Human player gets prompts informing about current game state
            and is asked to choose a move from list of valid moves
        """

        valid_moves = self.getValidMoves(board, capturing_piece, self.color)

        if len(valid_moves) == 0:
            return Player.GAME_OVER

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
                if index == 0:  # 0 index represent surrender
                    return Player.SURRENDER
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
                print(", Capturing: ", '(', capture_x, ' ', capture_y, ')', sep='')
            else:
                print()  # New line


class MinMaxBot(Player):
    """Bot using MinMax algorithm with alpha-beta pruning"""

    def __init__(self, color, depth, func_h):
        super().__init__(color)
        self.heuristic = func_h
        self.possible_moves = []
        self.move_values = []
        self.depth = depth

        self.explored = {}
        self.evaluated = {}

    def checkPossibleCaptures_MinMax(self, boardstate, piece):
        board_bitmap = boardstate.generateBitmap()
        moves, captures = piece.generateValidMoves(board_bitmap, True)

        if len(captures) != 0:
            return piece
        else:
            return None


    def capturePiece_MinMax(self, boardstate, piece_x, piece_y, current_player):
        pieces = boardstate.getPieces(not current_player)

        for i, piece in enumerate(pieces):
            if piece_x == piece.x and piece_y == piece.y:
                pieces[i].captured = True

    def updateBoard_MinMax(self, boardstate, move, current_player):
        x1, y1, x2, y2, capture_x, capture_y = move
        pieces = boardstate.getPieces(current_player)

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
                    self.capturePiece_MinMax(boardstate, capture_x, capture_y, current_player)

                    # Chain capture condition
                    if self.checkPossibleCaptures_MinMax(boardstate, pieces[i]):
                        return pieces[i]
                    else:
                        boardstate.clearCaptured()
                        return None

                break


    def MinMax(self, boardstate, depth, alpha, beta, current_player, capturing_piece, origin):
        if (self.depth - depth < 5):
            if (boardstate, depth) in self.explored:
                return self.explored[(boardstate, depth)]
        if (depth == 0):
            if boardstate in self.evaluated:
                return self.evaluated[boardstate]
            else:
                self.evaluated[boardstate] = self.heuristic(boardstate)
                return self.evaluated[boardstate]
        moves = self.getValidMoves(boardstate, capturing_piece, current_player)
        if (len(moves) == 0 and capturing_piece == None):
            val = self.heuristic(boardstate)
            if (self.depth - depth < 5):
                self.explored[(boardstate, depth)] = val
            return val
        if (current_player != self.color):
            for i, move in enumerate(moves, 1):
                backup = copy.deepcopy(boardstate)
                capturing_piece = self.updateBoard_MinMax(boardstate, move, current_player)
                if (not(capturing_piece is None)):
                    beta = min(beta, self.MinMax(boardstate, depth, alpha, beta, current_player, capturing_piece, False))      #for purposes of multi-capture
                    boardstate = copy.deepcopy(backup)
                else:
                    beta = min(beta, self.MinMax(boardstate, depth-1, alpha, beta, (not current_player), None, False))
                    boardstate = copy.deepcopy(backup)
                    if (alpha >= beta):
                        break
            if (self.depth - depth < 5):
                self.explored[(boardstate, depth)] = beta
            return beta
        elif (current_player == self.color):
            for i, move in enumerate(moves, 1):
                backup = copy.deepcopy(boardstate)
                capturing_piece = self.updateBoard_MinMax(boardstate, move, current_player)
                if (not(capturing_piece is None)):
                    alpha = max(alpha, self.MinMax(boardstate, depth, alpha, beta, current_player, capturing_piece, False))      #for purposes of multi-capture
                    boardstate = copy.deepcopy(backup)
                else:
                    alpha = max(alpha, self.MinMax(boardstate, depth-1, alpha, beta, (not current_player), None, False))
                    boardstate = copy.deepcopy(backup)
                    if (alpha >= beta):
                        break
                if (origin):
                    self.move_values.append(alpha)
            if (self.depth - depth < 5):
                self.explored[(boardstate, depth)] = alpha
            return alpha






    def pass_control(self, board_state, capturing_piece):
        #    Debug Code
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #print("Before move")
        board_state.display()
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if (len(self.getValidMoves(board_state, None, self.color)) == 0):
            return "game over"
        self.possible_moves = []
        self.possible_moves = self.getValidMoves(board_state, capturing_piece, self.color)
        self.move_values = []
        self.explored.clear()
        optimal_value = self.MinMax(board_state, self.depth, -10000, 10000, self.color, None, True)            #depth control here for now
        g = 0
        while (g < len(self.possible_moves)):
            if (optimal_value == self.move_values[g]):
                return self.possible_moves[g]
            g = g + 1

        return "Error"
