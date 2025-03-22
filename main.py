from abc import ABC, abstractmethod
from copy import deepcopy


class Player:
    def __init__(self, id, attributes=None):
        self.__id = id
        # Optional attributes
        self.__attributes = attributes

    def get_id(self):
        return self.__id

    def get_attributes(self):
        return self.__attributes


class Board(ABC):
    def __init__(self, first_player: Player, second_player: Player, attributes=None):
        self.__current_state = {"board_state": self.generate_empty_board(), "player_to_move": first_player}
        self.__past_states = []  # Stack of past states
        self.__players = [first_player, second_player]
        # Optional attributes
        self.__attributes = attributes

    def append_current_to_past(self):
        """Function takes current state and adds it to the stack of past states."""
        self.__past_states.append(deepcopy(self.__current_state))

    def set_current_state(self, new_state):
        """Function sets current state to one given by an argument."""
        self.__current_state = new_state

    def get_current_state(self):
        return self.__current_state

    def get_players(self):
        return self.__players

    def pop_from_past(self):
        """Function pops newest past state from the stack."""
        if self.__past_states.length() == 0:
            return False
        else:
            return self.__past_states.pop()

    def is_past_stack_non_empty(self) -> bool:
        return bool(self.__past_states)

    def get_player_to_move(self):
        """Function returns player to move."""
        return self.__current_state["player_to_move"]

    @abstractmethod
    def generate_empty_board(self):
        """Function should generate an empty board_state."""
        pass

    @abstractmethod
    def change_board(self, move):
        """
        Function should change self.__current_state according to the move.

        Function assumes it is a turn of the player_to_move. It should update board_state and player_to_move.
        """
        pass

    @abstractmethod
    def get_available_moves(self):
        """Function should return a list of available moves for a player_to_move."""
        pass

    @abstractmethod
    def is_there_a_victory(self) -> tuple[False, None] | tuple[True, Player]:
        """If there is any non-standard victory condition, it should return whether the game has finished and which
         player has won; otherwise it should return tuple(False, None)"""
        pass


class Game:
    def __init__(self, board):
        """
        Initializer creates Game object.

        :param board: inital game board, should be an instance of class which inherits from Board.
        """
        self.__board = board

    def move(self, move) -> Player:
        """
        Update the board state according to the move and return player to move.

        :param move: move to play on the board;
        :return: instance of the Player class that has a move.
        """
        self.__board.append_current_to_past()
        self.__board.change_board(move)
        return self.__board.get_player_to_move()

    def can_revert(self) -> bool:
        """Returns True if one can revert move, False otherwise"""
        return self.__board.is_past_stack_non_empty()

    def revert(self) -> Player | False:
        """
        Change the board state to previous and return player to move.

        :return: instance of the Player class that has a move or False if no previous previous move.
        """
        if self.__board.is_past_stack_non_empty():
            self.__board.set_current_state(self.__board.pop_from_past())
            return self.__board.get_player_to_move()
        else:
            return False

    def is_finished(self) -> tuple[False, None] | tuple[True, Player]:
        """
        Function returns whether the game has finished according to standard game condition.

        If the game has finished returns also the player who has lost.
        :return: tuple with first element being a boolean value whether the game has ended and the second is
                 the player to have lost (if game not finished the player is None).
        """
        is_victory, winner = self.__board.is_there_a_victory()
        if self.__board.get_available_moves() and not is_victory:
            return False, None
        else:
            if is_victory:
                return True, winner
            else:
                return True, self.__board.get_player_to_move()

    def get_current_player(self):
        return self.__board.get_player_to_move()

    def get_board_state(self):
        return self.__board.get_current_state()["board_state"]


class Engine:
    def minmax(self, depth, is_ab, eval_fun, game):
        pass

    def mcts(self, iter, time, game):
        pass
