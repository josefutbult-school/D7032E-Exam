from .WordBoggleBase import WordBoggleBase


class StandardBoggle(WordBoggleBase):
    def check_move(self, player, move, rules_args=None) -> tuple:
        return (True, "Word exists in wordlist!") if self._check_move(move=move) \
            else (False, "No such word in wordlist, or word occupied")
