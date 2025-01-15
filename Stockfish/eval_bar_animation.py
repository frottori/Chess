import chess
import chess.pgn
from stockfish import Stockfish
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 100, 500
BAR_WIDTH = 100
BAR_X = (WIDTH - BAR_WIDTH) // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Evaluation Bar")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
MIDPOINT_COLOR = (155, 155, 155)  

# Font for displaying evaluation
font = pygame.font.Font(None, 36)

# Function to draw the evaluation bar
def draw_eval_bar(eval_value, smooth_value):
    screen.fill(GRAY)  # Background

    # Scale evaluation value to the range (-10 to 10) and normalize
    eval_clamped = max(-10, min(10, smooth_value))  # Clamped to [-10, 10]
    white_bar_height = int((eval_clamped + 10) / 20 * HEIGHT)  # Normalize to [0, HEIGHT]

    # Draw the bars
    pygame.draw.rect(screen, WHITE, (BAR_X, HEIGHT - white_bar_height, BAR_WIDTH, white_bar_height))  # White bar
    pygame.draw.rect(screen, BLACK, (BAR_X, 0, BAR_WIDTH, HEIGHT - white_bar_height))  # Black bar

    # Draw midpoint line
    pygame.draw.line(
        screen, MIDPOINT_COLOR, 
        (BAR_X, HEIGHT // 2), (BAR_X + BAR_WIDTH, HEIGHT // 2), 3
    )  # Horizontal midpoint line

    # Display the evaluation value
    eval_text = font.render(f"{eval_value:.2f}", True, RED)
    text_rect = eval_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 20))  # Centered above midpoint line
    screen.blit(eval_text, text_rect)

    # Update the display
    pygame.display.flip()

# Path to Stockfish binary
stockfish = Stockfish("/opt/homebrew/bin/stockfish", parameters={"Threads": 2, "Hash": 1024})

# Path to your PGN file
username = input("Enter the username for the latest PGN game: ")
pgn_path = f"PGNs/{username}_latest_game.pgn"
if not username:
    pgn_path = "PGNs/magnuscarlsen_latest_game.pgn"

# Open the PGN file
with open(pgn_path) as pgn_file:
    game = chess.pgn.read_game(pgn_file)

# Initialize variables
board = game.board()
evaluations = []
current_eval = 0.0  # Start with an even evaluation

# Main game loop
for move in game.mainline_moves():
    board.push(move)  # Make the move on the board
    stockfish.set_fen_position(board.fen())  # Set the position in Stockfish
    evaluation = stockfish.get_evaluation()  # Get the evaluation from Stockfish

    # Convert evaluation to centipawns if not mate
    if evaluation["type"] == "cp":
        eval_value = round(evaluation["value"] * 0.01, 2)
    elif evaluation["type"] == "mate":
        eval_value = 10 if evaluation["value"] > 0 else -10  # Approximation for mate

    evaluations.append((move, eval_value))

    # Smoothly transition from current_eval to eval_value
    steps = 50  # Number of animation steps
    for step in range(steps):
        smooth_eval = current_eval + (eval_value - current_eval) * (step / steps)
        draw_eval_bar(eval_value, smooth_eval)
        time.sleep(0.02)  # Pause for smoother animation

        # Pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Update current evaluation
    current_eval = eval_value

# Wait a bit before exiting
pygame.time.wait(3000)
pygame.quit()