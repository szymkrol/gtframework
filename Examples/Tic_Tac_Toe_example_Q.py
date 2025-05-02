from Body.Player import Player
from Body.Game import Game
from Engines.Mcts import Mcts
from Engines.QLearning import QLearningEngine
from Engines.RandEng import RandEng
from Games.TicTacToe import TicBoard


config = {
    "first_player": Player(1, 'x'),
    "second_player": Player(2, 'o'),
}

my_board = TicBoard(**config)
my_game = Game(my_board)
my_engine = Mcts(500, 10)

ALPHA = 0.1  # Współczynnik uczenia
GAMMA = 0.9  # Współczynnik dyskontowania
EPSILON = 0.9  # Początkowa wartość epsilon (wysoka dla eksploracji na początku)
NUM_EPISODES = 100000  # Liczba gier treningowych
qlearner = QLearningEngine(alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON)
qlearner.train(RandEng(), NUM_EPISODES, Game, {}, TicBoard, config)

qlearner.save_q_table("kolko_krzyzyk_q_table_X.pkl")

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
