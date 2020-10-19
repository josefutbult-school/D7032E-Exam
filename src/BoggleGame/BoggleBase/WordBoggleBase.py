from abc import ABC
from random import choice

from BoggleGame.BoggleBase.BoggleBase import BoggleBase
from FileParser.DictionaryParser import DictionaryParser


class WordBoggleBase(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super(WordBoggleBase, self).__init__(number_of_boards, board_size)

    def create_board(self, board_size) -> list:
        board = super(WordBoggleBase, self).create_board(board_size)
        for row in board:
            for col in range(len(row)):
                row[col].value = choice(DictionaryParser.get_dict_meta('letters'))

        board[2][0].value = 'c'
        board[2][1].value = 'o'
        board[2][2].value = 'w'

        return board

    def rules(self, board_id, move, rules_args=None) -> bool:
        if move not in self.get_used_words(board_id) and DictionaryParser.check_dict_word(word=move):
            self.get_used_words(board_id).append(move)
            return True
        return False

    def get_game_info(self, board_id):
        return f"The words used already are: \n{' '.join(self.get_used_words(board_id))}"
