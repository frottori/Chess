from stockfish import Stockfish

# Initialize Stockfish engine
stockfish = Stockfish(path="/opt/homebrew/bin/stockfish", 
                      depth=18, 
                      parameters={"Threads": 2, "Minimum Thinking Time": 30})
stockfish.set_skill_level(20)  # Max strength

# Example PGN (game in Portable Game Notation)
moves = [
    "e2e4", "e7e5",
    "g1f3", "b8c6",
    "f1b5", "a7a6",
    "b5a4", "g8f6"
]

# Load the position and evaluate each move
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
stockfish.set_fen_position(starting_fen)
errors = []
for move in moves:
    eval_before = stockfish.get_evaluation()
    stockfish.make_moves_from_current_position([move])
    eval_after = stockfish.get_evaluation()
    
    if eval_before["type"] == "cp" and eval_after["type"] == "cp":
        # Compute centipawn loss for the move
        cp_loss = abs(eval_after["value"] - eval_before["value"])
        errors.append(cp_loss)

# Calculate average centipawn loss
acpl = sum(errors) / len(errors)
print(f"Average Centipawn Loss (ACPL): {acpl}")

# Interpret the ACPL (rough estimate of Elo strength)
if acpl < 20:
    print("Likely a Grandmaster-level player!")
elif acpl < 50:
    print("Strong club player (1800-2200).")
elif acpl < 100:
    print("Intermediate player (1400-1800).")
else:
    print("Beginner or casual player.")