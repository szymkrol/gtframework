from Engines.DeepQNetwork import DQNEngine
from Body.Player import Player
from Games.Connect4 import Conn4Board
from Body.Game import Game
from Engines.RandEng import RandEng

import torch
import torch.nn.functional as F
import torch.nn as nn

DQN_GAMMA = 0.99
DQN_LR = 5e-4  # Trochę wyższy learning rate
DQN_EPS_START = 0.95
DQN_EPS_END = 0.01
DQN_EPS_DECAY = 10000  # Wolniejszy spadek epsilonu
DQN_BATCH_SIZE = 256
DQN_MEMORY_CAPACITY = 100000
DQN_TARGET_UPDATE = 20  # Aktualizacja sieci celu co 20 epizodów

DQN_NUM_EPISODES = 15000  # Mniejsza liczba epizodów ze względu na czas
DQN_PRINT_EVERY = 500


# class MyQNetwork(nn.Module):
#     def __init__(self, n_observations=9, n_actions=9):
#         super(MyQNetwork, self).__init__()
#         # Wejście: 9 pól planszy
#         # Wyjście: 9 wartości Q (po jednej dla każdego możliwego ruchu/pola)
#         self.layer1 = nn.Linear(n_observations, 64)  # Mała warstwa ukryta
#         self.layer2 = nn.Linear(64, 64)
#         self.layer3 = nn.Linear(64, n_actions)
#
#     def forward(self, x):
#         x = F.relu(self.layer1(x))
#         x = F.relu(self.layer2(x))
#         return self.layer3(x)  # Zwraca wartości Q dla każdej akcji (pola 0-8)
#
#
# config = {
#     "first_player": Player(1, 'x'),
#     "second_player": Player(2, 'o'),
# }
#
# my_board = TicBoard(**config)
# my_game = Game(my_board)
#

#
# # Inicjalizacja agenta DQN
# agent_dqn_x = DQNEngine(Q_Network=MyQNetwork,
#                         state_dim=9, action_dim=9, all_actions=Game(TicBoard(**config)).get_available_moves(),
#                         gamma=DQN_GAMMA, lr=DQN_LR,
#                         epsilon_start=DQN_EPS_START, epsilon_end=DQN_EPS_END, epsilon_decay=DQN_EPS_DECAY,
#                         batch_size=DQN_BATCH_SIZE, memory_capacity=DQN_MEMORY_CAPACITY,
#                         target_update_freq=DQN_TARGET_UPDATE)
#
# # Opcjonalnie: Wczytaj wcześniej zapisany model
# # agent_dqn_x.load_model("dqn_policy_net_X.pth")
#
# print("Rozpoczynanie treningu agenta DQN...")
# agent_dqn_x.train_dqn_agent(RandEng(), GameClass=Game, game_config={}, BoardClass=TicBoard, board_config=config, num_episodes=DQN_NUM_EPISODES, print_every=DQN_PRINT_EVERY)


class MyQNetwork(nn.Module):
    def __init__(self, n_observations=42, n_actions=7):
        super(MyQNetwork, self).__init__()
        self.layer1 = nn.Linear(n_observations, 64)
        self.layer2 = nn.Linear(64, 64)
        self.layer3 = nn.Linear(64, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)


config = {
    "first_player": Player(1, 'x'),
    "second_player": Player(2, 'o'),
}

class Conn4DQN(DQNEngine):
    def get_tensor_repr(self, state_repr):
        mapping = {'x': 1.0,
                   ' ': 0.0,
                   'o': -1.0}
        numeric_board = [mapping[cell] for cell in state_repr]
        return torch.tensor(numeric_board, dtype=torch.float32).unsqueeze(0)

my_board = Conn4Board(**config)
my_game = Game(my_board)

agent_dqn_x = Conn4DQN(Q_Network=MyQNetwork,
                        state_dim=42, action_dim=7, all_actions=[0, 1, 2, 3, 4, 5, 6],
                        gamma=DQN_GAMMA, lr=DQN_LR,
                        epsilon_start=DQN_EPS_START, epsilon_end=DQN_EPS_END, epsilon_decay=DQN_EPS_DECAY,
                        batch_size=DQN_BATCH_SIZE, memory_capacity=DQN_MEMORY_CAPACITY,
                        target_update_freq=DQN_TARGET_UPDATE)

# agent_dqn_1 = Conn4DQN(Q_Network=MyQNetwork,
#                         state_dim=42, action_dim=7, all_actions=[0, 1, 2, 3, 4, 5, 6],
#                         gamma=DQN_GAMMA, lr=DQN_LR,
#                         epsilon_start=DQN_EPS_START, epsilon_end=DQN_EPS_END, epsilon_decay=DQN_EPS_DECAY,
#                         batch_size=DQN_BATCH_SIZE, memory_capacity=DQN_MEMORY_CAPACITY,
#                         target_update_freq=DQN_TARGET_UPDATE)

# agent_dqn_1.load_model("dqn_policy_net.pth")
#
# # Opcjonalnie: Wczytaj wcześniej zapisany model
# agent_dqn_x.load_model("dqn_policy_net_X.pth")
#
print("Rozpoczynanie treningu agenta DQN...")
agent_dqn_x.train_dqn_agent(RandEng(), GameClass=Game, game_config={}, BoardClass=Conn4Board, board_config=config, num_episodes=DQN_NUM_EPISODES, print_every=DQN_PRINT_EVERY)
# agent_dqn_x.load_model("dqn_policy_net.pth")

while not my_game.is_finished()[0]:
    agent_dqn_x.run(my_game)
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
