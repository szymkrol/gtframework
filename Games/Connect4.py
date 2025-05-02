from typing import Any
from collections.abc import Hashable
from itertools import chain

from Body.Player import Player
from Body.Board import Board


class Conn4Board(Board):
    def change_board(self, move: Any) -> None:
        i = 0
        while True:
            if self._current_state["board_state"][i][move] == ' ' and (i > 4 or self._current_state["board_state"][i+1][move] != ' '):
                self._current_state["board_state"][i][move] = self.get_player_to_move().get_attributes()
                self._alternate_player()
                break
            i += 1

    def get_available_moves(self) -> list[int]:
        return [i for i in range(7) if self._current_state["board_state"][0][i] == ' ']

    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        board = self._current_state["board_state"]

        # Horizontal wins
        for row in range(6):
            for column in range(4):
                for player in self._players:
                    if all(board[row][column + i] == player.get_attributes() for i in range(4)):
                        return True, player

        # Vertical wins
        for row in range(3):
            for column in range(7):
                for player in self._players:
                    if all(board[row + i][column] == player.get_attributes() for i in range(4)):
                        return True, player

        # Bottom-left to top-right wins
        for row in range(3, 6):
            for column in range(4):
                for player in self._players:
                    if all(board[row - i][column + i] == player.get_attributes() for i in range(4)):
                        return True, player

        # Top-left to bottom-right
        for row in range(3):
            for column in range(4):
                for player in self._players:
                    if all(board[row + i][column + i] == player.get_attributes() for i in range(4)):
                        return True, player

        return False, None

    def generate_empty_board(self) -> list[list[str]]:
        board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '].copy() for _ in range(6)]
        return board

    def get_state_repr(self) -> Hashable:
        return tuple(chain(*self._current_state["board_state"]))
