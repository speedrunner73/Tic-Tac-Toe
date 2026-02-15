import pygame
import sys
from constants import *
from board import Board
from drawings import *
pygame.init()

# ======================================
# Setup
# ======================================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tic_tac_toe")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)
restart_button = pygame.Rect(0, 0, 200, 50)
board = Board()

current_player = PLAYER_1
game_over = False
winner = None


# ======================================
# Main Loop
# ======================================

running = True
while running:
    clock.tick(60)

    # -------- Event Handling --------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:
                if restart_button.collidepoint(event.pos):
                    board.reset()
                    current_player = PLAYER_1
                    game_over = False
                    winner = None

            else:
                mouse_x, mouse_y = event.pos
                row = mouse_y // SQUARE_SIZE
                col = mouse_x // SQUARE_SIZE

                if board.place_move(row, col, current_player):
                    winner = board.check_winner()

                    if winner is not None:
                        print(f"Winner: Player {winner}")
                        game_over = True
                    elif board.is_full():
                        print("Draw!")
                        game_over = True
                    else:
                        current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1


    # -------- Rendering --------
    screen.fill(BLACK)
    draw_grid(screen)
    draw_pieces(screen, board)

    if game_over:
        draw_restart_button(screen, font, winner, restart_button)

    pygame.display.update()
