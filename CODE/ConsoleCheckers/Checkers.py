from ConsoleCheckers.consts import *

import numpy as np
import os

from typing import Tuple, Dict, List


def clear_window():
    os.system("cls")


class CheckersBoard:
    def __init__(self) -> None:
        self._board = self._init_board()
        self._last_piece_moved = None
        self._player = WHITE
        self._moves_no_capture = 0

    @property
    def opposite_player(self) -> str:
        return WHITE if self._player == BLACK else BLACK

    @property
    def player(self):
        return self._player

    @property
    def n_black_pieces(self):
        n = 0
        for row in range(SIZE):
            for col in range(SIZE):
                if self._board[row, col] in BLACKS:
                    n += 1

        return n

    @property
    def n_white_pieces(self):
        n = 0
        for row in range(SIZE):
            for col in range(SIZE):
                if self._board[row, col] in WHITES:
                    n += 1

        return n

    def _init_board(self) -> np.ndarray:
        """Method which returns intial state of the board

        Returns:
            np.ndarray: initial board
        """
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

    def square_is_empty(self, row: int, col: int) -> bool:
        """Function to check if a square is empty

        Args:
            state (np.ndarray): board state
            row (int): row to check
            col (int): column to check

        Returns:
            bool: True if empty False otherwise
        """
        if self._board[row, col] == 0:
            return True
        else:
            return False

    def get_all_valid_moves(self) -> Dict[str, List[Tuple[Tuple, Tuple]]]:
        """Returns dict of all available moves on the board
        "takes": List of take moves
        "simple": List of simple moves

        Returns:
            Dict: List[Tup[Tup, Tup]] -> (piece_to_select, piece_to_move)
        """
        moves = {"simple": [], "takes": []}

        if self._last_piece_moved is not None:
            moves["simple"] += []
            moves["takes"] += self._get_valid_take_moves(*self._last_piece_moved)
            if len(moves["takes"]) > 0:
                return moves
        for row in range(SIZE):
            for col in range(SIZE):
                piece = self._board[row, col]
                if piece in WHITES and self._player == WHITE:
                    moves["simple"] += self._get_valid_simple_moves(row, col)
                    moves["takes"] += self._get_valid_take_moves(row, col)
                elif piece in BLACKS and self._player == BLACK:
                    moves["simple"] += self._get_valid_simple_moves(row, col)
                    moves["takes"] += self._get_valid_take_moves(row, col)

        return moves

    def _get_valid_simple_moves(self, row: int, col: int) -> List:
        """Gets all valid simple moves available for a given square

        Args:
            row (int): row the square is on
            col (int): column the square is on

        Returns:
            List: tuple of tuples
        """
        piece = self._board[row, col]
        valid_moves = []
        if self._player == BLACK:
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
        elif self._player == WHITE:
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
        """Gets all valid take moves available for a given square

        Args:
            row (int): row the square is on
            col (int): column the square is on

        Returns:
            List: tuple of tuples
        """
        piece = self._board[row, col]
        valid_moves = []
        if self._player == BLACK:
            if piece == 2:
                for dir in LEGAL_DIRS[BLACK]["king"]:
                    if (
                        row + 2 * dir[0] in range(8)
                        and col + 2 * dir[1] in range(8)
                        and self._board[row + dir[0], col + dir[1]] in WHITES
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
                        and self._board[row + dir[0], col + dir[1]] in WHITES
                        and self.square_is_empty(row + 2 * dir[0], col + 2 * dir[1])
                    ):
                        valid_moves.append(
                            ((row, col), (row + 2 * dir[0], col + 2 * dir[1]))
                        )
        elif self._player == WHITE:
            if piece == 4:
                for dir in LEGAL_DIRS[WHITE]["king"]:
                    if (
                        row + 2 * dir[0] in range(8)
                        and col + 2 * dir[1] in range(8)
                        and self._board[row + dir[0], col + dir[1]] in BLACKS
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
                        and self._board[row + dir[0], col + dir[1]] in BLACKS
                        and self.square_is_empty(row + 2 * dir[0], col + 2 * dir[1])
                    ):
                        valid_moves.append(
                            ((row, col), (row + 2 * dir[0], col + 2 * dir[1]))
                        )

        return valid_moves

    def render(self) -> None:
        """Renders the board"""
        clear_window()
        cols = ["X", "A", "B", "C", "D", "E", "F", "G", "H"]
        print(str.join(" | ", cols))
        for row in range(SIZE):
            print("----------------------------------")
            print(
                str(8 - row),
                "|",
                str.join(" | ", [NUM_TO_STR[int(x)] for x in self._board[row, :]]),
            )
        print("----------------------------------")
        print("TURN: ", self._player)
        print("MOVES NO CAPTURE: ", self._moves_no_capture)

    @staticmethod
    def convert_rowcol_to_user(row: int, col: int) -> Tuple[int, str]:
        """Converts a row column tuple to the way a user sees the board

        Args:
            row (int):
            col (int):

        Returns:
            Tuple[int, str]:
        """
        row = 8 - row
        return row, NUMS_TO_COLS[col]

    @staticmethod
    def convert_rowcol_to_game(row: int, col: str) -> Tuple[int, int]:
        """Converts a row column tuple to the way the game understands
        from what user inputs

        Args:
            row (int):
            col (int):

        Returns:
            Tuple[int, str]:
        """
        row = 8 - row
        return row, COLS_TO_NUMS[col]

    def clear(self, row: int, col: int) -> None:
        """Clears a square

        Args:
            row (int): row square is located
            col (int): column square is located
        """
        self._board[row, col] = 0

    def check_winner(self) -> bool:
        """Checks for a winner

        Returns:
            bool: if game is over
        """
        if self._player == BLACK and self.n_white_pieces == 0:
            return True
        elif self._player == WHITE and self.n_black_pieces == 0:
            return True
        else:
            return False

    def crown(self, row: int, col: int) -> None:
        piece = self._board[row, col]
        if piece == 1:
            self._board[row, col] = 2
        elif piece == 3:
            self._board[row, col] = 4

    def step(
        self, action: Tuple, verbose: int = 0
    ) -> Tuple[bool, np.ndarray, bool, float, Dict]:
        """
        Return Arg is (valid_move, next_obs, done, reward, info)
        """
        # TODO: ADD IN CROWNING
        info = {}
        piece_to_move, place_to_move_to = action[0], action[1]
        all_valid_moves = self.get_all_valid_moves()

        if len(all_valid_moves["takes"]) == 0 and len(all_valid_moves["simple"]) == 0:
            if verbose:
                print(f"{self.opposite_player} HAS WON")
            return (True, self._board, True, -1, info)

        row, col = piece_to_move[0], piece_to_move[1]
        new_row, new_col = place_to_move_to[0], place_to_move_to[1]

        valid_simples, valid_takes = (
            all_valid_moves["simple"],
            all_valid_moves["takes"],
        )

        valid_selections = (
            [x[0] for x in valid_takes]
            if len(valid_takes) > 0
            else [x[0] for x in valid_simples]
        )

        valid_moves = (
            [x[1] for x in valid_takes]
            if len(valid_takes) > 0
            else [x[1] for x in valid_simples if x[0] == (row, col)]
        )

        info["fail_cause"] = "invalid move"

        if ((row, col) not in valid_selections) or (
            (new_row, new_col) not in valid_moves
        ):
            return (False, self._board, False, 0, info)
        self._board[new_row, new_col] = self._board[row, col]
        self.clear(row, col)
        self._moves_no_capture += 1

        if abs(new_row - row) == 2:
            one_row = 0.5 * (new_row - row)
            one_col = 0.5 * (new_col - col)
            self.clear(int(row + one_row), int(col + one_col))
            self._moves_no_capture = 0
            self._last_piece_moved = (new_row, new_col)
        else:
            self._last_piece_moved = None

        if self._board[new_row, new_col] in WHITES and new_row == 0:
            self.crown(new_row, new_col)
        if self._board[new_row, new_col] in BLACKS and new_row == 7:
            self.crown(new_row, new_col)

        if self._last_piece_moved is not None:
            if len(self._get_valid_take_moves(*self._last_piece_moved)) <= 0:
                self._player = self.opposite_player
                self._last_piece_moved = None
        else:
            self._player = self.opposite_player

        if self._moves_no_capture == 40:
            if verbose:
                print("DRAW - 40 MOVES WITH NO CAPTURE")
            return (True, self._board, True, 0, info)
        elif self.n_black_pieces == 1 and self.n_white_pieces == 1:
            if verbose:
                print("DRAW")
            return (True, self._board, True, 0, info)
        elif self.check_winner():
            if verbose:
                print(f"{self._player} HAS WON")
            return (True, self._board, True, 1, info)

        return (True, self._board, False, 0, info)

    @property
    def board(self) -> np.ndarray:
        """Current state

        Returns:
            np.ndarray: current board state
        """
        return self._board
