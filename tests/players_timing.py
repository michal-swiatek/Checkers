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

    def showResults(self, print_results=True, file=None, test_info=None):
        self.results.sort()
        best_of_results = self.results[:self.best_of]

        results_summed = sum(self.results)
        best_of_summed = sum(best_of_results)

        if print_results:
            print("Average over", self.repeat, "results:", results_summed / self.repeat, "s")
            print("Average over", self.best_of, "best results:", best_of_summed / self.best_of, "s")
            print("Best time:", self.results[0])
            print("Worst time:", self.results[-1])

        if file is not None:
            if test_info is not None:
                file.write(test_info)

            # All results
            file.write("Results (in seconds): ")
            for result in self.results:
                file.write("{:.3f} ".format(result))

            # Result info
            file.write("\nAverage over {} results: {:.3f}s\n".format(self.repeat, results_summed / self.repeat))
            file.write("Average over {} best results: {:.3f}s\n".format(self.best_of, best_of_summed / self.best_of))
            file.write("Best time: {:.3f}s\n".format(self.results[0]))
            file.write("Worst time: {:.3f}s\n\n".format(self.results[-1]))


def testSingleMoveTime(timer, depth, heuristic, board_state=None, capturing_piece=None, file=None):
    if board_state is None:
        board_state = Board.Board()

    player = Players.MinMaxBot(Pieces.Piece.BLACK, depth, heuristic, False)

    timer.testFunction(player.pass_control, copy.deepcopy(board_state), copy.deepcopy(capturing_piece))

    if heuristic == heuristics.h1:
        timer.showResults(print_results=True, file=file, test_info="Depth = {}\nHeuristic 1\n".format(depth))
    elif heuristic == heuristics.h2:
        timer.showResults(print_results=True, file=file, test_info="Depth = {}\nHeuristic 2\n".format(depth))


if __name__ == "__main__":
    file = open("timing_results.txt", "w")

    print("STARTING MOVES")
    file.write("STARTING MOVES\n\n")
    counter = 1  # indicates what tests have already finished

    # Test 1
    timer = Timer(100, 50)
    testSingleMoveTime(timer, 1, heuristics.h1, file=file)
    testSingleMoveTime(timer, 1, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 2
    timer = Timer(100, 50)
    testSingleMoveTime(timer, 2, heuristics.h1, file=file)
    testSingleMoveTime(timer, 2, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 3
    timer = Timer(100, 50)
    testSingleMoveTime(timer, 3, heuristics.h1, file=file)
    testSingleMoveTime(timer, 3, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 4
    timer = Timer(50, 20)
    testSingleMoveTime(timer, 4, heuristics.h1, file=file)
    testSingleMoveTime(timer, 4, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 5
    timer = Timer(50, 20)
    testSingleMoveTime(timer, 5, heuristics.h1, file=file)
    testSingleMoveTime(timer, 5, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 6
    timer = Timer(10, 5)
    testSingleMoveTime(timer, 6, heuristics.h1, file=file)
    testSingleMoveTime(timer, 6, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 7
    timer = Timer(10, 5)
    testSingleMoveTime(timer, 7, heuristics.h1, file=file)
    testSingleMoveTime(timer, 7, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    # Test 8
    timer = Timer(10, 5)
    testSingleMoveTime(timer, 8, heuristics.h1, file=file)
    testSingleMoveTime(timer, 8, heuristics.h2, file=file)
    print("Test", counter, "finished!")
    counter += 1

    file.close()
