from abc import ABC, abstractmethod
from copy import deepcopy
from Player import Player
from typing import Any, Self
from collections.abc import Hashable


class Board(ABC):
    def __init__(self, first_player: Player, second_player: Player, attributes: Any = None, turn_part: int = 0,
                 state_attr: Any = None, is_revertible: bool = True, remember_past: bool = True) -> None:
        """
        Initializer of Board object

        :param first_player: first player to move in a game.
        :param second_player: the other player.
        :param attributes: attributes of a board in general.
        :param turn_part: part of the move that is currently to be played.
        :param state_attr: attributes specific to initial board_state (attributes may change after move)
        :param is_revertible: if True, game can be reverted
        :param remember_past: if True, game remembers its past states
        """

        self._current_state = {"board_state": self.generate_empty_board(), "player_to_move": first_player,
                               "state_attr": state_attr}
        self._is_revertible = is_revertible
        self._remember_past = remember_past
        if self._remember_past:
            self._past_states = []  # Stack of past states
        self._players = [first_player, second_player]
        self._turn_part = turn_part
        # Optional attributes
        self._attributes = attributes

    def append_current_to_past(self) -> None:
        """Function takes current state and adds it to the stack of past states."""
        if self._remember_past:
            self._past_states.append(self._semi_copy_state(self._current_state))

    def set_current_state(self, new_state: dict[str: Any]) -> None:
        """Function sets current state to one given by an argument."""
        self._current_state = new_state

    def get_current_state(self) -> dict[str: Any]:
        return self._current_state

    def get_players(self) -> list[Player]:
        return self._players

    def pop_from_past(self) -> None | dict[str: Any]:
        """
        Function pops newest past state from the stack.

        :return: None if no past states on the stack or if game doesn't remember past states, else gets most recent
        past_state.
        """
        if len(self._past_states) == 0 or not self._remember_past:
            return None
        else:
            return self._past_states.pop()

    def is_past_stack_non_empty(self) -> bool:
        if self._remember_past:
            return bool(self._past_states)
        return True

    def get_player_to_move(self) -> Player:
        """Function returns player to move."""
        return self._current_state["player_to_move"]

    def _semi_copy_state(self, state: dict[str: Any]) -> dict[str: Any]:
        """
        Function returns semi_copy of current_state (deepcopy of board_state and state_attr, but reference to the
        same player_to_move.
        :param state: state to be copied.
        :return: semi_copy of a state.
        """
        return {"board_state": deepcopy(state["board_state"]), "player_to_move": state["player_to_move"],
                "state_attr": deepcopy(state["state_attr"])}

    def get_semi_copy(self) -> Self:
        """Returns a copy with a reference to the same players, but different board state and past_states."""
        new_board = self.__class__(self._players[0], self._players[1], attributes=deepcopy(self._attributes),
                                   turn_part=self._turn_part, is_revertible=self._is_revertible, remember_past=self._remember_past)
        new_board._current_state = self._semi_copy_state(self._current_state)
        if self._remember_past:
            new_board._past_states = [self._semi_copy_state(state) for state in self._past_states]
        return new_board

    def get_state_attr(self) -> Any:
        return self._current_state["state_attr"]

    def set_state_attr(self, attr: Any) -> None:
        self._current_state["state_attr"] = attr

    def _alternate_player(self) -> None:
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
    def change_board(self, move: Any):
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

    @abstractmethod
    def get_state_repr(self) -> Hashable:
        """Returns a hashable representation of current board state."""
        pass
