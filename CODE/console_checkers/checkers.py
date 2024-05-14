import numpy as np
import time
from typing import Tuple, List

from consts import *


class Checkers:
    def __init__(self) -> None:
        self.board = self._init_board()
        self.player = WHITE

    def _init_board(self) -> np.ndarray:
        board = np.empty((SIZE, SIZE))
        board.fill(0)
        for row in range(SIZE):
            if row == 3 or row == 4:
                continue
            for col in range(SIZE):
                if (row + 1) % 2 == 1:
                    if col % 2 == 1:
                        board[row, col] = BLACK_R if row <= 2 else WHITE_R
                else:
                    if col % 2 == 0:
                        board[row, col] = BLACK_R if row <= 2 else WHITE_R

        return board

    def select_piece(self) -> Tuple[int, int]:
        valid_row = False
        valid_col = False

        while valid_row is False:
            row = input("Enter row to select piece from: ")
            try:
                row = int(row)
            except:
                print("selected row must be an integer")
                continue
            if row not in range(1, 9):
                print("row must be in range of 1-8, shown on left side of board")

            row = 8 - row
            valid_row = True

        while valid_col is False:
            col = input("Enter column to select from: ")
            try:
                col = COLS_TO_NUMS[col]
            except:
                print("selected columns must be a letter between A-H")
                continue
            if col not in range(0, 8):
                print(
                    "column must be an letter between A-H shown at the top of the board"
                )

            valid_col = True

        if self.square_is_empty(row, col) is True:
            return self.select_piece()

        return row, col

    def square_is_empty(self, row: int, col: int) -> bool:
        if self.board[row, col] == 0:
            return True
        else:
            return False

    def get_all_valid_moves(self):
        moves = {"simple": [], "takes": []}
        for row in range(SIZE):
            for col in range(SIZE):
                piece = self.board[row, col]
                if piece in WHITES and self.player == WHITE:
                    moves["simple"] += self._get_valid_simple_moves(row, col)
                    moves["takes"] += self._get_valid_take_moves(row, col)
                elif piece in BLACKS and self.player == BLACK:
                    moves["simple"] += self._get_valid_simple_moves(row, col)
                    moves["takes"] += self._get_valid_take_moves(row, col)

        return moves

    def _get_valid_simple_moves(self, row: int, col: int):
        piece = self.board[row, col]
        valid_moves = []
        if self.player == BLACK:
            if piece == 2:
                for dir in LEGAL_DIRS[BLACK]["king"]:
                    if (
                        row + dir[0] in range(8)
                        and col + dir[1] in range(8)
                        and self.square_is_empty(row + dir[0], col + dir[1])
                    ):
                        valid_moves.append(((row, col), (row + dir[0], col + dir[1])))
            elif piece == 1:
                for dir in LEGAL_DIRS[BLACK]["regular"]:
                    if (
                        row + dir[0] in range(8)
                        and col + dir[1] in range(8)
                        and self.square_is_empty(row + dir[0], col + dir[1])
                    ):
                        valid_moves.append(((row, col), (row + dir[0], col + dir[1])))
        elif self.player == WHITE:
            if piece == 4:
                for dir in LEGAL_DIRS[WHITE]["king"]:
                    if (
                        row + dir[0] in range(8)
                        and col + dir[1] in range(8)
                        and self.square_is_empty(row + dir[0], col + dir[1])
                    ):
                        valid_moves.append(((row, col), (row + dir[0], col + dir[1])))
            elif piece == 3:
                for dir in LEGAL_DIRS[WHITE]["regular"]:
                    if (
                        row + dir[0] in range(8)
                        and col + dir[1] in range(8)
                        and self.square_is_empty(row + dir[0], col + dir[1])
                    ):
                        valid_moves.append(((row, col), (row + dir[0], col + dir[1])))

        return valid_moves

    def _get_valid_take_moves(self, row: int, col: int):
        piece = self.board[row, col]
        valid_moves = []
        if self.player == BLACK:
            if piece == 2:
                for dir in LEGAL_DIRS[BLACK]["king"]:
                    if (
                        row + 2 * dir[0] in range(8)
                        and col + 2 * dir[1] in range(8)
                        and self.board[row + dir[0], col + dir[1]] in WHITES
                        and self.square_is_empty(row + 2 * dir[0], col + 2 * dir[1])
                    ):
                        valid_moves.append(
                            ((row, col), (row + 2 * dir[0], col + 2 * dir[1]))
                        )
            elif piece == 1:
                for dir in LEGAL_DIRS[BLACK]["regular"]:
                    if (
                        row + 2 * dir[0] in range(8)
                        and col + 2 * dir[1] in range(8)
                        and self.board[row + dir[0], col + dir[1]] in WHITES
                        and self.square_is_empty(row + 2 * dir[0], col + 2 * dir[1])
                    ):
                        valid_moves.append(
                            ((row, col), (row + 2 * dir[0], col + 2 * dir[1]))
                        )
        elif self.player == WHITE:
            if piece == 4:
                if (
                    row + 2 * dir[0] in range(8)
                    and col + 2 * dir[1] in range(8)
                    and self.board[row + dir[0], col + dir[1]] in BLACKS
                    and self.square_is_empty(row + 2 * dir[0], col + 2 * dir[1])
                ):
                    valid_moves.append(
                        ((row, col), (row + 2 * dir[0], col + 2 * dir[1]))
                    )
            elif piece == 3:
                for dir in LEGAL_DIRS[WHITE]["regular"]:
                    if (
                        row + 2 * dir[0] in range(8)
                        and col + 2 * dir[1] in range(8)
                        and self.board[row + dir[0], col + dir[1]] in BLACKS
                        and self.square_is_empty(row + 2 * dir[0], col + 2 * dir[1])
                    ):
                        valid_moves.append(
                            ((row, col), (row + 2 * dir[0], col + 2 * dir[1]))
                        )

        return valid_moves

    def render(self) -> None:
        cols = ["X", "A", "B", "C", "D", "E", "F", "G", "H"]
        print(str.join(" | ", cols))
        for row in range(SIZE):
            print("----------------------------------")
            print(
                str(8 - row),
                "|",
                str.join(" | ", [NUM_TO_STR[int(x)] for x in self.board[row, :]]),
            )
        print("----------------------------------")

    @staticmethod
    def convert_rowcol_to_user(row: int, col: int) -> Tuple[int, str]:
        row = 8 - row
        return row, NUMS_TO_COLS[col]

    @staticmethod
    def convert_rowcol_to_game(row: int, col: str) -> Tuple[int, int]:
        row = 8 - row
        return row, COLS_TO_NUMS[col]

    def select_move(self):
        valid_row = False
        valid_col = False

        while valid_row is False:
            row = input("Enter row to select place to move to: ")
            try:
                row = int(row)
            except:
                print("selected row must be an integer")
                continue
            if row not in range(1, 9):
                print("row must be in range of 1-8, shown on left side of board")

            row = 8 - row
            valid_row = True

        while valid_col is False:
            col = input("Enter column to move to: ")
            try:
                col = COLS_TO_NUMS[col]
            except:
                print("selected columns must be a letter between A-H")
                continue
            if col not in range(0, 8):
                print(
                    "column must be an letter between A-H shown at the top of the board"
                )

            valid_col = True

        if self.square_is_empty(row, col) is False:
            return self.select_move()

        return row, col

    def clear(self, row: int, col: int) -> None:
        self.board[row, col] = 0

    @property
    def opposite_player(self):
        return WHITE if self.player == BLACK else BLACK

    def move(self):
        valid_selection = False
        row, col = None, None
        valid_moves = self.get_all_valid_moves()
        valid_simples, valid_takes = valid_moves["simple"], valid_moves["takes"]
        valid_selections = (
            [x[0] for x in valid_takes]
            if len(valid_takes) > 0
            else [x[0] for x in valid_simples]
        )

        if len(valid_simples) == 0 and len(valid_takes) == 0:
            print("GAME OVER")
            print(f"PLAYER {self.opposite_player} WON")
            time.sleep(5)
            quit()

        while valid_selection is False:
            print(
                f"Valid pieces to move are {set([Checkers.convert_rowcol_to_user(*x) for x in valid_selections])}"
            )

            row, col = self.select_piece()
            if (row, col) not in valid_selections:
                print("Please select a valid piece")
                continue
            valid_selection = True

        valid_move = False
        valid_moves = (
            [x[1] for x in valid_takes]
            if len(valid_takes) > 0
            else [x[1] for x in valid_simples if x[0] == (row, col)]
        )
        while valid_move is False:
            print(
                f"Valid moves for this piece are {set([Checkers.convert_rowcol_to_user(*x) for x in valid_moves])}"
            )
            new_row, new_col = self.select_move()
            if (new_row, new_col) not in valid_moves:
                print("Please select a valid move")
                continue
            valid_move = True

        self.board[new_row, new_col] = self.board[row, col]
        self.clear(row, col)

        if abs(new_row - row) == 2:
            one_row = 0.5 * (new_row - row)
            one_col = 0.5 * (new_col - col)
            self.clear(int(row + one_row), int(col + one_col))
        else:
            self.player = self.opposite_player


game = Checkers()
game.render()
while True:
    print(f"It is {game.player}s turn")
    game.move()
    game.render()
