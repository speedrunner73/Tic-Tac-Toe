import pygame
from constants import *

def draw_grid(screen) -> None:
    pygame.draw.line(screen, WHITE, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_THICKNESS)


def draw_pieces(screen, board) -> None:
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

def draw_restart_button(screen, font, winner, restart_button) -> None:
    if winner is not None:
        message = f"Player {winner} Wins!"
    else:
        message = "Draw!"

    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    padding = 20
    box_rect = text_rect.inflate(padding * 2, padding * 2)

    pygame.draw.rect(screen, BLACK, box_rect)
    pygame.draw.rect(screen, WHITE, box_rect, 3)
    screen.blit(text, text_rect)

    restart_button.center = (WIDTH // 2, HEIGHT // 2 + 90)

    pygame.draw.rect(screen, BLACK, restart_button, border_radius=8)
    pygame.draw.rect(screen, WHITE, restart_button, 2, border_radius=8)

    restart_text = font.render("Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)
