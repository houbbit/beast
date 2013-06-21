class Rock():
    start = "\033[0;32;42m" # Green
    stop = "\033[0;0m" # All atributes off
    def __init__(self):
        self.type = 'R'
        self.symbol = self.start + u'\u2588'u'\u2588' + self.stop
        pass
