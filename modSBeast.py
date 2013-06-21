class SuperBeast():
    start = "\033[0;31m" # Red
    stop = "\033[0;0m" # All atributes off
    def __init__(self):
        self.type = 'S'
        self.symbol = self.start + u'\u255f'u'\u2562' + self.stop
        self.isAlive = True
        pass
