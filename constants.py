from enum import Enum

# Screen and Grid
WIDTH = HEIGHT = 600
SQUARE_SIZE = WIDTH // 3
LINE_THICKNESS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Player Turns
EMPTY = -1
PLAYER_1 = 0  # X (Blue)
PLAYER_2 = 1  # O (Red)

# Game State Enums
class GameState(Enum):
    MODE_SELECT = 0
    DIFFICULTY_SELECT = 1
    SYMBOL_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4