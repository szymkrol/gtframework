from Player import Player
from Board import Board
from Game import Game
from Engine import Engine
from Mcts import Mcts
from Minmax import Minmax
from copy import deepcopy


class TicBoard(Board):
    def generate_empty_board(self):
        return [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

    def get_available_moves(self):
        available_moves = []
        for i, row in enumerate(self.get_current_state()["board_state"]):
            for j, cell in enumerate(row):
                if cell == '_':
                    available_moves.append((i, j))
        return available_moves

    def change_board(self, move):
        i, j = move
        player = self.get_current_state()["player_to_move"]
        if player == self.get_players()[0]:
            self.get_current_state()["player_to_move"] = self.get_players()[1]
        else:
            self.get_current_state()["player_to_move"] = self.get_players()[0]
        self.get_current_state()["board_state"][i][j] = player.get_attributes()

    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        board = self.get_current_state()["board_state"]
        is_finished = False
        symbol = None
        # Check rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "_":
                is_finished, symbol = True, board[i][0]
        # Check columns
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "_":
                is_finished, symbol = True, board[0][i]
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "_":
            is_finished, symbol = True, board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "_":
            is_finished, symbol = True, board[0][2]
        # No winner yet
        if is_finished:
            for player in self.get_players():
                if player.get_attributes() == symbol:
                    return True, player
        else:
            return False, None
"""
class Minmax_v2(Minmax):
    def evaluate(self,game):

        if game.is_finished()[1] is None:
            return 0
        elif game.is_finished()[1] == self.player:
            return 1
        else:
            return -1
"""

player1 = Player(1,'X')
player2 = Player(2,'O')
depth = 10
prun = True
my_board = TicBoard(player1, player2)
my_game = Game(my_board)
my_engine = Minmax(depth,prun,player2)
while not my_game.is_finished()[0]:
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    board = my_game.get_board_state()
    for x in board:
        print(x)
    i = int(input())
    j = int(input())
    my_game.move((i, j))
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    board = my_game.get_board_state()
    for x in board:
        print(x)
    my_engine.run(my_game)

# while not my_game.is_finished()[0]:
#     print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
#     board = my_game.get_board_state()
#     for x in board:
#         print(x)
#     i = int(input())
#     j = int(input())
#     my_game.move((i, j))


# print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
# board = my_game.get_board_state()
# for x in board:
#     print(x)
# i = int(input())
# j = int(input())
# my_game.move((i, j))
# print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
# board = my_game.get_board_state()
# for x in board:
#     print(x)
# my_game.revert()
# print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
# board = my_game.get_board_state()
# for x in board:
#     print(x)
