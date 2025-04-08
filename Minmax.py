from abc import abstractmethod
import math
import random
from Engine import Engine
from Game import Game
from Player import Player
from copy import deepcopy


class Minmax(Engine):
    def __init__(self, depth, prun, player: Player):
        self.depth = depth
        self.prun = prun
        self.player = player.get_id()  # gracz, dla którego minimax liczy ruch

    def run(self, game):
        if self.prun:
            move = self.pruning( deepcopy(game))[0]
        else:
            move = self.minimax( deepcopy(game))[0]
        Engine.run(self, game, move)

    #  @abstractmethod
    def evaluate(self, game):
        if game.is_finished()[1] is None:
            return 0
        elif game.is_finished()[1].get_id() == self.player:
            return 100
        else:
            return -50

    def minimax(self, game: Game, iteration=0) -> (int, int):
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
        if iteration % 2 == 0:
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

    def pruning(self, game, iteration=0, alpha=-math.inf, beta=math.inf):
        moves = game.get_available_moves()
        n = len(moves)
        scores = [0 for _ in range(n)]
        if iteration != self.depth and (not game.is_finished()[0]):
            for i in range(n):
                game.move(moves[i])
                if alpha <= beta:
                    value = self.pruning( deepcopy(game), iteration + 1,alpha,beta)[1]
                    scores[i] += value
                    if iteration % 2 == 0:
                        if value > alpha:
                            alpha = value
                    else:
                        if value < beta:
                            beta = value
                else:
                    scores[i] += -math.inf  # pruned
                game.revert()
        else:
            return None,self.evaluate(game)
        if iteration % 2 == 0:
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
