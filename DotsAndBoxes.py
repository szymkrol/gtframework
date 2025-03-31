from Player import Player
from Board import Board
from Game import Game
from Engine import Engine
from Mcts import Mcts


class DotsAndBoxes(Board):

    def __init__(self, first_player: Player, second_player: Player, size: int):
        super().__init__(first_player, second_player)
        self._size = size

    def generate_empty_board(self):
        pass

    def change_board(self, move):
        pass

    def get_available_moves(self):
        pass

    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        pass
