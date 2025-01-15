"""
Information about current game state. Evaluates valid moves at current state. Keeps a move log.
"""

import numpy as np
from stockfish import Stockfish

class GameState():
    def __init__(self):
        # Board is an 8x8 2d np array, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', 'P'
        # "--" represents an empty space with no piece.
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.whiteToMove = True 
        self.moveLog = [] # list of all moves taken in the game

    def get_fen(self):
        fen = ""
        for row in self.board:
            empty_count = 0
            for square in row:
                if square == "--":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    # Translate the piece based on color
                    piece = square[1]  # Piece type
                    color = square[0]  # Piece color
                    # Use uppercase for white and lowercase for black
                    fen += piece.upper() if color == 'w' else piece.lower()
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"    
        # Remove the last slash
        fen = fen[:-1]
        # Add the turn to move
        fen += " " + ("w" if self.whiteToMove else "b")  
        # Add castling availability (not implemented, so we just add "-" for simplicity)
        fen += " -"   
        # Add en passant target square (not implemented, so we just add "-" for simplicity)
        fen += " -"      
        # Add halfmove clock (not implemented, so we just add "0")
        fen += " 0"   
        # Add fullmove number (not implemented, so we just add "1")
        fen += " 1"
        return fen   
    
    def get_evaluation(self):
        stockfish = Stockfish("/opt/homebrew/bin/stockfish", parameters={"Threads": 2, "Hash": 1024})
        stockfish.set_fen_position(self.get_fen())
        evaluation = stockfish.get_evaluation()

        # Convert evaluation to centipawns if not mate
        if evaluation["type"] == "cp":
            eval_value = round(evaluation["value"] * 0.01, 2)
            mate_moves = None
        elif evaluation["type"] == "mate":
            eval_value = 10 if evaluation["value"] >= 0 else -10      
            mate_moves = abs(evaluation["value"])   
        return eval_value, mate_moves
    
    # def make_pgn(self):
    #     pass