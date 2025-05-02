from Games.Connect4 import Conn4Board
from Engines.Minmax import Minmax
from Engines.Mcts import Mcts
from Body.Game import Game
from Body.Player import Player

class Connect_4_Minmax(Minmax):
    def three_in_a_row(self, game):
        board = game.get_board_state()

        # Horizontal wins
        for row in range(6):
            for column in range(5):
                for player in game.get_players():
                    if all(board[row][column + i] == player.get_attributes() for i in range(3)):
                        return True, player

        # Vertical wins
        for row in range(4):
            for column in range(7):
                for player in game.get_players():
                    if all(board[row + i][column] == player.get_attributes() for i in range(3)):
                        return True, player

        # Bottom-left to top-right wins
        for row in range(2, 6):
            for column in range(5):
                for player in game.get_players():
                    if all(board[row - i][column + i] == player.get_attributes() for i in range(3)):
                        return True, player

        # Top-left to bottom-right
        for row in range(4):
            for column in range(5):
                for player in game.get_players():
                    if all(board[row + i][column + i] == player.get_attributes() for i in range(3)):
                        return True, player

        return False, None

    def evaluate(self, game):
        if game.is_finished()[1] == self.player:
            return 100
        elif not game.is_finished()[1] is None:
            return -50
        elif self.three_in_a_row(game)[1] == self.player:
            return 20
        elif not self.three_in_a_row(game)[1] is None:
            return -10
        else:
            return 0



my_board = Conn4Board(Player(1, 'x'), Player(2, 'o'))
my_game = Game(my_board)
my_engine = Mcts(2000, 20)
my_engine_v2 = Connect_4_Minmax(depth=5, prun=True, player=my_game.get_current_player())

while not my_game.is_finished()[0]:
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    board = my_game.get_board_state()
    for x in board:
        print(x)
    i = int(input())
    my_game.move(i)
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    board = my_game.get_board_state()
    for x in board:
        print(x)
    #  my_engine.run(my_game)
    my_engine_v2.run(my_game)
