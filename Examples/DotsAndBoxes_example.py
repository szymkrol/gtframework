from Games.DotsAndBoxes import DotsAndBoxes
from Engines.Minmax import Minmax
from Engines.Mcts import Mcts
from Engines.RandEng import RandEng
from Body.Game import Game
from Body.Player import Player

class DotMax(Minmax):
    def evaluate(self, game: Game) -> int:
        return -game.get_board().get_score()


player1 = Player(1, "MCTS")
player2 = Player(2, "MINIMAX")
my_board = DotsAndBoxes(player1, player2, 5)
my_game = Game(my_board)
my_mcts = Mcts(1000, 10, remember_past=False, const=2.5)
my_minimax = DotMax(3, True, player2)
my_randEng = RandEng()

while not my_game.is_finished()[0]:
    print(my_game)
    if my_game.get_current_player() == player1:
        print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")

        # i = int(input())
        # j = int(input())
        # x = (i, j)
        #
        # i = int(input())
        # j = int(input())
        # my_game.move((x, (i, j)))
        my_mcts.run(my_game)
    else:
        print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
        my_minimax.run(my_game)
