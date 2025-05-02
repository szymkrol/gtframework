import random
import pickle
from typing import Any

from Engines.Engine import Engine
from Body.Game import Game
from Body.Board import Board
from Body.Player import Player


class QLearningEngine(Engine):
    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.1):
        self._q_table = {}
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon

    def get_q_value(self, state: Any, action: Any) -> float:
        return self._q_table.get(state, {}).get(action, .0)

    def choose_action(self, state, available_moves):
        if random.uniform(0, 1) < self._epsilon:
            action = random.choice(available_moves)
        else:
            q_values = {move: self.get_q_value(state, move) for move in available_moves}
            if not q_values:
                return None
            max_q = max(q_values.values())
            best_moves = [move for move, q in q_values.items() if q==max_q]
            action = random.choice(best_moves)
        return action

    def learn(self, state, action, reward, next_state, next_available_moves):
        if state not in self._q_table:
            self._q_table[state] = {}

        if not next_available_moves:
            max_next_q = 0.0
        else:
            next_q_values = [self.get_q_value(next_state, next_move) for next_move in next_available_moves]
            max_next_q = max(next_q_values) if next_q_values else 0.0

        current_q = self.get_q_value(state, action)
        new_q = current_q + self._alpha * (reward + self._gamma * max_next_q - current_q)

        self._q_table[state][action] = new_q

    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self._q_table, f)
        print(f"Tabela Q zapisana do {filename}")

    def load_q_table(self, filename="q_table.pkl"):
        try:
            with open(filename, 'rb') as f:
                self._q_table = pickle.load(f)
            print(f"Tabela Q wczytana z {filename}")
        except FileNotFoundError:
            print(f"Nie znaleziono pliku {filename}. Inicjalizuję pustą tabelę Q.")
            self._q_table = {}

    def train(self, opponent: Engine, num_episodes: int, GameClass: type[Game], game_config: dict[str: Any], BoardClass: type[Board], board_config: dict[str: Any], player: Player = None):
        wins = 0
        losses = 0
        draws = 0
        original_epsilon = self._epsilon
        print_every = int(num_episodes / 10)
        for episode in range(num_episodes):
            board = BoardClass(**board_config)
            game = GameClass(board, **game_config)
            last_move = None
            if player is None:
                player = game.get_current_player()

            while not game.is_finished()[0]:
                state = game.get_state_repr()
                if player == game.get_current_player():
                    action = self.choose_action(game.get_state_repr(), game.get_available_moves())
                    last_move = (state, action)
                    game.move(action)
                else:
                    opponent.run(game)
                    is_finished, winner = game.is_finished()
                    prev_state, prev_action = last_move
                    if last_move is not None and is_finished:
                        if winner is None:
                            reward = 0.5
                            draws += 1
                        elif winner == player:
                            reward = 1
                            wins += 1
                        else:
                            reward = -1
                            losses += 1
                    elif last_move is not None:
                        reward = 0
                    self.learn(prev_state, prev_action, reward, game.get_state_repr(), game.get_available_moves())

            if game.get_current_player() != player:  # Gra się skończyła ruchem agenta
                prev_state, prev_action = last_move
                is_finished, winner = game.is_finished()
                if winner is None:
                    reward = 0.5
                    draws += 1
                elif winner == player:
                    reward = 1
                    wins += 1
                else:
                    reward = -1
                    losses += 1
                self.learn(prev_state, prev_action, reward, game.get_state_repr(), game.get_available_moves())

            self._epsilon = max(0.01, original_epsilon * (1 - episode / num_episodes))
            if (episode + 1) % print_every == 0:
                print(f"Epizod: {episode + 1}/{num_episodes}")
                print(f"  Wygrane: {wins}, Przegrane: {losses}, Remisy: {draws}")
                print(f"  Procent wygranych: {100 * wins / (episode + 1):.2f}%")
                print(f"  Aktualny epsilon: {self._epsilon:.4f}")
                print(f"  Rozmiar tabeli Q: {len(self._q_table)}")

        print("\nTrening zakończony.")
        print(f"Ostateczny stosunek W/L/D: {wins}/{losses}/{draws}")
        print(f"Ostateczny procent wygranych: {100 * wins / num_episodes:.2f}%")
        self._epsilon = original_epsilon


    def run(self, game: Game) -> bool:
        original_epsilon = self._epsilon
        self._epsilon = 0
        game.move(self.choose_action(game.get_state_repr(), game.get_available_moves()))
        self._epsilon = original_epsilon
