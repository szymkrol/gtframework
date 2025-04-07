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
            move = self.pruning(self.player, deepcopy(game))[0]
        else:
            move = self.minimax(self.player, deepcopy(game))[0]
        Engine.run(self, game, move)

    #  @abstractmethod
    def evaluate(self,game):
        # print("gracz dla którego liczymy minimaxa: ",self.player)
        # print(game.is_finished())
        if game.is_finished()[1] is None:
            return 0
        elif game.is_finished()[1].get_id() == self.player:
            # print(game.is_finished()[1].get_id())

            return 100
        else:
            # print(game.is_finished()[1].get_id())
            return -50

    def minimax(self, player, game: Game, iteration=0) -> (int, int):



        moves = game.get_available_moves()
        n = len(moves)
        scores = [0 for _ in range(n)]
        # print(self.depth,iteration,moves)
        if player == self.player:
            multiplier = 1
        else:
            multiplier = -1
        multiplier = 1
        # print(n, )
        try:
            if iteration != self.depth and not game.is_finished()[0]:
                for i in range(n):
                    # print("obecny ruch to ",moves[i])
                    # print("*")
                    game.move(moves[i])
                    player = game.get_current_player()
                    value = self.minimax(player, deepcopy(game), iteration + 1)[1]
                    scores[i] += value
                    game.revert()
                    # print("\n\n")
            else:
                for i in range(n):
                    scores[i] += multiplier * self.evaluate(game)
        except:
            for i in range(n):
                scores[i] += multiplier * self.evaluate(game)

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
        #  print(result)
        indeks = moves.index(result)
        # print("wyniki na glebokosci ", iteration,scores)
        # print("wybrano ",indeks)
        return result, scores[indeks]

    def pruning(self, player, game, iteration=0, alpha=-math.inf, beta=math.inf):
        moves = game.get_available_moves()
        n = len(moves)
        scores = [0 for _ in range(n)]
        if player == self.player:
            multiplier = 1
        else:
            multiplier = -1
        if (not game.is_finished()) and n > 0:
            if iteration != self.depth:
                for i in range(n):
                    game.move(moves[i])
                    player = game.get_current_player()
                    if alpha <= beta:
                        value = self.pruning(player, game, iteration + 1,alpha,beta)[1]
                        scores[i] += value
                        if player == self.player:
                            if value > alpha:
                                alpha = value
                        else:
                            if value < beta:
                                beta = value
                    else:
                        scores[moves[i]] += -math.inf  # pruned
                    game.revert()
            else:
                for i in range(n):
                    scores[i] += multiplier * self.evaluate(game)
        else:
            for i in range(n):
                scores[i] += multiplier * self.evaluate(game)

        if player == self.player:
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
        return result, scores[result]
