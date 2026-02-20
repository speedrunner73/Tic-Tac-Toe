from board import Board
from drawings import *
from constants import *
from button import Button
from ai import EasyAI, NormalAI, HardAI
import random

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = PLAYER_1
        self.winner = None

        self.state = GameState.MODE_SELECT
        self.menu_buttons: list[Button] = []

        self.title_font = pygame.font.SysFont(None, 80)
        self.subtitle_font = pygame.font.SysFont(None, 40)

        self._enter_mode_select()

        self.ai_move_delay = 1000
        self.ai_move_start_time = None
        self.ai = None

        self.human_player = None
        self.ai_player = None

    # --------------------------------------------------
    # Event Handling
    # --------------------------------------------------
    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        # ---------------------------
        # MODE SELECT
        # ---------------------------
        if self.state == GameState.MODE_SELECT:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):
                    if button.label == "Player vs Player":
                        self.ai = None
                        self._enter_playing()
                    elif button.label == "Player vs AI":
                        self._enter_difficulty_select()

        # ---------------------------
        # DIFFICULTY SELECT
        # ---------------------------
        elif self.state == GameState.DIFFICULTY_SELECT:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):
                    # Difficulty selection placeholder (AI later)
                    if button.label == "Easy":
                        self.ai = EasyAI(PLAYER_2)
                    elif button.label == "Normal":
                        self.ai = NormalAI(PLAYER_2)
                    elif button.label == "Hard":
                        self.ai = HardAI(PLAYER_2)

                    self._enter_symbol_select()

        # ---------------------------
        # SYMBOL SELECTION
        # ---------------------------
        elif self.state == GameState.SYMBOL_SELECT:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):

                    if button.label == "Play as X":
                        self.human_player = PLAYER_1
                        self.ai_player = PLAYER_2
                    elif button.label == "Play as O":
                        self.human_player = PLAYER_2
                        self.ai_player = PLAYER_1

                    self.ai.player = self.ai_player
                    self.ai.opponent = self.human_player

                    self._enter_playing()

        # ---------------------------
        # PLAYING
        # ---------------------------
        elif self.state == GameState.PLAYING:

            # Ignore clicks if it's AI's turn
            if self.ai is not None and self.current_player == self.ai_player:
                return

            mouse_x, mouse_y = event.pos
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE

            if self.board.place_move(row, col, self.current_player):

                self.winner = self.board.check_winner()

                if self.winner is not None:
                    self._enter_game_over()

                elif self.board.is_full():
                    self._enter_game_over()

                else:
                    self.current_player = (
                        PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
                    )

        # ---------------------------
        # GAME OVER
        # ---------------------------
        elif self.state == GameState.GAME_OVER:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):
                    if button.label == "Restart":
                        self._enter_mode_select()

    # --------------------------------------------------
    # Rendering
    # --------------------------------------------------
    def render(self, screen):

        if self.state == GameState.MODE_SELECT:
            draw_menu(
                screen,
                "Tic Tac Toe",
                "Select Mode",
                self.title_font,
                self.subtitle_font,
                self.menu_buttons
            )

        elif self.state == GameState.DIFFICULTY_SELECT:
            draw_menu(
                screen,
                "Tic Tac Toe",
                "Select Difficulty",
                self.title_font,
                self.subtitle_font,
                self.menu_buttons
            )

        elif self.state == GameState.SYMBOL_SELECT:
            draw_menu(
                screen,
                "Tic Tac Toe",
                "Select Symbol",
                self.title_font,
                self.subtitle_font,
                self.menu_buttons
            )

        elif self.state == GameState.PLAYING:
            screen.fill(BLACK)
            draw_grid(screen)
            draw_pieces(screen, self.board)

        elif self.state == GameState.GAME_OVER:
            screen.fill(BLACK)
            draw_grid(screen)
            draw_pieces(screen, self.board)

            draw_postgame_overlay(
                screen,
                self.subtitle_font,
                self.winner,
                self.menu_buttons
            )

    # --------------------------------------------------
    # Update (Game Logic Loop)
    # --------------------------------------------------
    def update(self):

        # Only run AI logic during play state
        if (
                self.state == GameState.PLAYING
                and self.ai is not None
                and self.current_player == self.ai_player
        ):

            current_time = pygame.time.get_ticks()

            # Start timer if not started
            if self.ai_move_start_time is None:
                self.ai_move_start_time = current_time
                return

            # Wait until delay passes
            if current_time - self.ai_move_start_time >= self.ai_move_delay:

                row, col = self.ai.get_move(self.board)
                self.board.place_move(row, col, self.ai_player)

                self.winner = self.board.check_winner()

                if self.winner or self.board.is_full():
                    self._enter_game_over()
                else:
                    self.current_player = self.human_player

                # Reset timer
                self.ai_move_start_time = None


    # --------------------------------------------------
    # Button Layout Helper
    # --------------------------------------------------
    def _create_horizontal_buttons(self, labels: list[str]) -> list[Button]:

        buttons = []

        button_width = 240
        button_height = 60
        spacing = 40

        count = len(labels)
        total_width = count * button_width + (count - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 + 20

        for i, label in enumerate(labels):
            rect = pygame.Rect(
                start_x + i * (button_width + spacing),
                y,
                button_width,
                button_height
            )
            buttons.append(Button(rect, label))

        return buttons

    def _create_vertical_buttons(self, labels: list[str]) -> list[Button]:

        buttons = []

        button_width = 240
        button_height = 60
        spacing = 25

        count = len(labels)
        total_height = count * button_height + (count - 1) * spacing
        start_y = (HEIGHT - total_height) // 2 + 80
        x = (WIDTH - button_width) // 2

        for i, label in enumerate(labels):
            rect = pygame.Rect(
                x,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            buttons.append(Button(rect, label))

        return buttons

    # --------------------------------------------------
    # State Transitions
    # --------------------------------------------------
    def _enter_mode_select(self):
        self.menu_buttons = self._create_horizontal_buttons(
            ["Player vs Player", "Player vs AI"]
        )
        self.state = GameState.MODE_SELECT

    def _enter_difficulty_select(self):
        self.menu_buttons = self._create_vertical_buttons(
            ["Easy", "Normal", "Hard"]
        )
        self.state = GameState.DIFFICULTY_SELECT

    def _enter_symbol_select(self):
        self.menu_buttons = self._create_horizontal_buttons(
            ["Play as X", "Play as O"]
        )
        self.state = GameState.SYMBOL_SELECT

    def _enter_playing(self):
        self.board.reset()
        self.winner = None
        self.menu_buttons = []
        self.ai_move_start_time = None

        self.current_player = random.choice([PLAYER_1, PLAYER_2])

        if self.ai is None:
            # Player vs Player mode
            self.human_player = None
            self.ai_player = None
        else:
            # Player vs AI mode
            # human_player and ai_player were already set in symbol select
            pass

        self.state = GameState.PLAYING

    def _enter_game_over(self):
        self.menu_buttons = self._create_horizontal_buttons(["Restart"])
        self.state = GameState.GAME_OVER
