import Board
import Pieces
import Players


def generateValidMoves(board):
    valid_moves, valid_captures = [], []
    board_bitmap = board.generateBitmap()

    for piece in board.white_pieces:
        moves, captures = piece.generateValidMoves(board_bitmap, len(valid_captures) != 0)

        if len(captures) != 0:
            valid_captures.extend(captures)
        else:
            valid_moves.extend(moves)

    for piece in board.black_pieces:
        moves, captures = piece.generateValidMoves(board_bitmap, len(valid_captures) != 0)

        if len(captures) != 0:
            valid_captures.extend(captures)
        else:
            valid_moves.extend(moves)

    if len(valid_captures) != 0:
        return valid_captures
    else:
        return valid_moves


next_move = None
current_player = Pieces.Piece.WHITE
Table = Board.Board()
white_player = Players.Player()
black_player = Players.Player()
active_piece_row = None
active_piece_column = None

#Main game loop

while True:
    #break       #for debug purposes
    if current_player == Pieces.Piece.WHITE:
        next_move = white_player.pass_control(Table)
    elif current_player == Pieces.Piece.BLACK:
        next_move = black_player.pass_control(Table)

    if next_move == "surrender":
        if current_player == Pieces.Piece.WHITE:
            print("Black player wins! (White surrendered)")
            break
        elif current_player == Pieces.Piece.BLACK:
            print("White player wins! (Black surrendered)")
    else:
        valid_moves = generateValidMoves(Table)

        if next_move in valid_moves:
            origin_row = int(next_move[1])          # y
            origin_column = int(next_move[0])       # x
            destination_row = int(next_move[3])     # y
            destination_column = int(next_move[2])  # x

            #check for capture
            if abs(destination_row - origin_row) == 1:
                #no capture
                Table.grid[origin_row][origin_column].row = destination_row
                Table.grid[origin_row][origin_column].column = destination_column
                Table.grid[destination_row][destination_column] = Table.grid[origin_row][origin_column]
                Table.grid[origin_row][origin_column] = None

            else:
                #with capture
                capture_row = (origin_row + int((destination_row - origin_row)/2))
                capture_column = (origin_column + int((destination_column - origin_column)/2))

                Table.grid[origin_row][origin_column].row = destination_row
                Table.grid[origin_row][origin_column].column = destination_column
                Table.grid[destination_row][destination_column] = Table.grid[origin_row][origin_column]
                Table.grid[origin_row][origin_column] = None

                Table.grid[capture_row][capture_column].alive = 0       #stays on board in case of chain capture

                Table.display()     #for debug purposes

                #if()       ---  check for chain capture
                #   active_piece_row = destination_row
                #   active_piece_column = destination_column
                #   continue - validation function will take active piece into account

                #else       --- no chain capture
                Table.clear_captured()
                active_piece_row = None
                active_piece_column = None
                if current_player == Pieces.Piece.WHITE:
                    current_player = Pieces.Piece.BLACK
                elif current_player == Pieces.Piece.BLACK:
                    current_player = Pieces.Piece.WHITE




#for debug purposes


temp = Table.generateBitmap()
print("\n", temp[7], "\n", temp[6], "\n", temp[5], "\n", temp[4], "\n", temp[3], "\n", temp[2], "\n", temp[1], "\n", temp[0], "\n")     #for debug purposes

print(Table.grid[7][1].owner)   #for debug purposes

Table.display()     #for debug purposes





next_move = white_player.pass_control(Table)
print(next_move)