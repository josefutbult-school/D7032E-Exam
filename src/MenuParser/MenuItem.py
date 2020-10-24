# This class works as a container for a single menu item presented by HostIO.
class MenuItem:
    def __init__(self, text, key, function, args=()):
        self.text = text
        self.key = key
        self.function = function
        self.args = args
