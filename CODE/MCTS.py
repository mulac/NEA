from ConsoleCheckers import CheckersBoard
from consts import *

import numpy as np
from tqdm import tqdm
from typing import Dict, List, Tuple, Iterator

from copy import deepcopy


class Node:
    def __init__(
        self,
        game: CheckersBoard,
        parent: "Node" = None,
        action_taken: Tuple = None,
        terminal: bool = None,
        reward: int = None,
        args: Dict = None,
    ):
        self._game = deepcopy(game)
        self._state = self._game.board
        self._parent = parent
        self.children: List[Node] = []
        self._action_taken = action_taken
        self._available_moves_left = self._init_available_moves()

        self._args = args

        self._visit_count, self._value_count = 0, 0

        self.is_terminal = terminal
        self.reward = reward
        self.colour = self._game.player

    def _init_available_moves(self):
        valid_moves = self._game.get_all_valid_moves()
        valid_takes, valid_simples = valid_moves["takes"], valid_moves["simple"]
        return valid_takes if len(valid_takes) > 0 else valid_simples

    @property
    def n_children(self):
        return len(self.children)

    @property
    def n_branches_available(self):
        return len(self._available_moves_left)

    @property
    def visit_count(self):
        return self._visit_count

    """def b_expand(self):
        for action in self._available_moves_left:
            self._available_moves_left.remove(action)
            child_game = deepcopy(self._game)
            valid, child_state, done, reward, info = child_game.step(action)

            child = Node(child_game, self, action, done, reward, self._args)
            self.children.append(child)"""

    def d_expand(self):
        idx = np.random.choice(len(self._available_moves_left))
        action = self._available_moves_left[idx]
        self._available_moves_left.remove(action)
        child_game = deepcopy(self._game)
        valid, child_state, done, reward, info = child_game.step(action)

        child = Node(child_game, self, action, done, reward, self._args)
        self.children.append(child)

        return child

    def select_child(self):
        best_child = None
        best_ucb = -np.inf
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child: "Node"):
        return (child._value_count / child._visit_count) + self._args["eec"] * (
            np.sqrt(np.log(self._visit_count) / child._visit_count)
        )

    def backprop(self, reward):
        self._visit_count += 1
        self._value_count += reward

        if self._parent is not None:
            if self._parent.colour != self.colour:
                reward *= -1
            self._parent.backprop(reward)

    def get_action_taken(self) -> Tuple[Tuple, Tuple]:
        return self._action_taken[0], self._action_taken[1]


class MCTS:

    def __init__(self, args: Dict = {"eec": 1.41, "n_searches": 5000}):
        """Creates new MCTS object

        Args:
            args (Dict, optional): hyperparms (Higher EEC -> more exploration). Defaults to {"eec": 10, "n_searches": 100}.
        """
        self._args = args
        self._root: Node = None

    def build_tree(self, root: CheckersBoard):
        """Constructs tree

        Args:
            root (CheckersBoard): Board to search from
        """
        self._root = Node(root, terminal=False, args=self._args)
        for search in tqdm(range(self._args["n_searches"])):
            node = self._root
            if node.n_branches_available == 0:
                node = node.select_child()

            if node is None:
                break
            while node.is_terminal is False and node.n_branches_available > 0:
                node = node.d_expand()

            node.backprop(node.reward * -1)

    def get_action_probs(self) -> np.ndarray:
        """Gets array of probabilities of action based on tree

        Returns:
            np.ndarray: Array of probabilities
        """
        p = np.zeros(
            (8, 8, 8)
        )  # (8x8) shows where to take piece from. Final 8 shows what direc e.g. idx 0 = row+1,col+1, idx 1 = row+1, col-1 etc.
        for child in self._root.children:
            piece_moved, moved_to = child.get_action_taken()
            row_change = moved_to[0] - piece_moved[0]
            col_change = moved_to[1] - piece_moved[1]
            direc_idx = ACTION_TO_IDX[(row_change, col_change)]
            p[piece_moved[0], piece_moved[1], direc_idx] = child._visit_count

        p /= np.sum(p)
        return p

    def convert_probs_to_action(self, p: np.ndarray) -> Tuple[Tuple, Tuple]:
        """Converts array of probabilites into action for game

        Args:
            p (np.ndarray): array of probs

        Returns:
            Tuple[Tuple, Tuple]: action (piece_to_move, move_to_where)
        """
        max_prob = np.max(p)
        idx = None
        for idx, val in np.ndenumerate(p):
            if val == max_prob:
                break
        row, col, idx = idx

        direc = IDX_TO_ACTION[idx]
        new_row, new_col = row + direc[0], col + direc[1]

        return ((row, col), (new_row, new_col))

    def get_action(self):
        p = self.get_action_probs()
        return self.convert_probs_to_action(p)


if __name__ == "__main__":
    import time

    n_games = 5
    games = np.empty(n_games, dtype=str)
    for gamen in range(n_games):

        mcts1 = MCTS(args={"eec": 1.41, "n_searches": 100000})
        mcts2 = MCTS(args={"eec": 1.41, "n_searches": 5})

        game = CheckersBoard()

        done = False
        while not done:
            game.render()
            print("GAME: ", gamen)

            if game._player == "white":
                valid = False
                while not valid:
                    print("Building Tree...")
                    mcts1.build_tree(game)
                    action = mcts1.get_action()
                    print(
                        f"WHITE'S MOVE:\n FROM:{CheckersBoard.convert_rowcol_to_user(*action[0])}\n TO:{CheckersBoard.convert_rowcol_to_user(*action[1])}"
                    )
                    valid, next_obs, done, reward, info = game.step(action, verbose=1)
                    if not valid:
                        print("TRIED TO MAKE INVALID MOVE")
                    if done and reward == 1:
                        games[gamen] = "white"
                    elif done and reward == 0:
                        games[gamen] = "draw"
            else:
                valid = False
                while not valid:
                    mcts2.build_tree(game)
                    action = mcts2.get_action()
                    print(
                        f"BLACK'S MOVE:\n FROM:{CheckersBoard.convert_rowcol_to_user(*action[0])}\n TO:{CheckersBoard.convert_rowcol_to_user(*action[1])}"
                    )
                    valid, next_obs, done, reward, info = game.step(action, verbose=1)
                    if not valid:
                        print("TRIED TO MAKE INVALID MOVE")
                    if done and reward == 1:
                        games[gamen] = "black"
                    elif done and reward == 0:
                        games[gamen] = "draw"

    print(games)
