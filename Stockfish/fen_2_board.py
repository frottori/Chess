fen = input("Enter a FEN string: ")

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