from stockfish import Stockfish

stockfish = Stockfish(path="/opt/homebrew/bin/stockfish", 
                      depth=18, 
                      parameters={"Threads": 2, "Minimum Thinking Time": 30})

# Example: Set a position
stockfish.set_position(["e2e4", "e7e5", "g1f3", "b8c6"])

# Get the FEN string from Stockfish
fen = stockfish.get_fen_position()

# Function to convert FEN to a 2D list
def fen_to_board(fen):
    board = []
    fen_board = fen.split(" ")[0]  # Extract board part from FEN
    for row in fen_board.split("/"):
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(["."] * int(char))  # Empty squares
            else:
                board_row.append(char)  # Piece
        board.append(board_row)
    return board

# Convert FEN to a 2D list
board_state = fen_to_board(fen)

# Print the board
for row in board_state:
    print(row)