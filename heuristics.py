from Pieces import Piece


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


def h2(board_state):
    """
        Heuristics counting all possible moves of a player as well as
        taking a piece position into account

        Counting all possible moves of a player makes AI to go for more
        open states as well as trying to minimize opponent movement.
        This leads to leaving enemy player only a few moves and potentially
        leading to win due to no possible moves. Also this strategy makes AI
        go for captures as in future this leads to fewer opponent moves
        (less pieces mean less possible moves). Counting moves introduces a clear
        distinction in power of Man and a King as King can generate much more
        moves thus he is much more valuable.
        Additionally piece position is taken into account as Man near promotion
        is more dangerous. For Kings this position effect cancel out as King in
        the middle of board can make a lot of moves.

    :param board_state: current board state
    :return: score as an integer
    """

    STATIC_POINTS = 2

    white_pieces = board_state.getPieces(Piece.WHITE)
    black_pieces = board_state.getPieces(Piece.BLACK)

    board_bitmap = board_state.generateBitmap()

    score = 0

    valid_moves, valid_captures = [], []
    for piece in white_pieces:
        moves, captures = piece.generateValidMoves(board_bitmap, len(valid_captures) != 0)

        if len(captures) > 0:
            valid_captures.extend(captures)
        else:
            valid_moves.extend(moves)

        score -= piece.y + STATIC_POINTS

    if len(valid_captures) > 0:
        valid_moves = valid_captures

    score -= len(valid_moves)

    valid_moves, valid_captures = [], []
    for piece in black_pieces:
        moves, captures = piece.generateValidMoves(board_bitmap, len(valid_captures) != 0)

        if len(captures) > 0:
            valid_captures.extend(captures)
        else:
            valid_moves.extend(moves)

        score += (7 - piece.y) + STATIC_POINTS  # Black pieces move in opposite direction

    if len(valid_captures) > 0:
        valid_moves = valid_captures

    score += len(valid_moves)

    return score
