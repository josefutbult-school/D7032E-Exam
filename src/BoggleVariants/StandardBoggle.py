from .BoggleBase import BoggleBase
from FileParser.DictionaryParser import DictionaryParser


class StandardBoggle(BoggleBase):
    def check_move(self, move):
        return DictionaryParser.check_dict_word(move)
