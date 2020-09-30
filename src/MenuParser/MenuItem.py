class MenuItem:
    def __init__(self, text, key, function, args=None):
        self.text = text
        self.key = key
        self.function = function
        self.args = args
