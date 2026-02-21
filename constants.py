from enum import Enum

# --------------------------------------------------
# Screen & Layout
# --------------------------------------------------

LINE_THICKNESS = 10

BOARD_SIZE = 600
INFO_PANEL_WIDTH = 400

WIDTH = BOARD_SIZE + INFO_PANEL_WIDTH
HEIGHT = BOARD_SIZE

SQUARE_SIZE = BOARD_SIZE // 3

BOARD_OFFSET_X = 0
PANEL_OFFSET_X = BOARD_SIZE

PANEL_PADDING = 40


# --------------------------------------------------
# Competitive E-Sports Color System
# --------------------------------------------------

BACKGROUND = (8, 10, 20)
PANEL_BG = (15, 8, 35)
GRID_COLOR = (40, 60, 110)
PANEL_BORDER = (200, 220, 255)

# Player Colors
X_COLOR = (0, 220, 255)      # Electric Blue
O_COLOR = (255, 70, 120)     # Neon Red

# Button Colors
BUTTON_BG = (25, 25, 40)
BUTTON_HOVER = (45, 45, 70)
BUTTON_BORDER = (90, 90, 140)

# Difficulty Accent Colors
EASY_COLOR = (0, 255, 100)
NORMAL_COLOR = (255, 210, 0)
HARD_COLOR = (255, 40, 40)


# --------------------------------------------------
# Player Turns
# --------------------------------------------------

EMPTY = -1
PLAYER_1 = 0  # X
PLAYER_2 = 1  # O


# --------------------------------------------------
# Game State Enums
# --------------------------------------------------

class GameState(Enum):
    MODE_SELECT = 0
    DIFFICULTY_SELECT = 1
    SYMBOL_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4