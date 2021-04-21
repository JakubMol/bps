class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__state = 0
        self.speedOfFireSpread = 0
        self.w = 1
        self.totalArea = self.w * self.w
        self.elevation = 0
        self.center = None

    def tostring(self):
        return f"Cell x:{self.x} y:{self.y} state:{self.state} speed of fire spread:{self.speedOfFireSpread} elevation: {self.elevation}"

    def todict(self):
        return {
            'longitude': self.center.longitude,
            'latitude': self.center.latitude,
            'state': self.state,
            'locations': "AUS",
        }

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        if state > 1:
            self.__state = 1
        else:
            self.__state = state
