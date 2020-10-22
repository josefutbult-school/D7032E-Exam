from abc import ABC

from BoggleGame.BoggleBase.BoggleBase import BoggleBase
from FileParser.DictionaryParser import DictionaryParser


class WordBoggleBase(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super(WordBoggleBase, self).__init__(number_of_boards, board_size)

    def create_board(self, board_size, tile_config_name=None) -> list:
        if board_size not in [4, 5]:
            raise IOError(f"Board size: {board_size}")
        board = super(WordBoggleBase, self).\
            create_board(board_size=board_size, tile_config_name='boggle16' if board_size == 4 else 'boggle25')

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
