from abc import abstractmethod
import math
import random
from Engine import Engine
from Game import Game
from Board import Board
from Player import Player


class Minmax(Engine):
    def __init__(self, depth, prun, board: Board, player1: Player, player2: Player):
        self.depth = depth
        self.prun = prun
        self.board = board
        self.player1 = player1.get_id()
        self.player2 = player2.get_id()

    def run(self, game, move):  # nie za bardzo wiem, jak to uzupełnić
        if self.prun:
            move = self.minimax(self.player2,game)[0]
        else:
            move = self.pruning(self.player2,game)[0]
        Engine.run(self, game, move)

    @abstractmethod
    def evaluate(self):
        pass

    def minimax(self, player, game: Game, iteration=0) -> (int, int):
        moves = game.get_available_moves()
        n = len(moves)
        scores = [0 for _ in range(n)]
        if player == self.player1:
            multiplier = 1
        else:
            multiplier = -1
        if (not game.is_finished()) and n > 0:
            if iteration != self.depth:
                for i in range(n):
                    game.move(moves[i])
                    player = game.get_current_player()
                    value = self.minimax(player, game, iteration+1)[1]
                    scores[i] += value
                    game.revert()
            else:
                for i in range(n):
                    scores[i] += multiplier*self.evaluate()
        else:
            for i in range(n):
                scores[i] += multiplier * self.evaluate()

        if player == self.player1:
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

    def pruning(self,player,game,iteration=0,alpha=math.inf,beta= -math.inf):
        pass
