from typing import Any
import random
import time

from Engines.Engine import Engine
from Body.Game import Game
from Engines.GameTree import GameTree, TreeNode
from Body.Player import Player


class Mcts(Engine):
    """
    Class should make a move for the current player based on the MCTS method.
    """

    def __init__(self, iter_limit: int, time_limit: float, const: float = 1.41, remember_past: bool = True) -> None:
        """
        Engine constructor.
        :param iter_limit: maximum number of iterations spend on traversing tree.
        :param time_limit: maximum time (in seconds) spend on traversing tree.
        :param const: exploration parameter
        :param remember_past: whether the game has to remember past states to work properly
        """
        self._iter_limit = iter_limit
        self._time_limit = time_limit
        self._const = const
        self._remember_past = remember_past

    def run(self, game: Game) -> bool:
        move = self.mcts(game)
        return super().run(game, move)

    def mcts(self, game: Game) -> Any:
        """
        Function evaluates the game tree and returns best move for current player according to MCTS.
        :param game: game on which MCTS is to be done.
        :return: best move.
        """
        root = TreeNode(exploration_const=self._const)
        tree = GameTree(root, game)

        t_end = time.time() + self._time_limit
        for _ in range(self._iter_limit):
            if time.time() >= t_end:
                break
            self._single_mcts(tree)

        # Find best node
        children = root.get_children()
        if not children:
            return random.choice(game.get_available_moves())
        return max(children, key=lambda c: c.get_num_sims()).get_move_from_parent()

    def _play_to_end(self, game: Game) -> tuple[False, None] | tuple[True, Player]:
        """Function plays randomly until game finishes."""
        while not game.is_finished()[0]:
            game.move(random.choice(game.get_available_moves()))
        return game.is_finished()

    def _single_mcts(self, tree: GameTree) -> None:
        """Method performs single MCTS iteration."""
        current_node = tree.get_root()
        current_game = tree.get_root_game_copy(is_revertible=False, remember_past=self._remember_past)
        first_player = current_game.get_current_player()

        # Finding the most promising leaf
        while current_node.get_children():
            current_node = current_node.get_max_UCB_child()
            current_game.move(current_node.get_move_from_parent())

        # Expansion
        finished, winner = current_game.is_finished()
        if not finished:
            current_node.create_children(current_game.get_available_moves())
            current_node = random.choice(current_node.get_children())
            current_game.move(current_node.get_move_from_parent())
            finished, winner = self._play_to_end(current_game)

        # Backpropagation
        is_win = finished and winner == first_player
        while current_node:
            current_node.increment_num_sims()
            if is_win:
                current_node.increment_num_wins()
            current_node = current_node.get_parent()
