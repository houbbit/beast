class Eggs():
    start = "\033[0;31m" # Red
    stop = "\033[0;0m" # All atributes off
    def __init__(self):
        self.type = 'E'
        self.symbol = self.start + u'\xa4'u'\xa4' + self.stop
        self.isAlive = True
        pass
