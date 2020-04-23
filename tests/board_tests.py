"""
    Authors: Michal Swiatek, Jan Wasilewski
    Github: https://github.com/michal-swiatek/Checkers
"""


import unittest

import board


class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = board.Board()

    def testConstructor(self):
        white_pieces = self.board.getPieces(board.Piece.WHITE)
        black_pieces = self.board.getPieces(board.Piece.BLACK)

        # At the beginning of a game each player has 12 pieces
        self.assertEqual(len(white_pieces), 12)
        self.assertEqual(len(black_pieces), 12)

        # Check that at the bottom left corner white piece is placed
        grid = self.board.generateBoardState()
        self.assertEqual(grid[0][0].x, 0)
        self.assertEqual(grid[0][0].y, 0)
        self.assertEqual(grid[0][0].white, board.Piece.WHITE)

    def testGenerateBitmap(self):
        bitmap = self.board.generateBitmap()

        bit_sum = 0
        for x in range(8):
            for y in range(8):
                if bitmap[x][y] is True:
                    bit_sum += 1
                elif bitmap[x][y] is False:
                    bit_sum -= 1

        self.assertEqual(bit_sum, 0)  # board bitmap should be symmetric

        # Setting one piece as captured should change its value in bitmap to not color
        self.board.white_pieces[0].captured = True
        bitmap = self.board.generateBitmap()

        bit_sum = 0
        for x in range(8):
            for y in range(8):
                if bitmap[x][y] is True:
                    bit_sum += 1
                elif bitmap[x][y] is False:
                    bit_sum -= 1

        self.assertEqual(bit_sum, -2)  # board bitmap after one capture should not be symmetric

    def testGenerateBoardState(self):
        grid = self.board.generateBoardState()

        # Top right corner should contain black piece
        self.assertEqual(grid[7][7].x, 7)
        self.assertEqual(grid[7][7].y, 7)
        self.assertEqual(grid[7][7].white, board.Piece.BLACK)

        # Bottom left corner should contain white piece
        self.assertEqual(grid[0][0].x, 0)
        self.assertEqual(grid[0][0].y, 0)
        self.assertEqual(grid[0][0].white, board.Piece.WHITE)

        # Empty spot
        self.assertEqual(grid[1][0], None)

    def testClearCaptured(self):
        grid = self.board.generateBoardState()
        self.assertNotEqual(grid[0][0], None)

        self.board.white_pieces[0].captured = True
        self.board.clearCaptured()

        grid = self.board.generateBoardState()
        self.assertEqual(grid[0][0], None)


if __name__ == "__main__":
    unittest.main()
