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
        pass

    @abstractmethod
    def evaluate(self):
        pass

    def minimax(self, player, game: Game, iteration=0) -> (int, int):
        moves = game.get_available_moves()
        scores = [0 for _ in range(max(moves)+1)]
        if player == self.player1:
            multiplier = 1
        else:
            multiplier = -1
        try:
            if iteration != self.depth:
                for i in moves:
                    game.move(i)
                    if player == self.player1:
                        player = self.player2
                    else:
                        player = self.player1
                    value = self.minimax(player, game, iteration+1)
                    scores[i] += value
                    game.revert()
            else:
                for i in moves:
                    scores[i] += multiplier*self.evaluate()
        except:
            for i in moves:
                scores[i] += multiplier * self.evaluate()

        if player == self.player1:
            best_choice_value = -math.inf
            for i in moves:
                if scores[i] > best_choice_value:
                    best_choice_value = scores[i]
        else:
            best_choice_value = math.inf
            for i in moves:
                if scores[i] < best_choice_value:
                    best_choice_value = scores[i]
        choices = []
        for i in moves:
            if scores[i] == best_choice_value:
                choices.append(i)
        result = random.choice(choices)
        return result, scores[result]
