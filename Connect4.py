from Player import Player
from Board import Board
from Game import Game
from Mcts import Mcts
from typing import Any
from Minmax import Minmax
from collections.abc import Hashable
from itertools import chain


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


class Connect_4_Minmax(Minmax):
    def three_in_a_row(self, game):
        board = game.get_board_state()

        # Horizontal wins
        for row in range(6):
            for column in range(5):
                for player in game.get_players():
                    if all(board[row][column + i] == player.get_attributes() for i in range(3)):
                        return True, player

        # Vertical wins
        for row in range(4):
            for column in range(7):
                for player in game.get_players():
                    if all(board[row + i][column] == player.get_attributes() for i in range(3)):
                        return True, player

        # Bottom-left to top-right wins
        for row in range(2, 6):
            for column in range(5):
                for player in game.get_players():
                    if all(board[row - i][column + i] == player.get_attributes() for i in range(3)):
                        return True, player

        # Top-left to bottom-right
        for row in range(4):
            for column in range(5):
                for player in game.get_players():
                    if all(board[row + i][column + i] == player.get_attributes() for i in range(3)):
                        return True, player

        return False, None

    def evaluate(self, game):
        if game.is_finished()[1] == self.player:
            return 100
        elif not game.is_finished()[1] is None:
            return -50
        elif self.three_in_a_row(game)[1] == self.player:
            return 20
        elif not self.three_in_a_row(game)[1] is None:
            return -10
        else:
            return 0


my_board = Conn4Board(Player(1, 'x'), Player(2, 'o'))
my_game = Game(my_board)
my_engine = Mcts(2000, 20)
my_engine_v2 = Connect_4_Minmax(depth=5, prun=True, player=my_game.get_current_player())

while not my_game.is_finished()[0]:
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    board = my_game.get_board_state()
    for x in board:
        print(x)
    i = int(input())
    my_game.move(i)
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    board = my_game.get_board_state()
    for x in board:
        print(x)
    #  my_engine.run(my_game)
    my_engine_v2.run(my_game)
