from collections.abc import Hashable
from typing import Any

from Body.Player import Player
from Body.Board import Board
from Games.Lattice import Lattice


class DotsAndBoxes(Board):

    def __init__(self, first_player: Player, second_player: Player, attributes: int, turn_part: int = 0, score: int = 0,
                 is_revertible: bool = True, remember_past: bool = True) -> None:
        self._size = attributes
        super().__init__(first_player, second_player, attributes=attributes, turn_part=turn_part, state_attr=score,
                         is_revertible=is_revertible, remember_past=remember_past)

    def generate_empty_board(self) -> Lattice:
        return Lattice(self._size + 1)

    def change_board(self, move: Any) -> None:
        node_a = self.get_current_state()["board_state"].get_field(move[0])
        node_b = self.get_current_state()["board_state"].get_field(move[1])
        node_a.remove_connection(node_b)
        score_change = 0
        for node in [node_a, node_b]:
            if node.is_closed() and node.get_attribute() == '_':
                node.set_attribute('x')
                if self.get_current_state()["player_to_move"] == self._players[0]:
                    score_change += 1
                else:
                    score_change -= 1
        if score_change == 0:
            self._alternate_player()
        self.set_state_attr(self.get_state_attr() + score_change)

    def get_available_moves(self) -> list[Any]:
        available_moves = []
        for i in range(0, self._size + 1):
            for j in range(0, self._size + 1):
                if (i == 0 or i == self._size) and (j == 0 or j == self._size):
                    continue
                nodes = self.get_current_state()["board_state"].get_lower_right_connections((i, j))
                for node in nodes:
                    available_moves.append(((i, j), node.get_coords()))
        return available_moves

    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        if len(self.get_available_moves()) == 0:
            if self.get_state_attr() == 0:
                return False, None
            players = self.get_players()
            if self.get_state_attr() > 0:
                if players[0].get_attributes():
                    winner = players[0]
                else:
                    winner = players[1]
            else:
                if players[0].get_attributes():
                    winner = players[1]
                else:
                    winner = players[0]
            return True, winner
        else:
            return False, None

    def get_state_repr(self) -> Hashable:
        return self.get_current_state()["board_state"].get_state_repr()

    def get_score(self) -> int:
        return self.get_state_attr()

    def __str__(self) -> str:
        return self.get_current_state()["board_state"].__str__() + str(self.get_state_attr())
