class Player():
    start = "\033[0;36m" # Red
    stop = "\033[0;0m" # All atributes off
    def __init__(self):
        self.type = 'P'
        self.symbol = self.start + u'\u25c0'u'\u25b6' + self.stop
        self.isAlive = True
        pass
