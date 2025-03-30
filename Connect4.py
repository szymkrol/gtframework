from Player import Player
from Board import Board
from Game import Game
from Mcts import Mcts


class Conn4Board(Board):
    def change_board(self, move):
        i = 0
        while True:
            if self._current_state["board_state"][i][move] == ' ' and (i > 4 or self._current_state["board_state"][i+1][move] != ' '):
                self._current_state["board_state"][i][move] = self.get_player_to_move().get_attributes()
                self._alternate_player()
                break
            i += 1

    def get_available_moves(self):
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

    def generate_empty_board(self):
        board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '].copy() for _ in range(6)]
        return board

my_board = Conn4Board(Player(1, 'x'), Player(2, 'o'))
my_game = Game(my_board)
my_engine = Mcts(500, 10)

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
    my_engine.run(my_game)
