from Game import Game


class Engine:
    def run(self, game: Game, move: object) -> bool:
        """
        Method makes move in game.
        :param game: game to play move
        :param move: move to be done
        :return: False if move is wrong or game is finished, otherwise True
        """
        if game.is_finished()[0]:
            return False
        if move in game.get_available_moves():
            game.move(move)
            return True
        else:
            return False
