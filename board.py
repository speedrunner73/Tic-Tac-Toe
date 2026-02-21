from constants import *

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
    def check_winner(self):

        # Rows
        for row in range(3):
            if (
                    self._board[row][0] != EMPTY and
                    self._board[row][0] == self._board[row][1] == self._board[row][2]
            ):
                return self._board[row][0], ("row", row)

        # Columns
        for col in range(3):
            if (
                    self._board[0][col] != EMPTY and
                    self._board[0][col] == self._board[1][col] == self._board[2][col]
            ):
                return self._board[0][col], ("col", col)

        # Main diagonal
        if (
                self._board[0][0] != EMPTY and
                self._board[0][0] == self._board[1][1] == self._board[2][2]
        ):
            return self._board[0][0], ("diag", 0)

        # Anti diagonal
        if (
                self._board[0][2] != EMPTY and
                self._board[0][2] == self._board[1][1] == self._board[2][0]
        ):
            return self._board[0][2], ("diag", 1)

        return None, None

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

    # =======================================================
    # clone() -> "Board"
    #
    # Function used to create a copy of the board that an AI
    # can use to use its algorithms implemented to determine
    # the most optimal move
    # =======================================================
    def clone(self):
        new_board = Board()
        new_board._board = [row[:] for row in self._board]
        return new_board

    # =======================================================
    # get_available_moves(self) -> list[tuple[int, int]]
    #
    # Function for AI to give it the list of spaces that the
    # AI can work with instead of using what is already there
    # and working over what is already done
    # =======================================================
    def get_available_moves(self) -> list[tuple[int, int]]:
        moves = []
        for row in range(3):
            for col in range(3):
                if self._board[row][col] == EMPTY:
                    moves.append((row, col))

        return moves

    # =======================================================
    # would_win() -> bool
    #
    # This function is still fair game because the AI needs
    # to actually work and not just be dumb and place random
    # X's or O's and actually check if it is a good idea to
    # place it.
    # =======================================================
    def would_win(self, row: int, col: int, player: int) -> bool:
        if self.get_cell(row, col) != EMPTY:
            return False

        test_board = self.clone()
        test_board.place_move(row, col, player)

        winner, _ = test_board.check_winner()
        return winner == player
