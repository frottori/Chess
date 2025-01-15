from stockfish import Stockfish

stockfish = Stockfish(path="/opt/homebrew/bin/stockfish", 
                      depth=18, 
                      parameters={"Threads": 2, "Minimum Thinking Time": 30})

# Example: Set a position
fen = input("Enter a FEN string: ")
stockfish.set_fen_position(fen)

# Get the FEN string from Stockfish
fen = stockfish.get_fen_position()

# Function to convert FEN to a 2D list with color and piece type
def fen_to_board(fen):
    board = []
    fen_board = fen.split(" ")[0]  # Extract board part from FEN
    piece_mapping = {
        "r": "bR", "n": "bN", "b": "bB", "q": "bQ", "k": "bK", "p": "bp",  # black pieces
        "R": "wR", "N": "wN", "B": "wB", "Q": "wQ", "K": "wK", "P": "wp"   # white pieces
    }
    
    for row in fen_board.split("/"):
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(["--"] * int(char))  # Empty squares
            else:
                board_row.append(piece_mapping.get(char, "--"))  # Map piece to the new format
        board.append(board_row)
    return board

# Convert FEN to a 2D list
board_state = fen_to_board(fen)

# Print the board in the requested format
print("[")
for row in board_state:
    print(f'    {row},')
print("]")