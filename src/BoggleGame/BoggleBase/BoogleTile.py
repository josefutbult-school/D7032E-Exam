# This is a container class that takes the function of a tile on the game board matrix.
class BoggleTile:
    traversed = False
    used_in_word = False

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)
