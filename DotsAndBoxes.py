from Player import Player
from Board import Board
from Game import Game
from Engine import Engine
from Mcts import Mcts
from Lattice import LatticeNode, Lattice, get_neigh_coords


class DotsAndBoxes(Board):

    def __init__(self, first_player: Player, second_player: Player, size: int):
        super().__init__(first_player, second_player)
        self._size = size
        self._score = 0

    def generate_empty_board(self):
        return Lattice(self._size + 1)

    def change_board(self, move):
        node_a = self.get_current_state()["board_state"].get_field(move[0])
        node_b = self.get_current_state()["board_state"].get_field(move[1])
        node_a.remove_connection(node_b)
        score_change = 0
        for node in [node_a, node_b]:
            if node.is_isolated():
                if self.get_current_state()["current_player"].get_attribute():
                    score_change += 1
                else:
                    score_change -= 1
        if score_change == 0:
            self._alternate_player()

    def get_available_moves(self):
        available_moves = []
        for i in range(0, self._size + 1):
            for j in range(0, self._size + 1):
                if i == 0 and j == 0:
                    continue
                nodes = self.get_current_state()["board_state"].get_lower_right_connections((i, j))
                for node in nodes:
                    available_moves.append(((i, j), node.get_coords()))
        return available_moves

    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        if len(self.get_available_moves()) == 0:
            if self._score == 0:
                return False, None
            elif self._score > 0:
                players = self.get_players()
                if players[0].get_attributes():
                    winner = players[0]
                else:
                    winner = players[1]
            else:
                players = self.get_players()
                if players[0].get_attributes():
                    winner = players[1]
                else:
                    winner = players[0]
