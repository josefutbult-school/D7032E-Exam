from .WordBoggleBase import WordBoggleBase


class GenerousBoggle(WordBoggleBase):
    def __init__(self, board_size):
        super().__init__(board_size)
        self.store_traversed_tiles = False

    def check_move(self, player, move) -> tuple:
        return (True, "Word exists in wordlist!") if super().check_move(player, move) \
            else (False, "No such word in wordlist")
