from random import choice
from .BoggleBase import BoggleBase
from FileParser.DictionaryParser import DictionaryParser


class WordBoggleBase(BoggleBase):
    def __init__(self, board_size):
        super().__init__(board_size)
        for row in self.board:
            for col in range(len(row)):
                row[col].value = choice(DictionaryParser.get_dict_meta('letters'))

        self.used_words = []

        self.board[2][0].value = 'c'
        self.board[2][1].value = 'o'
        self.board[2][2].value = 'w'

    def rules(self, move, rules_args=None):
        return move not in self.used_words and DictionaryParser.check_dict_word(word=move)

    def get_game_info(self):
        return f"The words used allready are: \n{' '.join(self.used_words)}"
