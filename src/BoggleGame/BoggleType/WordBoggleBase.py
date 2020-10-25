from abc import ABC

from BoggleGame.BoggleBase.BoggleBase import BoggleBase
from FileParser.DictionaryParser import DictionaryParser
from FileParser.SettingsParser import SettingsParser


# This is an abstract class meant to be one of two implemented by a game mode.
# It allows a child class to operate on a dictionary of words.
class WordBoggleBase(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super(WordBoggleBase, self).__init__(number_of_boards, board_size)
        self.words_in_board = []

    def create_board(self, board_size, tile_config_name=None) -> list:
        if board_size not in [4, 5]:
            raise IOError(f"Board size: {board_size}")
        board = super(WordBoggleBase, self). \
            create_board(board_size=board_size, tile_config_name='boggle16' if board_size == 4 else 'boggle25')

        return board

    # Checks if a move is an instance of a dictionary and not already used.
    def rules(self, board_id, move, register_used_word, rules_args=None) -> bool:
        if move not in self.get_used_words(board_id) and DictionaryParser.check_dict_word(word=move):
            if register_used_word:
                self.get_used_words(board_id).append(move)
            return True
        return False

    def get_game_info(self, board_id):
        return f"The words used already are: \n{' '.join(self.get_used_words(board_id))}"

    # Prints out all the possible words on the board for all players
    def get_game_end_info(self):
        if SettingsParser.get_setting('show_solution'):
            return "The board contained the following words:\n" + ', '.join(self.words_in_board)
        return super(WordBoggleBase, self).get_game_end_info()

    # Runs a parallel process to the game, first filtering out all words in a dictionary which letters are not
    # a letter on the board, and than runs the same _check_move method as an ordinary player on all the
    # remaining words.
    def game_paralell_process(self):
        board = self.get_board(0)
        letters = []
        for row in board:
            for char in row:
                letters.append(char.value)
        letters = list(dict.fromkeys(letters))

        def check_word(word):
            for character in list(word):
                if character not in letters:
                    return False
            return self._check_move(word, 0, generous_boggle, register_used_word=False)

        generous_boggle = SettingsParser.get_setting('generous_boggle')
        self.words_in_board = list(filter(check_word, [word.lower() for word in DictionaryParser.wordlist]))

    # The 'Qu' tile is a special case for word based boggle, which means that this two characters must be
    # interpreted as one tile.
    def split_move(self, move) -> tuple:
        if move[0] == 'q' and move[1] == 'u':
            return 'qu', move[2:]
        else:
            return super(WordBoggleBase, self).split_move(move)

    def get_words_in_board(self):
        return self.words_in_board
