"""
Information about current game state. Evaluates valid moves at current state. Keeps a move log.
"""

import numpy as np
from stockfish import Stockfish
from stockfish import StockfishException
import chess

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

    def make_move(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"         # Empty the start square
            self.board[move.endRow][move.endCol] = move.pieceMoved  # Move the piece to the end square
            self.moveLog.append(move)                               # Log the move
            self.whiteToMove = not self.whiteToMove                 # Swap the turn

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
    
    # Function to map the numpy array to the chess.Board() object (FOW NOW FOR EVAL TO WORK PROPERLY, I WILL FIX GET_FEN() LATER)
    def to_chess_board(self):
        # Create the empty board object
        board = chess.Board(fen="8/8/8/8/8/8/8/8 w - - 0 1")
        
        # Map the numpy array to the chessboard's squares
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "--":
                    # Determine the piece and place it on the board
                    chess_piece = piece[1].upper() if piece[0] == "w" else piece[1].lower()
                    square = chess.square(col, 7 - row)  # Flip rows to match board orientation
                    board.set_piece_at(square, chess.Piece.from_symbol(chess_piece)) 
        return board
    
    def get_evaluation(self):
        try:
            stockfish = Stockfish("/opt/homebrew/bin/stockfish", parameters={"Threads": 2, "Hash": 1024})
            # stockfish.set_depth(17)
            # fen = self.get_fen()
            fen = self.to_chess_board().fen()
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()

            # Convert evaluation to centipawns if not mate
            if evaluation["type"] == "cp":
                eval_value = round(evaluation["value"] * 0.01, 2)
                mate_moves = None
            elif evaluation["type"] == "mate":
                eval_value = 10 if evaluation["value"] >= 0 else -10      
                mate_moves = abs(evaluation["value"])   
        except StockfishException:
            eval_value = 0
            mate_moves = None
            print("Stockfish failed to evaluate the position, evaluation set to 0")
        return eval_value, mate_moves

class Move():
    # Maps keys to values
    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} # Reverse the dictionary
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        
        self.startRow, self.startCol = startSq
        self.endRow, self.endCol = endSq
        self.pieceMoved = board[self.startRow][self.startCol] # The piece you want to move
        self.pieceCaptured = board[self.endRow][self.endCol]  # The piece you want to capture

    def get_chess_notation(self):
        # make all chess noations for captures etc.
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
        