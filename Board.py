from abc import ABC, abstractmethod
from copy import deepcopy
from Player import Player


class Board(ABC):
    def __init__(self, first_player: Player, second_player: Player, attributes=None, turn_part = 0):
        self._current_state = {"board_state": self.generate_empty_board(), "player_to_move": first_player}
        self._past_states = []  # Stack of past states
        self._players = [first_player, second_player]
        self._turn_part = turn_part
        # Optional attributes
        self._attributes = attributes

    def append_current_to_past(self):
        """Function takes current state and adds it to the stack of past states."""
        self._past_states.append(self._semi_copy_state(self._current_state))

    def set_current_state(self, new_state):
        """Function sets current state to one given by an argument."""
        self._current_state = new_state

    def get_current_state(self):
        return self._current_state

    def get_players(self):
        return self._players

    def pop_from_past(self):
        """Function pops newest past state from the stack."""
        if len(self._past_states) == 0:
            return False
        else:
            return self._past_states.pop()

    def is_past_stack_non_empty(self) -> bool:
        return bool(self._past_states)

    def get_player_to_move(self):
        """Function returns player to move."""
        return self._current_state["player_to_move"]

    def _semi_copy_state(self, state):
        return {"board_state": deepcopy(state["board_state"]), "player_to_move": state["player_to_move"]}

    def get_semi_copy(self):
        """Returns a copy with a reference to the same players, but different board state and past_states."""
        new_board = self.__class__(self._players[0], self._players[1], attributes=deepcopy(self._attributes))
        new_board._current_state = self._semi_copy_state(self._current_state)
        new_board._past_states = [self._semi_copy_state(state) for state in self._past_states]
        return new_board

    def _alternate_player(self):
        """Function changes current player to the other one."""
        player = self.get_current_state()["player_to_move"]
        if player == self.get_players()[0]:
            self.get_current_state()["player_to_move"] = self.get_players()[1]
        else:
            self.get_current_state()["player_to_move"] = self.get_players()[0]

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
