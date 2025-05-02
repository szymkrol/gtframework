import random

from Engines.Engine import Engine
from Body.Game import Game


class RandEng(Engine):
    def run(self, game: Game) -> bool:
        move = random.choice(game.get_available_moves())
        return super().run(game, move)
