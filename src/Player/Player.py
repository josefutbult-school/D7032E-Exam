# This class works as a container for a specific players data, and some simple functionality
class Player:
    def __init__(self, id):
        self.id = id
        self.points = 0

    def get_id(self):
        return self.id

    def parse_move(self, result, score) -> str:
        if result[0]:
            self.points += score

        return result[1]

    def get_points(self):
        return self.points

    def __str__(self):
        return f"Player {self.id}"

    @staticmethod
    def set_mocup(state):
        Player.mockup = state
