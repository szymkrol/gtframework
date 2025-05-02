from Body.Player import Player
from Body.Game import Game
from Engines.Minmax import Minmax
from Games.TicTacToe import TicBoard


class Minmax_v2(Minmax):
    def evaluate(self, game):
        if game.is_finished()[1] is None:
            return 0
        elif game.is_finished()[1] == self.player:
            return 100
        else:
            return -50


player1 = Player(1, 'X')
player2 = Player(2, 'O')
depth = 10
prun = True
my_board = TicBoard(player1, player2)
my_game = Game(my_board)
my_engine = Minmax_v2(depth, prun, player2)
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
print(f"Winner is: {my_game.is_finished()[1].get_attributes()}")

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
