from abc import ABC, abstractmethod
from copy import deepcopy


class Engine:
    def minmax(self, depth, is_ab, eval_fun, game):
        pass

    def mcts(self, iterations, time, game):
        pass

    def run(self, game):
        pass
