from abc import ABC, abstractmethod

from Board import Board
from Player import Player
from typing import Any, Self


class Game:
    def __init__(self, board: Any, first_player: Player=None, second_player: Player=None) -> None:
        """
        Initializer creates Game object.

        :param board: initial game board, should be an instance of class, which inherits from Board.
        """

        self._board = board
        if first_player is None:
            first_player = self._board.get_players()[0]
        if second_player is None:
            second_player = self._board.get_players()[1]
        self._players = [first_player, second_player]

    def move(self, move: Any) -> Player:
        """
        Update the board state according to the move and return player to move.

        :param move: move to play on the board;
        :return: instance of the Player class that has a move.
        """
        self._board.append_current_to_past()
        self._board.change_board(move)
        return self._board.get_player_to_move()

    def can_revert(self) -> bool:
        """Returns True if one can revert move, False otherwise"""
        return self._board.is_past_stack_non_empty()

    def revert(self) -> Player | bool:
        """
        Change the board state to previous and return player to move.

        :return: instance of the Player class that has a move or False if no previous previous move.
        """
        if self._board.is_past_stack_non_empty():
            self._board.set_current_state(self._board.pop_from_past())
            return self._board.get_player_to_move()
        else:
            return False

    def is_finished(self) -> tuple[False, None] | tuple[True, Player]:
        """
        Function returns whether the game has finished according to standard game condition.

        If the game has finished returns also the player who has lost.
        :return: tuple with first element being a boolean value whether the game has ended and the second is
                 the player to have lost (if game not finished the player is None).
        """
        is_victory, winner = self._board.is_there_a_victory()
        if self._board.get_available_moves() and not is_victory:
            return False, None
        else:
            if is_victory:
                return True, winner
            else:
                return True, self._board.get_player_to_move()

    def get_current_player(self) -> Player:
        return self._board.get_player_to_move()

    def get_board_state(self) -> Any:
        return self._board.get_current_state()["board_state"]

    def get_available_moves(self) -> Any:
        return self._board.get_available_moves()

    def get_semi_copy(self) -> Self:
        return Game(self._board.get_semi_copy(), self._players[0], self._players[1])
