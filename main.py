import pygame
import sys

pygame.init()

# ======================================
# Constants
# ======================================
WIDTH = HEIGHT = 600
SQUARE_SIZE = WIDTH // 3
LINE_THICKNESS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

EMPTY = -1
PLAYER_1 = 0  # X (Blue)
PLAYER_2 = 1  # O (Red)

# ======================================
# Setup
# ======================================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tic_tac_toe")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

board = [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
]

current_player = PLAYER_1
game_over = False
winner = None

# ======================================
# Utility Functions
# ======================================

def print_board(board):
    for row in board:
        print(row)
    print()


def draw_grid():
    pygame.draw.line(screen, WHITE, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_THICKNESS)
    pygame.draw.line(screen, WHITE, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_THICKNESS)


def draw_pieces():
    for row in range(3):
        for col in range(3):

            if board[row][col] == PLAYER_1:
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

            elif board[row][col] == PLAYER_2:
                pygame.draw.circle(screen, RED,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 40,
                                   8)


def check_winner(board):

    # Rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]

    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    # Diagonal TL -> BR
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]

    # Diagonal TR -> BL
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


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

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = event.pos
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE

            if board[row][col] == EMPTY:
                board[row][col] = current_player
                print_board(board)

                winner = check_winner(board)

                if winner is not None:
                    print(f"Winner: Player {winner}")
                    game_over = True
                elif is_board_full(board):
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

        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Create padded black box around text
        padding = 20
        box_rect = text_rect.inflate(padding * 2, padding * 2)

        pygame.draw.rect(screen, BLACK, box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 3)  # Optional white border

        screen.blit(text, text_rect)


    pygame.display.update()
