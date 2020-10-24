from BoggleGame.BoardTypes.MultipleBoardBoggle import MultipleBoardBoggle
from BoggleGame.BoggleType.WordBoggleBase import WordBoggleBase


# This game mode is a word based mode where the different players gets their own isolated board
class StandardBoggle(WordBoggleBase, MultipleBoardBoggle):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)

    def check_move(self, board_id, move, generous_boggle, rules_args=None) -> tuple:
        return (True, "Word exists in wordlist!") if self._check_move(board_id=board_id,
                                                                      move=move,
                                                                      generous_boggle=generous_boggle) \
            else (False, "No such word in wordlist, or word occupied")

    def __str__(self):
        return "Standard Boggle"

    @staticmethod
    def get_name():
        return "Standard Boggle"
