"""
Responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

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
def drawGameState(screen, gstate):
    drawBoard(screen)                   # Draw the squares on the board
    drawPieces(screen, gstate.board)    # Draw the pieces on top of the squares

# Draw the squares on the board
def drawBoard(screen):
    # the top left square is always light so we start with white
    colors = [p.Color("#a0b9cf"), p.Color("#7e98ac")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2] # Alternate the colors of the squares (odd or even) 
            p.draw.rect(screen, color, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # (x,y,width,height) x = col and y = row

# Draw the pieces on top of the squares with current game state from GameState.board
def drawPieces(screen, board):
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
    playerClicks = []   # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS) # Cap the framerate
        p.display.flip()    # Update the screen

if __name__ == "__main__":
    main()