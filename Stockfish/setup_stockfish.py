from stockfish import Stockfish

#! Stockfish parameters
# {
#     "Debug Log File": "",
#     "Contempt": 0,
#     "Min Split Depth": 0,
#     "Threads": 1, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
#     "Ponder": "false",
#     "Hash": 16, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
#     "MultiPV": 1,
#     "Skill Level": 20,
#     "Move Overhead": 10,
#     "Minimum Thinking Time": 20,
#     "Slow Mover": 100,
#     "UCI_Chess960": "false",
#     "UCI_LimitStrength": "false",
#     "UCI_Elo": 1350
# }

stockfish = Stockfish(path="/opt/homebrew/bin/stockfish", 
                      depth=18, 
                      parameters={"Threads": 2, "Minimum Thinking Time": 30})

# Update stockfish parameters
# stockfish.update_engine_parameters({"Hash": 2048, "UCI_Chess960": "true"}) # Gets stockfish to use a 2GB hash table, and also to play Chess960.

print(stockfish.get_parameters())
stockfish.reset_engine_parameters()

# Set the position of the board
stockfish.set_position(["e2e4", "e7e5", "g1f3", "b8c6"])

print(stockfish.get_board_visual())

# Make a move
stockfish.make_moves_from_current_position(["g4d7", "a8b8", "f1d1"])

# Skill level
stockfish.set_skill_level(15)
# Elo rating
stockfish.set_elo_rating(1350)
# Depth
stockfish.set_depth(15)

# Get the FEN position in Forsyth–Edwards notation (FEN)
stockfish.get_fen_position()

stockfish.get_evaluation()

# Get the board state
print(stockfish.get_board_visual())

print(stockfish.is_move_correct('a2a3'))

print(stockfish.get_top_moves(3))
print(stockfish.get_best_move())

print(stockfish.get_stockfish_major_version())

stockfish.get_what_is_on_square("e1") # returns Stockfish.Piece.WHITE_KING
stockfish.get_what_is_on_square("d8") # returns Stockfish.Piece.BLACK_QUEEN
stockfish.get_what_is_on_square("h2") # returns Stockfish.Piece.WHITE_PAWN
stockfish.get_what_is_on_square("b5") # returns None

stockfish.will_move_be_a_capture("c3d5")  # returns Stockfish.Capture.DIRECT_CAPTURE  
stockfish.will_move_be_a_capture("e5f6")  # returns Stockfish.Capture.DIRECT_CAPTURE  
stockfish.will_move_be_a_capture("e5d6")  # returns Stockfish.Capture.EN_PASSANT  
stockfish.will_move_be_a_capture("f1e2")  # returns Stockfish.Capture.NO_CAPTURE 