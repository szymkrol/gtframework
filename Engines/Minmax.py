from abc import abstractmethod
import math
import random
from typing import Any
from copy import deepcopy

from Engines.Engine import Engine
from Body.Game import Game
from Body.Player import Player


class Minmax(Engine):
    def __init__(self, depth: int, prun: bool, player: Player) -> None:
        self.depth = depth
        self.prun = prun
        self.player = player  # gracz, dla którego minimax liczy ruch

    def run(self, game: Game) -> bool:
        if self.prun:
            move = self.pruning(game)[0]
        else:
            move = self.minimax(game)[0]
        return Engine.run(self, game, move)

    @abstractmethod
    def evaluate(self, game):
        pass

    def minimax(self, game: Game, iteration: int=0) -> tuple[Any, int]:
        moves = game.get_available_moves()
        n = len(moves)
        scores = [0 for _ in range(n)]
        if iteration != self.depth and not game.is_finished()[0]:
            for i in range(n):
                game.move(moves[i])
                value = self.minimax( deepcopy(game), iteration + 1)[1]
                scores[i] += value
                game.revert()
        else:
            return None, self.evaluate(game)
        if game.get_current_player() == self.player:
            best_choice_value = -math.inf
            for i in range(n):
                if scores[i] > best_choice_value:
                    best_choice_value = scores[i]
        else:
            best_choice_value = math.inf
            for i in range(n):
                if scores[i] < best_choice_value:
                    best_choice_value = scores[i]
        choices = []
        for i in range(n):
            if scores[i] == best_choice_value:
                choices.append(moves[i])
        result = random.choice(choices)
        indeks = moves.index(result)
        return result, scores[indeks]

    def pruning(self, game: Game, iteration: int=0, alpha: float | int=-math.inf, beta: float | int =math.inf) -> tuple[Any, int]:
        moves = game.get_available_moves()
        n = len(moves)
        scores = [0] * n

        if iteration != self.depth and not game.is_finished()[0]:
            for i, move in enumerate(moves):
                if alpha <= beta:
                    game.move(move)
                    value = self.pruning(game, iteration + 1, alpha, beta)[1]
                    game.revert()

                    scores[i] += value
                    if game.get_current_player() == self.player:
                        if value > alpha:
                            alpha = value
                    else:
                        if value < beta:
                            beta = value
                else:
                    scores[i] += -math.inf  # pruned
        else:
            return None, self.evaluate(game)

        if game.get_current_player() == self.player:
            best_choice_value = max(scores)
        else:
            best_choice_value = min(scores)

        choices = [moves[i] for i in range(n) if scores[i] == best_choice_value]

        result = random.choice(choices)
        return result, best_choice_value
