from Engine import Engine
from Game import Game
import random

class RandEng(Engine):
    def run(self, game: Game) -> bool:
        move = random.choice(game.get_available_moves())
        return super().run(game, move)
