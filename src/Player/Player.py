from IO.PlayerIO import PlayerIO


# 4478
class Player:
    def __init__(self, id):
        self.id = id
        self.points = 0

    def get_id(self):
        return self.id

    def parse_move(self, result):
        if result[0]:
            self.points += 1

        PlayerIO.write_player(self.id, result[1])

    def __str__(self):
        return f"Player {self.id}"

    @staticmethod
    def set_mocup(state):
        Player.mockup = state
