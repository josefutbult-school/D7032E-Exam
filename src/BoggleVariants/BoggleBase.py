class BoggleBase():
    def __init__(self, board_size):
        self.board = [['n'] * board_size] * board_size

    def get_board(self):
        return self.board

    def check_move(self, player, move) -> tuple:
        raise NotImplementedError()

