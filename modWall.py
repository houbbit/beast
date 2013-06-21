class Wall():
    start = "\033[1;33;103m" # Bright yellow background and foreground
    stop = "\033[0;0m" # All atributes off
    def __init__(self):
        self.type = 'W'
        self.symbol = self.start + u'\u2588'u'\u2588' + self.stop
        pass
