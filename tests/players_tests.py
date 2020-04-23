import unittest

import board
import pieces
import players
import heuristics


class PlayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.player = players.Player(pieces.Piece.WHITE)
        self.board = board.Board()

    def checkMove(self, move, x1, y1, x2, y2, cx, cy):
        self.assertEqual(move[0], x1)
        self.assertEqual(move[1], y1)
        self.assertEqual(move[2], x2)
        self.assertEqual(move[3], y2)
        self.assertEqual(move[4], cx)
        self.assertEqual(move[5], cy)

    def testStartingMoves(self):
        moves = self.player.getValidMoves(self.board, None, self.player.color)

        self.assertEqual(len(moves), 7)
        self.checkMove(moves[0], 0, 2, 1, 3, None, None)
        self.checkMove(moves[1], 2, 2, 1, 3, None, None)
        self.checkMove(moves[2], 2, 2, 3, 3, None, None)
        self.checkMove(moves[3], 4, 2, 3, 3, None, None)
        self.checkMove(moves[4], 4, 2, 5, 3, None, None)
        self.checkMove(moves[5], 6, 2, 5, 3, None, None)
        self.checkMove(moves[6], 6, 2, 7, 3, None, None)

    def testCaptures(self):
        # Position black piece for capture
        self.board.black_pieces[0].x = 3
        self.board.black_pieces[0].y = 3

        moves = self.player.getValidMoves(self.board, None, self.player.color)

        # Only captures should be allowed
        self.assertEqual(len(moves), 2)
        self.checkMove(moves[0], 2, 2, 4, 4, 3, 3)
        self.checkMove(moves[1], 4, 2, 2, 4, 3, 3)

    def testChainCapture(self):
        # Position black piece for capture
        self.board.black_pieces[0].x = 3
        self.board.black_pieces[0].y = 3

        # Find capturing piece
        capturing_piece = None
        for piece in self.board.white_pieces:
            if piece.x == 2 and piece.y == 2:
                capturing_piece = piece
                break

        self.assertNotEqual(capturing_piece, None)

        moves = self.player.getValidMoves(self.board, capturing_piece, self.player.color)

        # Only chain capture should be allowed
        self.assertEqual(len(moves), 1)
        self.checkMove(moves[0], 2, 2, 4, 4, 3, 3)


class MinimaxBotH1Test(unittest.TestCase):
    def setUp(self) -> None:
        self.player = players.MinMaxBot(pieces.Piece.BLACK, 6, heuristics.h1, False)
        self.board = board.Board()

    def checkMove(self, move, x1, y1, x2, y2, cx, cy):
        self.assertEqual(move[0], x1)
        self.assertEqual(move[1], y1)
        self.assertEqual(move[2], x2)
        self.assertEqual(move[3], y2)
        self.assertEqual(move[4], cx)
        self.assertEqual(move[5], cy)

    def testStartingMove(self):
        move = self.player.passControl(self.board, None)

        self.checkMove(move, 1, 5, 0, 4, None, None)

    def testCapture(self):
        # Setup capture
        self.board.white_pieces[0].x = 4
        self.board.white_pieces[0].y = 4

        move = self.player.passControl(self.board, None)

        self.checkMove(move, 3, 5, 5, 3, 4, 4)

    def testStartingMoveDepth7(self):
        self.player.depth = 7

        move = self.player.passControl(self.board, None)

        self.checkMove(move, 1, 5, 0, 4, None, None)

    def testCaptureDepth7(self):
        self.player.depth = 7

        # Setup capture
        self.board.white_pieces[0].x = 4
        self.board.white_pieces[0].y = 4

        move = self.player.passControl(self.board, None)

        self.checkMove(move, 3, 5, 5, 3, 4, 4)


class MinimaxBotH2Test(MinimaxBotH1Test):
    def setUp(self) -> None:
        self.player = players.MinMaxBot(pieces.Piece.BLACK, 6, heuristics.h2, False)
        self.board = board.Board()

    def testStartingMoveDepth7(self):
        self.player.depth = 7

        move = self.player.passControl(self.board, None)

        self.checkMove(move, 1, 5, 2, 4, None, None)


if __name__ == "__main__":
    unittest.main()
