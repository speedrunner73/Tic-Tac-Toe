import pygame
from constants import *


# --------------------------------------------------
# Grid
# --------------------------------------------------

def draw_grid(screen) -> None:

    # Vertical Lines
    pygame.draw.line(
        screen,
        GRID_COLOR,
        (BOARD_OFFSET_X + SQUARE_SIZE, 0),
        (BOARD_OFFSET_X + SQUARE_SIZE, BOARD_SIZE),
        LINE_THICKNESS
    )

    pygame.draw.line(
        screen,
        GRID_COLOR,
        (BOARD_OFFSET_X + 2 * SQUARE_SIZE, 0),
        (BOARD_OFFSET_X + 2 * SQUARE_SIZE, BOARD_SIZE),
        LINE_THICKNESS
    )

    # Horizontal Lines
    pygame.draw.line(
        screen,
        GRID_COLOR,
        (BOARD_OFFSET_X, SQUARE_SIZE),
        (BOARD_OFFSET_X + BOARD_SIZE, SQUARE_SIZE),
        LINE_THICKNESS
    )

    pygame.draw.line(
        screen,
        GRID_COLOR,
        (BOARD_OFFSET_X, 2 * SQUARE_SIZE),
        (BOARD_OFFSET_X + BOARD_SIZE, 2 * SQUARE_SIZE),
        LINE_THICKNESS
    )


# --------------------------------------------------
# Pieces
# --------------------------------------------------

def draw_pieces(screen, board) -> None:

    for row in range(3):
        for col in range(3):

            cell = board.get_cell(row, col)

            base_x = BOARD_OFFSET_X + col * SQUARE_SIZE
            base_y = row * SQUARE_SIZE

            if cell == PLAYER_1:
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (base_x + 40, base_y + 40),
                    (base_x + SQUARE_SIZE - 40,
                     base_y + SQUARE_SIZE - 40),
                    8
                )

                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (base_x + 40,
                     base_y + SQUARE_SIZE - 40),
                    (base_x + SQUARE_SIZE - 40,
                     base_y + 40),
                    8
                )

            elif cell == PLAYER_2:
                pygame.draw.circle(
                    screen,
                    O_COLOR,
                    (base_x + SQUARE_SIZE // 2,
                     base_y + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 2 - 40,
                    8
                )


# --------------------------------------------------
# Competitive Info Panel
# --------------------------------------------------

def draw_info_panel(screen, game):

    panel_rect = pygame.Rect(PANEL_OFFSET_X, 0, INFO_PANEL_WIDTH, HEIGHT)

    # Panel Background
    pygame.draw.rect(screen, PANEL_BG, panel_rect)

    # Left Divider
    pygame.draw.line(
        screen,
        PANEL_BORDER,
        (PANEL_OFFSET_X, 0),
        (PANEL_OFFSET_X, HEIGHT),
        3
    )

    y = PANEL_PADDING

    # MODE
    mode_label = game.section_font.render("MODE", True, PANEL_BORDER)
    screen.blit(mode_label, (PANEL_OFFSET_X + PANEL_PADDING, y))
    y += 40

    mode_value = "PLAYER VS PLAYER" if game.ai is None else "PLAYER VS AI"
    mode_surface = game.value_font.render(mode_value, True, X_COLOR)
    screen.blit(mode_surface, (PANEL_OFFSET_X + PANEL_PADDING, y))
    y += 70

    # DIFFICULTY
    if game.ai is not None:
        diff_label = game.section_font.render("DIFFICULTY", True, PANEL_BORDER)
        screen.blit(diff_label, (PANEL_OFFSET_X + PANEL_PADDING, y))
        y += 40

        difficulty = type(game.ai).__name__.replace("AI", "").upper()

        # Accent color
        if difficulty == "EASY":
            color = EASY_COLOR
        elif difficulty == "NORMAL":
            color = NORMAL_COLOR
        else:
            color = HARD_COLOR

        diff_surface = game.value_font.render(difficulty, True, color)
        screen.blit(diff_surface, (PANEL_OFFSET_X + PANEL_PADDING, y))
        y += 70

    # CURRENT TURN
    if game.state == GameState.PLAYING:

        turn_label = game.section_font.render("CURRENT TURN", True, PANEL_BORDER)
        screen.blit(turn_label, (PANEL_OFFSET_X + PANEL_PADDING, y))
        y += 40

        if game.current_player == PLAYER_1:
            turn_surface = game.value_font.render("X", True, X_COLOR)
        else:
            turn_surface = game.value_font.render("O", True, O_COLOR)

        screen.blit(turn_surface, (PANEL_OFFSET_X + PANEL_PADDING, y))


# --------------------------------------------------
# Post Game Overlay
# --------------------------------------------------

def draw_postgame_overlay(screen, font, winner, buttons):
    overlay = pygame.Surface((BOARD_SIZE, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # semi-transparent black
    screen.blit(overlay, (0, 0))

    if winner is not None:
        message = "X WINS" if winner == PLAYER_1 else "O WINS"
    else:
        message = "DRAW"

    text = font.render(message, True, PANEL_BORDER)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    padding = 20
    box_rect = text_rect.inflate(padding * 2, padding * 2)

    pygame.draw.rect(screen, PANEL_BG, box_rect)
    pygame.draw.rect(screen, PANEL_BORDER, box_rect, 3)

    screen.blit(text, text_rect)

    for button in buttons:
        button.draw(screen, font)


# --------------------------------------------------
# Menu Screen
# --------------------------------------------------

def draw_menu(screen, title, subtitle, title_font, subtitle_font, button_font, buttons):

    screen.fill(BACKGROUND)

    # Title
    title_surface = title_font.render(title.upper(), True, PANEL_BORDER)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160))
    screen.blit(title_surface, title_rect)

    # Subtitle
    subtitle_surface = subtitle_font.render(subtitle.upper(), True, PANEL_BORDER)
    subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(subtitle_surface, subtitle_rect)

    # Buttons
    for button in buttons:
        button.draw(screen, button_font)

def draw_win_line(screen, win_line, progress, winner):

    if not win_line:
        return

    line_type, index = win_line

    # Determine color based on winner
    if winner == PLAYER_1:
        color = X_COLOR
    else:
        color = O_COLOR

    start = None
    end = None

    # Horizontal
    if line_type == "row":
        y = index * SQUARE_SIZE + SQUARE_SIZE // 2
        start = (0, y)
        end = (BOARD_SIZE, y)

    # Vertical
    elif line_type == "col":
        x = index * SQUARE_SIZE + SQUARE_SIZE // 2
        start = (x, 0)
        end = (x, BOARD_SIZE)

    # Main diagonal
    elif line_type == "diag" and index == 0:
        start = (0, 0)
        end = (BOARD_SIZE, BOARD_SIZE)

    # Anti diagonal
    elif line_type == "diag" and index == 1:
        start = (BOARD_SIZE, 0)
        end = (0, BOARD_SIZE)

    # Interpolate animation
    current_x = start[0] + (end[0] - start[0]) * progress
    current_y = start[1] + (end[1] - start[1]) * progress

    pygame.draw.line(
        screen,
        color,
        start,
        (current_x, current_y),
        10
    )