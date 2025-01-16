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
        # Dictionary to map the piece to its move function
        self.moveFunctions = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves, 
                              "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.whiteToMove = True 
        self.moveLog = [] # list of all moves taken in the game  

    """
    Functions to move pieces
    """
    # Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    def make_move(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"         # Empty the start square
            self.board[move.endRow][move.endCol] = move.pieceMoved  # Move the piece to the end square
            self.moveLog.append(move)                               # Log the move
            self.whiteToMove = not self.whiteToMove                 # Swap the turn

    # Undo the last move made
    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    """
    Functions to get all possible moves
    """
    # All moves considering checks
    def get_valid_moves(self):
        return self.get_all_possible_moves() #! We will not consider checks for now
    
    # All moves without considering checks
    def get_all_possible_moves(self):
        moves = [] 
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] # Get the color of the piece
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): # If it's the correct turn
                    piece = self.board[row][col][1] # Get the piece type
                    self.moveFunctions[piece](row, col, moves)
        return moves
    
    """
    Functions to get all possible moves for each piece
    """
    def get_pawn_moves(self, row, col, moves):
        if self.whiteToMove: # White pawn moves
            next_row = row - 1
            next_2_row = row - 2
            start_row = 6
            other_player = 'b'
        else: # Black pawn moves
            next_row = row + 1
            next_2_row = row + 2
            start_row = 1
            other_player = 'w'

        if self.board[next_row][col] == "--": # 1 square pawn advance
                moves.append(Move((row, col), (next_row, col), self.board))
                if row == start_row and self.board[next_2_row][col] == "--": # 2 square pawn advance if at starting position
                    moves.append(Move((row, col), (next_2_row, col), self.board))
        if col - 1 >= 0: # Capture to the left/right
            if self.board[next_row][col - 1][0] == other_player:
                moves.append(Move((row, col), (next_row, col - 1), self.board))
        if col + 1 <= 7: # Capture to the right/left
            if self.board[next_row][col + 1][0] == other_player:
                moves.append(Move((row, col), (next_row, col + 1), self.board))     
        
    def get_rook_moves(self, row, col, moves):
        if row+1 <= 7:
            self.rook_helper(row+1,len(self.board[row]),  1, "row", row, col, moves)
        if row-1 >= 0:
            self.rook_helper(row-1, -1, -1, "row", row, col, moves)
        if col+1 <= 7:
            self.rook_helper(col+1, len(self.board[row]), 1, "col", row, col, moves)
        if col-1 >= 0:
            self.rook_helper(col-1, -1, -1, "col", row, col, moves)
        return moves

    def rook_helper(self, start, length, step, flag, row, col, moves):
        for k in range(start, length, step):
            if flag == "row":
                if self.board[k][col] == "--":
                    moves.append(Move((row, col), (k, col), self.board))
                else:
                    if self.board[k][col][0] != self.board[row][col][0]:  # Opposite color piece
                        moves.append(Move((row, col), (k, col), self.board))
                    break
            else:
                if self.board[row][k] == "--":
                    moves.append(Move((row, col), (row, k), self.board))
                else:
                    if self.board[row][k][0] != self.board[row][col][0]:  # Opposite color piece
                        moves.append(Move((row, col), (row, k), self.board))
                    break
                    

    def get_knight_moves(self, row, col, moves):
        knight_moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row + 2, col - 1), (row + 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2)
        ]
        
        for move in knight_moves:
            r, c = move
            if 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                if self.board[r][c] == "--" or self.board[r][c][0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (r, c), self.board))

    def get_bishop_moves(self, row, col, moves):
        if row+1 <= 7 and col+1 <= 7:
            self.bishop_helper(row+1, col+1, 1, 1, row, col, moves)
        if row+1 <= 7 and col-1 >= 0:
            self.bishop_helper(row+1, col-1, 1, -1, row, col, moves)
        if row-1 >= 0 and col+1 <= 7:
            self.bishop_helper(row-1, col+1, -1, 1, row, col, moves)
        if row-1 >= 0 and col-1 >= 0:
            self.bishop_helper(row-1, col-1, -1, -1, row, col, moves)
        return moves
    
    def bishop_helper(self, start_row, start_col, row_step, col_step, row, col, moves):
        r, c = start_row, start_col
        while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
            if self.board[r][c] == "--":
                moves.append(Move((row, col), (r, c), self.board))
            else:
                if self.board[r][c][0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (r, c), self.board))
                break
            r += row_step
            c += col_step

    def get_queen_moves(self, row, col, moves):
        moves.append(self.get_rook_moves(row, col, moves))
        moves.append(self.get_bishop_moves(row, col, moves))

    def get_king_moves(self, row, col, moves):
        if row+1 <= 7:
            self.king_helper(row+1, col, row, col, moves)
        if row-1 >= 0:
            self.king_helper(row-1, col, row, col, moves)
        if col+1 <= 7:
            self.king_helper(row, col+1, row, col, moves)
        if col-1 >= 0:
            self.king_helper(row, col-1, row, col, moves)
        if row+1 <= 7 and col+1 <= 7:
            self.king_helper(row+1, col+1, row, col, moves)
        if row+1 <= 7 and col-1 >= 0:
            self.king_helper(row+1, col-1, row, col, moves)
        if row-1 >= 0 and col+1 <= 7:
            self.king_helper(row-1, col+1, row, col, moves)
        if row-1 >= 0 and col-1 >= 0:
            self.king_helper(row-1, col-1, row, col, moves)

    def king_helper(self, r, c, row, col, moves):
        if self.board[r][c] == "--" or self.board[r][c][0] != self.board[row][col][0]:
            moves.append(Move((row, col), (r, c), self.board))       

    """
    Functions to get the evaluation of the current position. FEN NEEDS TO BE FIXED
    """
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
    # def to_chess_board(self):
    #     # Create the empty board object
    #     board = chess.Board(fen="8/8/8/8/8/8/8/8 w - - 0 1")
        
    #     # Map the numpy array to the chessboard's squares
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board[row][col]
    #             if piece != "--":
    #                 # Determine the piece and place it on the board
    #                 chess_piece = piece[1].upper() if piece[0] == "w" else piece[1].lower()
    #                 square = chess.square(col, 7 - row)  # Flip rows to match board orientation
    #                 board.set_piece_at(square, chess.Piece.from_symbol(chess_piece)) 
    #     return board
    
    def get_evaluation(self):
        try:
            stockfish = Stockfish("/opt/homebrew/bin/stockfish", parameters={"Threads": 2, "Hash": 1024})
            stockfish.set_depth(20)
            fen = self.get_fen()
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()

            # Convert evaluation to centipawns if not mate
            if evaluation["type"] == "cp":
                eval_value = round(evaluation["value"] * 0.01, 1)
                mate_moves = None
            elif evaluation["type"] == "mate":
                eval_value = 10      
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

    # Overriding the equals method
    def __eq__(self, other):
        return isinstance(other, Move) and self.startRow == other.startRow and self.startCol == other.startCol and self.endRow == other.endRow and self.endCol == other.endCol
    def get_chess_notation(self):
        # make all chess noations for captures etc.
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]