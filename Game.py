import Board
import Players

next_move = None
current_player = "white"
Table = Board.Board()
white_player = Players.Player()
black_player = Players.Player()
active_piece_row = None
active_piece_column = None

    #Main game loop

while 1 == 1:
    #break       #for debug purposes
    if current_player == "white":
        next_move = white_player.pass_control(Table)
    elif current_player == "black":
        next_move = black_player.pass_control(Table)

    if next_move == "surrender":
        if current_player == "white":
            print("Black player wins! (White surrendered)")
            break
        elif current_player == "black":
            print("White player wins! (Black surrendered)")
    else:
        #move validation
        #move validation
        #move validation

        #if()
        #assuming valid move
        origin_row = int(next_move[0])
        origin_column = int(next_move[2])
        destination_row = int(next_move[4])
        destination_column = int(next_move[6])

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
            if current_player == "white":
                current_player = "black"
            elif current_player == "black":
                current_player = "white"




#for debug purposes


temp = Table.condense()
print("\n", temp[7], "\n", temp[6], "\n", temp[5], "\n", temp[4], "\n", temp[3], "\n", temp[2], "\n", temp[1], "\n", temp[0], "\n")     #for debug purposes

print(Table.grid[7][1].owner)   #for debug purposes

Table.display()     #for debug purposes





next_move = white_player.pass_control(Table)
print(next_move)