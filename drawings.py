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

def draw_postgame_overlay(screen, font, winner, buttons) -> None:

    if winner is not None:
        message = f"Player {winner} Wins!"
    else:
        message = "Draw!"

    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

    padding = 20
    box_rect = text_rect.inflate(padding * 2, padding * 2)

    pygame.draw.rect(screen, BLACK, box_rect)
    pygame.draw.rect(screen, WHITE, box_rect, 3)
    screen.blit(text, text_rect)

    for button in buttons:
        button.draw(screen, font)



def draw_menu(screen, title, subtitle, t_font,s_font, buttons):
    screen.fill(BLACK)

    # Title
    title_surface = t_font.render(title, True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140))
    screen.blit(title_surface, title_rect)

    # Subtitle
    subtitle_surface = s_font.render(subtitle, True, WHITE)
    subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(subtitle_surface, subtitle_rect)

    # Buttons
    for button in buttons:
        button.draw(screen, s_font)