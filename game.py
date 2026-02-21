import random

from board import Board
from drawings import *
from constants import *
from button import Button
from ai import EasyAI, NormalAI, HardAI


class Game:

    def __init__(self):

        self.board = Board()
        self.current_player = PLAYER_1
        self.winner = None

        self.state = GameState.MODE_SELECT
        self.menu_buttons: list[Button] = []

        # Competitive Fonts (replace path with your Hemi Head file)
        self.title_font = pygame.font.Font("assets/fonts/HemiHead426.ttf", 72)
        self.section_font = pygame.font.Font("assets/fonts/HemiHead426.ttf", 32)
        self.value_font = pygame.font.Font("assets/fonts/HemiHead426.ttf", 42)
        self.symbol_font = pygame.font.Font("assets/fonts/HemiHead426.ttf", 100)

        self._enter_mode_select()

        # AI Settings
        self.ai_move_delay = 1000
        self.ai_move_start_time = None
        self.ai = None

        self.human_player = None
        self.ai_player = None

        # Winning Line
        self.win_line = None
        self.win_animation_progress = 0
        self.win_animation_speed = 0.05

    # --------------------------------------------------
    # Event Handling
    # --------------------------------------------------

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        # ---------------- MODE SELECT ----------------
        if self.state == GameState.MODE_SELECT:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):

                    if button.label == "Player vs Player":
                        self.ai = None
                        self._enter_playing()

                    elif button.label == "Player vs AI":
                        self._enter_difficulty_select()

        # ---------------- DIFFICULTY ----------------
        elif self.state == GameState.DIFFICULTY_SELECT:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):

                    if button.label == "Easy":
                        self.ai = EasyAI(PLAYER_2)
                    elif button.label == "Normal":
                        self.ai = NormalAI(PLAYER_2)
                    elif button.label == "Hard":
                        self.ai = HardAI(PLAYER_2)

                    self._enter_symbol_select()

        # ---------------- SYMBOL ----------------
        elif self.state == GameState.SYMBOL_SELECT:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):

                    if button.label == "X":
                        self.human_player = PLAYER_1
                        self.ai_player = PLAYER_2
                    elif button.label == "O":
                        self.human_player = PLAYER_2
                        self.ai_player = PLAYER_1

                    self.ai.player = self.ai_player
                    self.ai.opponent = self.human_player

                    self._enter_playing()

        # ---------------- PLAYING ----------------
        elif self.state == GameState.PLAYING:

            # Ignore clicks if AI turn
            if self.ai is not None and self.current_player == self.ai_player:
                return

            mouse_x, mouse_y = event.pos
            row = mouse_y // SQUARE_SIZE
            col = (mouse_x - BOARD_OFFSET_X) // SQUARE_SIZE

            if 0 <= col < 3 and 0 <= row < 3:

                if self.board.place_move(row, col, self.current_player):

                    self.winner, self.win_line = self.board.check_winner()

                    if self.winner is not None or self.board.is_full():
                        self._enter_game_over()
                    else:
                        self.current_player = (
                            PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
                        )

        # ---------------- GAME OVER ----------------
        elif self.state == GameState.GAME_OVER:
            for button in self.menu_buttons:
                if button.is_clicked(event.pos):
                    if button.label == "Restart":
                        self._enter_mode_select()

    # --------------------------------------------------
    # Rendering
    # --------------------------------------------------

    def render(self, screen):

        # --------------------------------------------------
        # MENU STATES
        # --------------------------------------------------
        if self.state in (
                GameState.MODE_SELECT,
                GameState.DIFFICULTY_SELECT,
                GameState.SYMBOL_SELECT
        ):

            if self.state == GameState.MODE_SELECT:
                subtitle = "SELECT MODE"
                button_font = self.section_font

            elif self.state == GameState.DIFFICULTY_SELECT:
                subtitle = "SELECT DIFFICULTY"
                button_font = self.section_font

            else:  # SYMBOL_SELECT
                subtitle = "SELECT SIDE"
                button_font = self.symbol_font

            draw_menu(
                screen,
                "TIC TAC TOE",
                subtitle,
                self.title_font,
                self.section_font,
                button_font,
                self.menu_buttons
            )

            return

        # --------------------------------------------------
        # GAME STATES (PLAYING / GAME_OVER)
        # --------------------------------------------------
        screen.fill(BACKGROUND)

        # Draw board
        draw_grid(screen)
        draw_pieces(screen, self.board)

        # Draw win animation (only if someone won)
        if (
                self.state == GameState.GAME_OVER
                and self.winner is not None
        ):
            draw_win_line(
                screen,
                self.win_line,
                self.win_animation_progress,
                self.winner
            )

        # Draw info panel
        draw_info_panel(screen, self)

        # Draw postgame overlay
        if self.state == GameState.GAME_OVER:
            draw_postgame_overlay(
                screen,
                self.value_font,
                self.winner,
                self.menu_buttons
            )

    # --------------------------------------------------
    # Update (AI Loop)
    # --------------------------------------------------

    def update(self):

        # ------------------------------
        # AI TURN LOGIC
        # ------------------------------
        if (
            self.state == GameState.PLAYING
            and self.ai is not None
            and self.current_player == self.ai_player
        ):

            current_time = pygame.time.get_ticks()

            # Start delay timer
            if self.ai_move_start_time is None:
                self.ai_move_start_time = current_time
                return

            # Wait for delay
            if current_time - self.ai_move_start_time >= self.ai_move_delay:

                row, col = self.ai.get_move(self.board)
                self.board.place_move(row, col, self.ai_player)

                self.winner, self.win_line = self.board.check_winner()

                if self.winner or self.board.is_full():
                    self.win_animation_progress = 0
                    self._enter_game_over()
                else:
                    self.current_player = self.human_player

                self.ai_move_start_time = None

        # ------------------------------
        # WIN LINE ANIMATION
        # ------------------------------
        if (
            self.state == GameState.GAME_OVER
            and self.win_line is not None
        ):
            if self.win_animation_progress < 1:
                self.win_animation_progress += 0.05

    # --------------------------------------------------
    # Button Layout Helpers
    # --------------------------------------------------

    def _create_horizontal_buttons(self, labels: list[str]) -> list[Button]:
        buttons = []
        spacing = 40
        padding_x = 30
        padding_y = 18

        # First measure all buttons
        widths = []

        for label in labels:
            text_surface = self.section_font.render(label.upper(), True, PANEL_BORDER)
            width = text_surface.get_width() + padding_x * 2
            widths.append(width)

        total_width = sum(widths) + spacing * (len(labels) - 1)
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 + 20

        current_x = start_x

        for i, label in enumerate(labels):
            button_width = widths[i]
            button_height = text_surface.get_height() + padding_y * 2

            rect = pygame.Rect(
                current_x,
                y,
                button_width,
                button_height
            )

            buttons.append(Button(rect, label))

            current_x += button_width + spacing

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
        self.menu_buttons = []

        labels = ["Easy", "Normal", "Hard"]
        colors = [EASY_COLOR, NORMAL_COLOR, HARD_COLOR]

        button_width = 260
        button_height = 70
        spacing = 30

        total_height = len(labels) * button_height + (len(labels) - 1) * spacing
        start_y = (HEIGHT - total_height) // 2 + 80
        x = (WIDTH - button_width) // 2

        for i, label in enumerate(labels):
            rect = pygame.Rect(
                x,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )

            self.menu_buttons.append(
                Button(rect, label, accent_color=colors[i])
            )

        self.state = GameState.DIFFICULTY_SELECT

    def _enter_symbol_select(self):

        self.menu_buttons = []

        labels = ["X", "O"]
        colors = [X_COLOR, O_COLOR]

        button_size = 120
        spacing = 120

        total_width = 2 * button_size + spacing
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT // 2

        for i, label in enumerate(labels):
            rect = pygame.Rect(
                start_x + i * (button_size + spacing),
                y,
                button_size,
                button_size
            )

            self.menu_buttons.append(
                Button(rect, label, accent_color=colors[i])
            )

        self.state = GameState.SYMBOL_SELECT

    def _enter_playing(self):

        self.board.reset()
        self.winner = None
        self.menu_buttons = []
        self.ai_move_start_time = None

        self.current_player = random.choice([PLAYER_1, PLAYER_2])

        if self.ai is None:
            self.human_player = None
            self.ai_player = None

        self.state = GameState.PLAYING

    def _enter_game_over(self):
        button_width = 240
        button_height = 60

        x = (WIDTH - button_width) // 2
        y = HEIGHT // 2 + 60

        rect = pygame.Rect(x, y, button_width, button_height)
        self.menu_buttons = [Button(rect, "Restart")]
        self.state = GameState.GAME_OVER