def h1(boardstate):
    """Heuristic based on number of pieces. Assumes bot playing black."""
    a = 0
    b = 0
    h = 0
    for i in range(len(boardstate.white_pieces)):
        if (boardstate.white_pieces[i].captured == False):
            a = a + 1
    for i in range(len(boardstate.black_pieces)):
        if (boardstate.black_pieces[i].captured == False):
            b = b + 1
    h = b - a
    return h