from abc import ABC, abstractmethod
from copy import deepcopy
from Player import Player

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
