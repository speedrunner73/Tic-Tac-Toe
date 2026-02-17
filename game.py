import pygame
from board import Board
from constants import *
from drawings import *


class Game:

    def __init__(self):
        self.board = Board()
        self.current_player = PLAYER_1
        self.winner = None
        self.game_over = False

        self.font = pygame.font.SysFont(None, 60)
        self.restart_button = pygame.Rect(0, 0, 200, 50)

    # -------------------------
    # Event Handling
    # -------------------------
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.game_over:
                if self.restart_button.collidepoint(event.pos):
                    self.reset()

            else:
                mouse_x, mouse_y = event.pos
                row = mouse_y // SQUARE_SIZE
                col = mouse_x // SQUARE_SIZE

                if self.board.place_move(row, col, self.current_player):

                    self.winner = self.board.check_winner()

                    if self.winner is not None:
                        self.game_over = True

                    elif self.board.is_full():
                        self.game_over = True

                    else:
                        self.current_player = (
                            PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
                        )

    # -------------------------
    # Reset
    # ------------------------
    def reset(self):
        self.board.reset()
        self.current_player = PLAYER_1
        self.winner = None
        self.game_over = False

    # -------------------------
    # Render
    # -------------------------
    def render(self, screen):
        draw_grid(screen)
        draw_pieces(screen, self.board)

        if self.game_over:
            draw_restart_button(
                screen,
                self.font,
                self.winner,
                self.restart_button
            )