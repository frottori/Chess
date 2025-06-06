"""
Responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine
from stockfish import Stockfish

# Global Constants
BOARD_SIZE = 600                            # Dimensions of the chessboard
DIMENSION = 8                               # Dimensions of a chess board are 8x8
SQUARE_SIZE = BOARD_SIZE // DIMENSION       # Size of each square on the board
BAR_WIDTH = SQUARE_SIZE // 2                # Width of the evaluation bar
BAR_HEIGHT = BOARD_SIZE                     # Height of the evaluation bar
WIDTH = BOARD_SIZE + BAR_WIDTH              # Total window width
HEIGHT = BOARD_SIZE                         # Total window height
MAX_FPS = 15                                # For animations of pieces
IMAGES = {}                                 # Dictionary of images

def load_images(): 
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.smoothscale(
            p.image.load("Chess/images_blue_theme/" + piece + ".png"),
            (SQUARE_SIZE, SQUARE_SIZE)
        )

# Draws graphics of current game state 
def draw_game_state(screen, gs):    
    draw_board(screen)                                      # Draw the squares on the board
    draw_pieces(screen, gs.board)                           # Draw the pieces on top of the squares
    draw_eval_bar(screen, gs)                               # Draw the evaluation bar
    
# Draw the squares on the board
def draw_board(screen):
    # Starting position of the chessboard (right of the evaluation bar)
    board_offset_x = BAR_WIDTH
    colors = [p.Color("#a0b9cf"), p.Color("#7e98ac")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]  # Alternate colors of squares
            p.draw.rect(
                screen, color, 
                p.Rect(board_offset_x + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )

# Draw the pieces on top of the squares with current game state from GameState.board
def draw_pieces(screen, board):
    board_offset_x = BAR_WIDTH
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": 
                screen.blit(
                    IMAGES[piece],
                    p.Rect(board_offset_x + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

# Function to draw the evaluation bar
def draw_eval_bar(screen, gs):
    eval_value, mate_moves = gs.get_evaluation()
    font = p.font.SysFont("Consolas", 14, bold=True)

    # Scale evaluation value to the range (-10 to 10) and normalize
    eval_clamped = max(-10, min(10, eval_value))  # Clamped to [-10, 10]
    white_bar_height = int((eval_clamped + 10) / 20 * HEIGHT)  # Normalize to [0, HEIGHT]

    # Display the evaluation value 
    eval_text = font.render(f"{abs(eval_value):.1f}", True, p.Color("#9b9b9b"))
    if eval_value > 0:
        text_rect = eval_text.get_rect(center=(BAR_WIDTH // 2, BAR_HEIGHT - 20))  # All the way down
    else:     
        text_rect = eval_text.get_rect(center=(BAR_WIDTH // 2, 20))  # All the way up
    p.draw.rect(screen, p.Color("#ffffff"), (0, BAR_HEIGHT - white_bar_height, BAR_WIDTH, white_bar_height))  # White bar
    p.draw.rect(screen, p.Color("#000000"), (0, 0, BAR_WIDTH, BAR_HEIGHT - white_bar_height))                 # Black bar

    # Display the mate or who won
    draw_black = False 
    draw_white = False
    
    if mate_moves == 0:   
        draw_black = True if gs.whiteToMove else False
        draw_white = True if not gs.whiteToMove else False
        text = "0-1" if gs.whiteToMove else "1-0"
        eval_text = font.render(text, True, p.Color("#9b9b9b"))
    elif mate_moves is not None:
        eval_text = font.render(f"M{mate_moves}", True, p.Color("#9b9b9b"))
        draw_black = True if not gs.whiteToMove else False
        draw_white = True if gs.whiteToMove else False

    if draw_black:
        text_rect = eval_text.get_rect(center=(BAR_WIDTH // 2, 20))                 # All the way up
        p.draw.rect(screen, p.Color("#000000"), (0, 0, BAR_WIDTH, BAR_HEIGHT))      # Black bar
    if draw_white:
        text_rect = eval_text.get_rect(center=(BAR_WIDTH // 2, BAR_HEIGHT - 20))    # All the way down
        p.draw.rect(screen, p.Color("#ffffff"), (0, 0, BAR_WIDTH, BAR_HEIGHT))      # White bar
    
    screen.blit(eval_text, text_rect)

def draw_selection(screen, gs, sqSelected, is_selected):
    board_offset_x = BAR_WIDTH
    row, col = sqSelected
    if row < 0 or col < 0:
        return
    if is_selected:
        color = p.Color("#8ec7e9") if (row + col) % 2 == 0 else p.Color("#378ccc") # highlight the square (dependig if light or dark square)
    else:
        color = p.Color("#a0b9cf") if (row + col) % 2 == 0 else p.Color("#7e98ac") # reset the color of the square
    p.draw.rect(
        screen, color, 
        p.Rect(board_offset_x + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4
    )

def main():
    # Initialize a window
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))    # Set the window size
    p.display.set_caption("Chess")                  # Title of the window
    clock = p.time.Clock()                          # For animations (framerate)
    screen.fill(p.Color("#a0b9cf"))                 # Fill the screen with white color
    gs = ChessEngine.GameState()                    # Initialize the game state

    validMoves = gs.get_valid_moves()
    moveMade = False
    load_images()                                   # Load the images of the pieces

    running = True
    sqSelected = ()     # square selected by the user (tuple: (row, col))
    playerClicks = []   # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    draw_game_state(screen, gs) # initial draw of the game state

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()  # (x, y) location of the mouse
                col = (loc[0] - BAR_WIDTH) // SQUARE_SIZE  # Adjust for board offset
                row = loc[1] // SQUARE_SIZE              
                if sqSelected != (row, col):    # double click same square
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    draw_selection(screen, gs, sqSelected, is_selected=True)
                else:
                    draw_selection(screen, gs, sqSelected, is_selected=False)
                    sqSelected = ()
                    playerClicks = []
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.make_move(move)
                        draw_selection(screen, gs, sqSelected, is_selected=False)
                        moveMade = True
                    else:
                        draw_selection(screen, gs, playerClicks[0], is_selected=False)
                        playerClicks = [playerClicks[1]]
                        draw_selection(screen, gs, sqSelected, is_selected=True)
            # Key Handler 
            elif e.type == p.KEYDOWN:
                if (valid_keystroke(e.key)):
                    gs.undo_move()
                    moveMade = True
        if moveMade:
            validMoves = gs.get_valid_moves()
            draw_game_state(screen, gs)   
            sqSelected = ()
            playerClicks = []
            moveMade = False
        # print(sqSelected)
        clock.tick(MAX_FPS)  # Cap the framerate
        p.display.flip()    # Update the screen

def valid_keystroke(key):
    return key == p.K_z and (p.key.get_mods() & p.KMOD_CTRL) or key == p.K_z and (p.key.get_mods() & p.KMOD_META)

if __name__ == "__main__":
    main()