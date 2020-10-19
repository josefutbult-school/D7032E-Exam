class BoggleTile:
    traversed = False
    value = None
    used_in_word = False

    def __str__(self):
        return str(self.value)
