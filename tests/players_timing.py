import time
import copy

import Board
import Pieces
import Players
import heuristics


class Timer:
    def __init__(self, repeat=5, best_of=3):
        self.repeat = int(repeat)
        self.best_of = int(best_of)

        self.results = []

    def reset(self):
        self.results = []

    def testFunction(self, function, *args):
        self.reset()
        test_time0 = time.time()

        for case in range(self.repeat):
            args_copy = copy.deepcopy(args)

            t0 = time.time()
            function(*args_copy)
            t1 = time.time()

            self.results.append(t1 - t0)

        test_time1 = time.time()

        print("Test time:", test_time1 - test_time0, "s")

    def showResults(self):
        self.results.sort()
        best_of_results = self.results[:self.best_of]

        results_summed = sum(self.results)
        best_of_summed = sum(best_of_results)

        print("Average over", self.repeat, "results:", results_summed / self.repeat, "s")
        print("Average over", self.best_of, "best results:", best_of_summed / self.best_of, "s")


def testSingleMoveTime(timer, depth, heuristic, board_state=Board.Board(), capturing_piece=None):
    player = Players.MinMaxBot(Pieces.Piece.BLACK, depth, heuristic, False)

    timer.testFunction(player.pass_control, board_state, capturing_piece)

    timer.showResults()


if __name__ == "__main__":
    timer = Timer(10, 5)

    testSingleMoveTime(timer, 6, heuristics.h1)
