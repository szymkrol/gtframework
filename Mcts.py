from Engine import Engine
from Game import Game
from GameTree import GameTree, TreeNode
from typing import Any, Tuple
import random
import time

from Player import Player


class Mcts(Engine):
    """
    Class should make a move for the current player based on the MCTS method.
    """

    def __init__(self, iter_limit: int, time_limit: float, const=1.41) -> None:
        """
        Engine constructor
        :param iter_limit: maximum number of iterations spend on traversing tree.
        :param time_limit: maximum time (in seconds) spend on traversing tree.
        :param const: exploration parameter
        """
        self._iter_limit = iter_limit
        self._time_limit = time_limit
        self._const = const

    def run(self, game: Game) -> bool:
        move = self.mcts(game)
        print(move)
        return Engine.run(self, game, move)

    def mcts(self, game: Game) -> Any:
        """
        Function evaluates the game tree and returns best move for current player according to MCTS
        :param game:
        :return: Best move
        """
        tree = GameTree(TreeNode(exploration_const=self._const), game)
        i = 0
        t_end = time.time() + self._time_limit

        # Doing MCTS within constraints
        while i < self._iter_limit and time.time() < t_end:
            self._single_mcts(tree)
            i += 1

        # Find best node
        children = tree.get_root().get_children()
        children.sort(key=lambda node: node.get_num_sims(), reverse=True)
        best_node = children[0]
        return best_node.get_move_from_parent()

    def _play_to_end(self, game: Game) -> tuple[False, None] | tuple[True, Player]:
        """Function plays randomly until game finishes."""
        while not game.is_finished()[0]:
            available_moves = game.get_available_moves()
            game.move(random.choice(available_moves))
        return game.is_finished()

    def _single_mcts(self, tree: GameTree) -> None:
        """Method performs single MCTS iteration."""
        current_node = tree.get_root()
        current_game = tree.get_root_game_copy()
        first_player = current_game.get_current_player()

        # Finding the most promising leaf
        while current_node.get_children():
            current_node = current_node.get_max_UCB_child()
            current_game.move(current_node.get_move_from_parent())

        if not current_game.is_finished()[0]:
            # Game has not finished yet
            current_node.create_children(current_game.get_available_moves())
            best_node = current_node.get_max_UCB_child()
            current_game.move(best_node.get_move_from_parent())
            result = self._play_to_end(current_game)
            best_node.increment_num_sims()
            is_win = False
            if result[0]:
                if result[1] == first_player:
                    best_node.increment_num_wins()
                    is_win = True

        else:
            # Game has already finished
            result = current_game.is_finished()
            is_win = False
            if result[0]:
                if result[1] == first_player:
                    is_win = True

        # Backpropagation
        while current_node.get_parent() is not None:
            current_node.increment_num_sims()
            if is_win:
                current_node.increment_num_wins()
            current_node = current_node.get_parent()
        # Root update
        current_node.increment_num_sims()
        if is_win:
            current_node.increment_num_wins()
