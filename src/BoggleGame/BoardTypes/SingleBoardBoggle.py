from abc import ABC

from BoggleGame.BoggleBase.BoggleBase import BoggleBase


class SingleBoardBoggle(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)
        self.board = self.create_board(board_size)
        self.used_words = []

    def get_board(self, board_id) -> list:
        return self.board

    def get_used_words(self, board_id) -> list:
        return self.used_words
