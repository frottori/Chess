"""
Responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

# Global Constants
WIDTH = HEIGHT = 512                        # Resolution quality of the board (also 400)
DIMENSION = 8                               # Dimensions of a chess board are 8x8
SQUARE_SIZE = HEIGHT // DIMENSION           # Size of each square on the board
MAX_FPS = 15                                # For animations of pieces
IMAGES = {}                                 # Dictionary of images

def load_images(): 
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.smoothscale(p.image.load("Chess/images_blue_theme/" + piece + ".png"),(SQUARE_SIZE, SQUARE_SIZE))
        # e.g. IMAGES["wp"]

# Draws graphics of current game state 
def draw_game_state(screen, gstate):
    draw_board(screen)                   # Draw the squares on the board
    draw_pieces(screen, gstate.board)    # Draw the pieces on top of the squares

# Draw the squares on the board
def draw_board(screen):
    # the top left square is always light so we start with white
    colors = [p.Color("#a0b9cf"), p.Color("#7e98ac")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2] # Alternate the colors of the squares (odd or even) 
            p.draw.rect(screen, color, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # (x,y,width,height) x = col and y = row

# Draw the pieces on top of the squares with current game state from GameState.board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": 
                screen.blit(IMAGES[piece], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                # blit draws the image on the screen

def main():
    # Initialize a window
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))    # Set the window size
    p.display.set_caption("Chess")                  # Title of the window
    clock = p.time.Clock()                          # For animations (framerate)
    screen.fill(p.Color("white"))                   # Fill the screen with white color
    gs = ChessEngine.GameState()                    # Initialize the game state
    load_images()                                   # Load the images of the pieces

    running = True
    sqSelected = ()     # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []   # keep track of player 2 clicks (two tuples: [(6, 4), (4, 4)]) (source, destination)
    draw_game_state(screen, gs) # Draw the initial game state
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()         # (x, y) location of the mouse
                col = loc[0] // SQUARE_SIZE     # x / SQUARE_SIZE
                row = loc[1] // SQUARE_SIZE     # y / SQUARE_SIZE
                if sqSelected != (row, col):    # double click same square
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) 
                else:
                    sqSelected = ()
                    playerClicks = []
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    gs.make_move(move)
                    draw_game_state(screen, gs)
                    sqSelected = ()
                    playerClicks = []

        clock.tick(MAX_FPS) # Cap the framerate
        p.display.flip()    # Update the screen

if __name__ == "__main__":
    main()