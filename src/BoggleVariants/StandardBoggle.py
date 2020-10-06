from .BoggleBase import BoggleBase
from FileParser.DictionaryParser import DictionaryParser


class StandardBoggle(BoggleBase):
    def check_move(self, player, move) -> tuple:
        return (True, "Word exists in wordlist!") if DictionaryParser.check_dict_word(move) \
            else (False, "No such word in wordlist")
