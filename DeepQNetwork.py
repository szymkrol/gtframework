from abc import ABC, abstractmethod

import torch
import torch.nn as nn
import torch.optim as optim

from collections import deque, namedtuple

import math
import random
from typing import Any

from Engine import Engine
from Game import Game
from Board import Board
from Player import Player

Experience = namedtuple('Experience',
                        ('state', 'action', 'next_state', 'reward', 'done'))


class ReplayMemory:
    """Prosta implementacja bufora pamięci powtórek."""

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Zapisuje przejście."""
        self.memory.append(Experience(*args))

    def sample(self, batch_size):
        """Pobiera losową próbkę przejść."""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQNEngine(Engine, ABC):
    def __init__(self, Q_Network,
                 state_dim, action_dim, all_actions,
                 memory_capacity=10000, batch_size=128,
                 gamma=0.99, lr=1e-4,
                 epsilon_start=0.9, epsilon_end=0.05, epsilon_decay=1000,
                 target_update_freq=10):
        self.all_actions = all_actions  # Defined externally
        self.action_to_index = {a: i for i, a in enumerate(self.all_actions)}
        self.index_to_action = {i: a for i, a in enumerate(self.all_actions)}
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.memory = ReplayMemory(memory_capacity)
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.target_update_freq = target_update_freq

        self.policy_net = Q_Network(state_dim, action_dim)
        self.target_net = Q_Network(state_dim, action_dim)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=lr, amsgrad=True)
        self.steps_done = 0

    def run(self, game: Game) -> bool:
        init_epsilon = self.epsilon
        self.epsilon = 0
        game.move(self.choose_action(self.get_tensor_repr(game.get_state_repr()), game.get_available_moves()))
        self.epsilon = init_epsilon

    def choose_action(self, state_tensor, available_moves):
        # Epsilon decay
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * \
                       math.exp(-1. * self.steps_done / self.epsilon_decay)
        self.steps_done += 1

        if random.random() < self.epsilon:
            return random.choice(available_moves)

        with torch.no_grad():
            q_values = self.policy_net(state_tensor)  # shape [1, num_total_actions]

            # Mask out illegal actions
            valid_indices = [self.action_to_index[a] for a in available_moves]
            mask = torch.full_like(q_values, float('-inf'))
            mask[0, valid_indices] = 0  # Only valid indices are unmasked

            masked_q = q_values + mask
            action_index = masked_q.argmax(1).item()
            return self.index_to_action[action_index]

    def remember(self, state_tensor, action, next_state_tensor, reward, done):
        action_index = self.action_to_index[action]
        self.memory.push(
            state_tensor,
            torch.tensor([[action_index]], dtype=torch.long),
            next_state_tensor,
            torch.tensor([reward], dtype=torch.float32),
            torch.tensor([done], dtype=torch.bool)
        )

    def learn(self):
        if len(self.memory) < self.batch_size:
            return
        experiences = self.memory.sample(self.batch_size)
        batch = Experience(*zip(*experiences))
        # Utwórz tensory dla stanów niekońcowych
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Oblicz Q(s_t, a) - sieć policy_net oblicza Q dla stanu, a my wybieramy kolumnę odpowiadającą akcji
        # state_action_values[i] to Q(state_batch[i], action_batch[i])
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Oblicz V(s_{t+1}) dla wszystkich następnych stanów.
        # Oczekiwana wartość akcji jest obliczana na podstawie target_net.
        # Wybieramy najlepszą wartość za pomocą max(1)[0].
        next_state_values = torch.zeros(self.batch_size)
        with torch.no_grad():  # Nie liczymy gradientów dla sieci celu
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0]

        # Oblicz oczekiwaną wartość Q (target)
        # expected_state_action_values[i] = reward_batch[i] + gamma * V(s_{t+1}) dla i-tej próbki
        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        # Oblicz stratę Huber'a (jest mniej wrażliwa na outliery niż MSE)
        criterion = nn.SmoothL1Loss()  # lub nn.MSELoss()
        loss = criterion(state_action_values,
                         expected_state_action_values.unsqueeze(1))  # Target musi mieć ten sam kształt co output

        # Optymalizuj model
        self.optimizer.zero_grad()
        loss.backward()
        # Ograniczenie gradientu (opcjonalnie, ale często pomaga)
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()

    def update_target_net(self):
        # Kopiuj wagi z policy_net do target_net
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def save_model(self, filename="dqn_policy_net.pth"):
        torch.save(self.policy_net.state_dict(), filename)
        print(f"Model sieci Q zapisany do {filename}")

    def load_model(self, filename="dqn_policy_net.pth"):
        try:
            self.policy_net.load_state_dict(torch.load(filename))
            self.target_net.load_state_dict(self.policy_net.state_dict())  # Zsynchronizuj sieć celu
            self.policy_net.eval()  # Ustaw w tryb ewaluacji po wczytaniu
            self.target_net.eval()
            print(f"Model sieci Q wczytany z {filename}")
        except FileNotFoundError:
            print(f"Nie znaleziono pliku {filename}. Inicjalizuję nową sieć.")

    def train_dqn_agent(self, opponent: Engine,
                        GameClass: type[Game], game_config: dict[str: Any],
                        BoardClass: type[Board], board_config: dict[str: Any],
                        player: Player = None,
                        num_episodes=10000, print_every=500):
        wins = 0
        losses = 0
        draws = 0
        total_steps = 0

        for episode in range(num_episodes):
            board = BoardClass(**board_config)
            game = GameClass(board, **game_config)
            state_tensor = self.get_tensor_repr(game.get_state_repr())
            first_player = game.get_current_player()
            done = False

            while not done:
                total_steps += 1
                current_player = game.get_current_player()
                available_moves = game.get_available_moves()

                if current_player == first_player:
                    # Ruch agenta DQN
                    action = self.choose_action(state_tensor, available_moves)
                    if action is None:
                        break

                    game.move(action)
                    next_state_tensor = self.get_tensor_repr(game.get_state_repr())
                    done, winner = game.is_finished()

                    # Określ nagrodę
                    reward = 0
                    if done:
                        if winner == first_player:
                            reward = 1  # Win
                        elif winner is None:
                            reward = 0.5  # Draw
                        else:  # Remis
                            reward = -1  # Lose

                    # Zapisz doświadczenie w pamięci
                    # Nawet jeśli done=True, next_state_tuple jest potrzebny, ale będzie None w Experience
                    self.remember(state_tensor, action,
                                  next_state_tensor if not done else None,
                                  reward, done)

                    # Przejdź do następnego stanu
                    state_tensor = next_state_tensor

                    # Ucz się na podstawie próbki z pamięci
                    self.learn()

                else:  # Ruch przeciwnika
                    done, winner = game.is_finished()
                    if not done:  # Remis przed ruchem przeciwnika
                        opponent.run(game)
                        done, winner = game.is_finished()
                        state_tensor = self.get_tensor_repr(game.get_state_repr())

                if done:
                    if winner == first_player:
                        wins += 1
                    elif winner is None:
                        draws += 1
                    else:
                        losses += 1

            # Aktualizuj sieć celu co pewną liczbę epizodów
            if episode % self.target_update_freq == 0:
                self.update_target_net()
                # print(f"Epizod {episode}: Zaktualizowano sieć celu.")

            if (episode + 1) % print_every == 0:
                print(f"Epizod: {episode + 1}/{num_episodes}")
                print(f"  Wygrane: {wins}, Przegrane: {losses}, Remisy: {draws}")
                print(f"  Procent wygranych (od ost. raportu): {100 * wins / print_every:.2f}%")
                print(f"  Aktualny epsilon: {self.epsilon:.4f}")
                print(f"  Rozmiar pamięci: {len(self.memory)}")
                # Resetuj liczniki dla raportu
                wins, losses, draws = 0, 0, 0

        print("\nTrening DQN zakończony.")
        # Zapisz model po treningu
        self.save_model(f"dqn_policy_net.pth")

    @abstractmethod
    def get_tensor_repr(self, state_repr):
        pass
