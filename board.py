from constants import *
from typing import Optional

class Board:
    def __init__(self) -> None:
        self._board = [[EMPTY for _ in range(3)] for _ in range(3)]

    # =======================================================
    # get_cell(self, row: int, col: int) -> int
    #
    # Accessor method created to allow main.py to access
    # the value of a specific cell when needed
    # =======================================================
    def get_cell(self, row: int, col: int) -> int:
        # Handle exception
        if not (0 <= row < 3 and 0 <= col < 3):
            raise IndexError("OUT OF BOUNDS")

        return self._board[row][col]

    # =======================================================
    # place_move(self, row, col, int)
    #
    # If a value on the board at a specific point == -1
    # then replace the value with 0 or 1 depending on whose
    # turn is it, and return a boolean value based on if a
    # value was changed or not.
    # =======================================================
    def place_move(self, row: int, col: int, player: int) -> bool:
        # Bounds Check
        if not (0 <= row < 3 and 0 <= col < 3):
            return False

        # Determine if you can place value there or not
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player
            return True
        return False

    # =======================================================
    # is_board_full(self)
    #
    # Function determined to check if the game is over
    # based on 4 conditions:
    #   1. Horizontally across a row
    #   2. Vertically across a column
    #   3. Top Left to Bottom Right
    #   4. Bottom Left to Top Right
    # =======================================================
    def check_winner(self) -> Optional[int]:
        # Case 1: Rows
        for row in range(3):
            if self._board[row][0] == self._board[row][1] == self._board[row][2] and self._board[row][0] != EMPTY:
                return self._board[row][0]

        # Case 2: Columns
        for col in range(3):
            if self._board[0][col] == self._board[1][col] == self._board[2][col] and self._board[0][col] != EMPTY:
                return self._board[0][col]

        # Case 3: Diagonal TL -> BR
        if self._board[0][0] == self._board[1][1] == self._board[2][2] and self._board[0][0] != EMPTY:
            return self._board[0][0]

        # Case 4: Diagonal TR -> BL
        if self._board[0][2] == self._board[1][1] == self._board[2][0] and self._board[0][2] != EMPTY:
            return self._board[0][2]

        return None

    # =======================================================
    # is_full(self)
    #
    # Function determined to check if the board is full
    # Used in case of a tie or if we need to reset the game
    # =======================================================
    def is_full(self) -> bool:
        for row in self._board:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True

    # =======================================================
    # reset(self) -> None
    #
    # In the case a game ends, reset the game by setting
    # all values in grid to EMPTY [-1]
    # =======================================================
    def reset(self) -> None:
        for row in range(3):
            for col in range(3):
                self._board[row][col] = EMPTY

    # =======================================================
    # print(self) -> None:
    #
    # Function used to print the board onto the console for
    # checking to see if everything is running properly
    # and as intended
    # Should print out value of 0 or 1 based on if X or O was
    # selected, and any space not clicked on should be -1
    # =======================================================
    def print(self) -> None:
        for row in self._board:
            print(row)
        print()