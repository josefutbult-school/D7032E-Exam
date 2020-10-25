from abc import ABC

from BoggleGame.BoggleBase.BoggleBase import BoggleBase


# This is an abstract class meant to be one of two implemented by a game mode. It lets the
# lets the different players share a single board, making their moves impact each other.
class SingleBoardBoggle(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)
        self.board = self.create_board(board_size)
        self.used_words = []

    def get_board(self, board_id) -> list:
        return self.board

    def get_used_words(self, board_id) -> list:
        return self.used_words

    def set_board_value(self, position, value):
        self.board[position[0]][position[1]].value = value