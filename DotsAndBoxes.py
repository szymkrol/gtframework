from Player import Player
from Board import Board
from Game import Game
from Engine import Engine
from Mcts import Mcts
from Lattice import LatticeNode, Lattice, get_neigh_coords


class DotsAndBoxes(Board):

    def __init__(self, first_player: Player, second_player: Player, attributes):
        self._size = attributes
        super().__init__(first_player, second_player, attributes)
        self._score = 0


    def generate_empty_board(self):
        return Lattice(self._size + 1)

    def change_board(self, move):
        node_a = self.get_current_state()["board_state"].get_field(move[0])
        node_b = self.get_current_state()["board_state"].get_field(move[1])
        node_a.remove_connection(node_b)
        score_change = 0
        for node in [node_a, node_b]:
            if node.is_closed():
                if self.get_current_state()["player_to_move"].get_attributes():
                    score_change += 1
                else:
                    score_change -= 1
        if score_change == 0:
            self._alternate_player()

    def get_available_moves(self):
        available_moves = []
        for i in range(0, self._size + 1):
            for j in range(0, self._size + 1):
                if (i == 0 or i == self._size) and (j == 0 or j == self._size):
                    continue
                nodes = self.get_current_state()["board_state"].get_lower_right_connections((i, j))
                for node in nodes:
                    available_moves.append(((i, j), node.get_coords()))
        return available_moves

    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        if len(self.get_available_moves()) == 0:
            if self._score == 0:
                return False, None
            players = self.get_players()
            if self._score > 0:
                if players[0].get_attributes():
                    winner = players[0]
                else:
                    winner = players[1]
            else:
                if players[0].get_attributes():
                    winner = players[1]
                else:
                    winner = players[0]
            return True, winner
        else:
            return False, None


my_board = DotsAndBoxes(Player(1, True), Player(2, False), 5)
my_game = Game(my_board)
my_engine = Mcts(500, 10)

while not my_game.is_finished()[0]:
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    i = int(input())
    j = int(input())
    x = (i, j)
    i = int(input())
    j = int(input())
    my_game.move((x, (i, j)))
    print(f"It is now turn of: {my_game.get_current_player().get_attributes()}")
    my_engine.run(my_game)
