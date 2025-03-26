from Engine import Engine
from Game import Game


class Mcts(Engine):
    """
    Class should make a move for the current player based on the MCTS method.
    """

    def __init__(self, iter_limit, time_limit, const=1.41):
        """
        Engine constructor
        :param iter_limit: maximum number of iterations spend on traversing tree.
        :param time_limit: maximum time (in seconds) spend on traversing tree.
        :param const: exploration parameter
        """
        self.iter_limit = iter_limit
        self.time_limit = time_limit
        self.const = const

    def run(self, game: Game) -> bool:
        move = self.mcts(game)
        Engine.run(game, move)

    def mcts(self, game: Game):
        """
        Function evaluates the game tree and returns best move for current player according to MCTS
        :param game:
        :return: Best move
        """

        pass
