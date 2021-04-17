class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = 0
        self.speedOfFireSpread = 0

    def tostring(self):
        return f"Cell x:{self.x} y:{self.y} state:{self.state} speed of fire spread:{self.speedOfFireSpread}"
