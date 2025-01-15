import chess
import chess.pgn
from stockfish import Stockfish

# Path to your Stockfish binary
stockfish = Stockfish("/opt/homebrew/bin/stockfish", 
                      parameters={"Threads": 2, 
                                  "Hash": 1025,
                                  })

# Path to your PGN file
username = input("Enter the username for latest PGN game: ")
pgn_path = "PGNs/" + username + "_latest_game.pgn"
if username == "":
    pgn_path = "PGNs/magnuscarlsen_latest_game.pgn"

# Open the PGN file
with open(pgn_path) as pgn_file:
    game = chess.pgn.read_game(pgn_file)

# Initialize variables
board = game.board()
evaluations = []

# Iterate through all moves in the game
for move in game.mainline_moves():
    board.push(move)  # Make the move on the board
    stockfish.set_fen_position(board.fen())  # Set the position in Stockfish
    evaluation = stockfish.get_evaluation()  # Get the evaluation from Stockfish
    evaluations.append((move, evaluation))   # Save the move and evaluation

# Print evaluations
print("\nEvaluations: (Positive is advantage white, negative is advantage black)")
i = 1
num_move = 1
for move, eval in evaluations:

    player = "WHITE" if i % 2 == 1 else "BLACK"
    if i % 2 == 1 and i != 1:
        num_move += 1
    
    i += 1

    if eval["type"] == "cp":
        eval_value = round(eval["value"] * 0.01, 2)  # e.g -1.50 like chess.com
        print(f"{num_move}. {player} Move: {move}, Evaluation: {eval_value} centipawns")
    elif eval["type"] == "mate":
        print(f"{num_move}. {player} Move: {move}, Evaluation: Mate in {eval["value"]} moves")

# Centipawn loss
# This value can be used as an indicator of the quality of play. 
# The fewer centipawns one loses per move, the stronger the play. 
# The computer analysis on Lichess is powered by Stockfish. a centipawn cP 
# is 1/100 of the worth of a pawn.