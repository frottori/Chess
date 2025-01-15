import chess
import chess.pgn
from stockfish import Stockfish

# Path to your Stockfish binary
stockfish = Stockfish("/opt/homebrew/bin/stockfish", parameters={"Threads": 2, "Hash": 128})

# Path to your PGN file
pgn_path = "Stockfish/game1.pgn"

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
    evaluations.append((move, evaluation))  # Save the move and evaluation

# Print evaluations
for move, eval_ in evaluations:
    if eval_["type"] == "cp":
        eval_score = eval_["value"]
        print(f"Move: {move}, Evaluation: {eval_score} centipawns")
    elif eval_["type"] == "mate":
        print(f"Move: {move}, Evaluation: Mate in {eval_['value']} moves")

# Centipawn loss
# This value can be used as an indicator of the quality of play. 
# The fewer centipawns one loses per move, the stronger the play. 
# The computer analysis on Lichess is powered by Stockfish. a centipawn cP 
# is 1/100 of the worth of a pawn.