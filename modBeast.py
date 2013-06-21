class Beast():
    start = "\033[0;31m" # Red
    stop = "\033[0;0m" # All atributes off
    def __init__(self):
        self.type = 'B'
        self.symbol = self.start + u'\u251c'u'\u2524' + self.stop
        self.isAlive = True
        pass
