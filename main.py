import pygame
import sys
from constants import *
from board import Board
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
# Utility Functions
# ======================================

def draw_grid() -> None:
    pygame.draw.line(screen, WHITE, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_THICKNESS)


def draw_pieces():
    for row in range(3):
        for col in range(3):
            cell = board.get_cell(row, col)
            if cell == PLAYER_1:
                pygame.draw.line(screen, BLUE,
                                 (col * SQUARE_SIZE + 40, row * SQUARE_SIZE + 40),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 40,
                                  row * SQUARE_SIZE + SQUARE_SIZE - 40),
                                 8)
                pygame.draw.line(screen, BLUE,
                                 (col * SQUARE_SIZE + 40,
                                  row * SQUARE_SIZE + SQUARE_SIZE - 40),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 40,
                                  row * SQUARE_SIZE + 40),
                                 8)

            elif cell == PLAYER_2:
                pygame.draw.circle(screen, RED,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 40,
                                   8)


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
    draw_grid()
    draw_pieces()

    if game_over:
        if winner is not None:
            message = f"Player {winner} Wins!"
        else:
            message = "Draw!"

        # Winner Text
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        padding = 20
        box_rect = text_rect.inflate(padding * 2, padding * 2)

        pygame.draw.rect(screen, BLACK, box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 3)

        screen.blit(text, text_rect)

        # Restart Button (below popup)
        restart_button.center = (WIDTH // 2, HEIGHT // 2 + 90)

        pygame.draw.rect(screen, BLACK, restart_button, border_radius=8)
        pygame.draw.rect(screen, WHITE, restart_button, 2, border_radius=8)

        restart_text = font.render("Restart", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        screen.blit(restart_text, restart_text_rect)

    pygame.display.update()
