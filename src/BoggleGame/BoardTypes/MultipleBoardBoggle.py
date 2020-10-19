from abc import ABC

from BoggleGame.BoggleBase.BoggleBase import BoggleBase


class MultipleBoardBoggle(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)
        self.used_words = [[] for i in range(number_of_boards)]
        self.boards = [self.create_board(board_size)]

        for i in range(1, board_size):
            self.boards.append(self.create_board(board_size))
            for row in range(board_size):
                for col in range(board_size):
                    self.boards[-1][row][col].value = self.boards[0][row][col].value

    def get_board(self, board_id) -> list:
        return self.boards[board_id]

    def get_used_words(self, board_id) -> list:
        return self.used_words[board_id]
