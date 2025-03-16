from abc import ABC, abstractmethod


class Engine:
    def minmax(self, board, depth, player, is_ab, eval_fun, game):
        pass

    def mcts(self, board, iter, time, player, game):
        pass


class Board(ABC):
    def __init__(self):
        self.current_state = []

    def current_state(self):
        pass

    @abstractmethod
    def return_available_moves(self):
        pass

class Player:
    def __init__(self, id):
        self.id = id
    pass


class Game(ABC):
    @abstractmethod
    def initalise(self):
        # tworzy planszę i zwraca Board
        pass
