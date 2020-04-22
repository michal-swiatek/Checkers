import unittest

import Pieces


class PieceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.piece = Pieces.Piece(Pieces.Piece.WHITE, 0, 0)

    def testConstructor(self):
        self.assertEqual(self.piece.x, 0)
        self.assertEqual(self.piece.y, 0)
        self.assertEqual(self.piece.white, Pieces.Piece.WHITE)
        self.assertEqual(self.piece.captured, False)

    def testUninitializedMethods(self):
        bitmap = [True, None, False]  # Arbitrary bitmap

        self.assertEqual(self.piece.generateValidMoves(bitmap), None)
        self.assertEqual(self.piece.displayCharacter(), None)


class ManTest(unittest.TestCase):
    def setUp(self) -> None:
        self.piece = Pieces.Man(Pieces.Piece.WHITE, 1, 1)
        self.bitmap = [[None for i in range(8)] for j in range(8)]

    def checkMove(self, move, x1, y1, x2, y2, cx, xy):
        x1, y1, x2, y2, cx, cy = move
        self.assertEqual(move[0], x1)
        self.assertEqual(move[1], y1)
        self.assertEqual(move[2], x2)
        self.assertEqual(move[3], y2)
        self.assertEqual(move[4], cx)
        self.assertEqual(move[5], cy)

    def testMoves(self):
        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 0)
        self.assertEqual(len(moves), 2)

        self.checkMove(moves[0], 1, 1, 0, 2, None, None)
        self.checkMove(moves[1], 1, 1, 2, 2, None, None)

    def testCaptures(self):
        self.bitmap[0][2] = Pieces.Piece.BLACK
        self.bitmap[2][2] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 1)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 1, 3, 3, 2, 2)

        self.bitmap[3][3] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 0)
        self.assertEqual(len(moves), 0)

        self.bitmap[3][3] = Pieces.Piece.WHITE

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 0)
        self.assertEqual(len(moves), 0)

    def testCapturesWithMoves(self):
        self.bitmap[2][2] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 1)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 1, 3, 3, 2, 2)

    def testCaptureBackwards(self):
        self.piece.y = 3
        self.bitmap[2][2] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 1)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 3, 3, 1, 2, 2)

    def testDisplayCharacter(self):
        self.assertEqual(self.piece.displayCharacter(), 'w')


class KingTest(ManTest):
    def setUp(self) -> None:
        self.piece = Pieces.King(Pieces.Piece.WHITE, 1, 1)
        self.bitmap = [[None for i in range(8)] for j in range(8)]

    def testLongCapture(self):
        self.bitmap[4][4] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 3)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 1, 5, 5, 2, 2)
        self.checkMove(captures[0], 1, 1, 6, 6, 2, 2)
        self.checkMove(captures[0], 1, 1, 7, 7, 2, 2)

    def testMoves(self):
        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 0)
        self.assertEqual(len(moves), 9)

        self.checkMove(moves[0], 1, 1, 0, 2, None, None)
        self.checkMove(moves[1], 1, 1, 2, 2, None, None)

    def testCaptures(self):
        self.bitmap[0][2] = Pieces.Piece.BLACK
        self.bitmap[2][2] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 5)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 1, 3, 3, 2, 2)

        self.bitmap[3][3] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 0)
        self.assertEqual(len(moves), 2)

        self.bitmap[3][3] = Pieces.Piece.WHITE

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 0)
        self.assertEqual(len(moves), 2)

    def testCapturesWithMoves(self):
        self.bitmap[2][2] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 5)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 1, 3, 3, 2, 2)

    def testCaptureBackwards(self):
        self.piece.y = 3
        self.bitmap[2][2] = Pieces.Piece.BLACK

        moves, captures = self.piece.generateValidMoves(self.bitmap)

        self.assertEqual(len(captures), 2)
        self.assertEqual(len(moves), 0)

        self.checkMove(captures[0], 1, 3, 3, 1, 2, 2)
        self.checkMove(captures[0], 1, 3, 4, 0, 2, 2)

    def testDisplayCharacter(self):
        self.assertEqual(self.piece.displayCharacter(), 'W')


if __name__ == "__main__":
    unittest.main()
