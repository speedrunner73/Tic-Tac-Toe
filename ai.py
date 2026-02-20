from typing import override
import random
import math
from board import Board
from constants import *
from abc import ABC, abstractmethod

class BaseAI(ABC):
    def __init__(self, player: int) -> None:
        self.player = player
        self.opponent = PLAYER_1 if player == PLAYER_2 else PLAYER_2

    # Abstract function, implementing by the three subclasses
    @abstractmethod
    def get_move(self, board: Board) -> tuple[int, int]:
        raise NotImplementedError("Subclasses must implement this method")

class EasyAI(BaseAI):
    @override
    def get_move(self, board: Board) -> tuple[int, int]:
        moves = board.get_available_moves()

        # If the AI can win, take it
        for row, col in moves:
            if board.would_win(row, col, self.player):
                return row, col

        # 30% Chance to Block if in scenario
        probability = random.random()
        for row, col in moves:
            if board.would_win(row, col, self.opponent):
                if probability < 0.3:
                    return row, col
                break

        return random.choice(moves)

class NormalAI(BaseAI):
    @override
    def get_move(self, board: Board) -> tuple[int, int]:
        moves = board.get_available_moves()

        # Take the win
        for row, col in moves:
            if board.would_win(row, col, self.player):
                return row, col

        # Always block
        for row, col in moves:
            if board.would_win(row, col, self.opponent):
                return row, col

        # Take Center if needed
        if board.get_cell(1, 1) == EMPTY:
            return 1, 1

        # Take Corners as Second Priority
        corners = [(0,0), (0, 2), (2, 0), (2, 2)]
        available_corners = [
            (r, c) for (r, c) in corners
            if board.get_cell(r, c) == EMPTY
        ]

        if available_corners:
            return random.choice(available_corners)

        # Return random if all else fails
        return random.choice(moves)

class HardAI(BaseAI):
    @override
    def get_move(self, board: Board) -> tuple[int, int]:

        moves = board.get_available_moves()
        move_scores = []

        for row, col in moves:
            test_board = board.clone()
            test_board.place_move(row, col, self.player)

            score = self._minimax(test_board, maximizing=False)
            move_scores.append(((row, col), score))

        # Sort by score descending
        move_scores.sort(key=lambda x: x[1], reverse=True)

        best_score = move_scores[0][1]

        # Gather best moves
        best_moves = [move for move, score in move_scores if score == best_score]

        # ----------------------------------------
        # Opening Center Bias
        # ----------------------------------------
        if len(moves) == 9:
            if (1, 1) in best_moves and random.random() < 0.6:
                return 1, 1

        # ----------------------------------------
        # Controlled Imperfection
        # ----------------------------------------
        imperfection_rate = 0.15

        if len(move_scores) > 1 and random.random() < imperfection_rate:
            # Choose from second-tier moves
            second_best_score = move_scores[1][1]
            second_moves = [
                move for move, score in move_scores
                if score == second_best_score
            ]
            return random.choice(second_moves)

        # Otherwise optimal move
        return random.choice(best_moves)

    def _minimax(self, board: Board, maximizing: bool) -> int:
        winner = board.check_winner()

        # Terminate
        if winner == self.player:
            return 1
        elif winner == self.opponent:
            return -1
        elif board.is_full():
            return 0

        moves = board.get_available_moves()

        if maximizing:
            best_score = -math.inf
            for row, col in moves:
                test_board = board.clone()
                test_board.place_move(row, col, self.player)

                score = self._minimax(test_board, maximizing = False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = math.inf
            for row, col in moves:
                test_board = board.clone()
                test_board.place_move(row, col, self.opponent)

                score = self._minimax(test_board, maximizing = True)
                best_score = min(best_score, score)

            return best_score