from Body.Player import Player
from Body.Game import Game
from Engines.Mcts import Mcts
from Games.TicTacToe import TicBoard


my_board = TicBoard(Player(1, 'x'), Player(2, 'o'))
my_game = Game(my_board)
my_engine = Mcts(100000, 10)
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
