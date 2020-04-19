def h1(board_state):
    """Heuristic based on number of pieces. Assumes bot playing black."""

    a = 0
    b = 0
    h = 0
    for i in range(len(board_state.white_pieces)):
        if not board_state.white_pieces[i].captured:
            a = a + 1
    for i in range(len(board_state.black_pieces)):
        if not board_state.black_pieces[i].captured:
            b = b + 1
    h = b - a
    return h
