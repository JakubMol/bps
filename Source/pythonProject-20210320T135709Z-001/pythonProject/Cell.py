class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__state = 0
        self.speedOfFireSpread = 0
        self.w = 1
        self.totalArea = self.w * self.w
        self.center = None

    def tostring(self):
        return f"Cell x:{self.x} y:{self.y} state:{self.state} speed of fire spread:{self.speedOfFireSpread} elevation: {self.center.elevation}"

    def todict(self):
        return {
            'longitude': self.center.longitude,
            'latitude': self.center.latitude,
            #'state': self.state,
            #'locations': "AUS",
        }

    def tocsv(self, gridid):
        return {
            'longitude': self.center.longitude,
            'latitude': self.center.latitude,
            'state': self.state,
            'elevation': self.center.elevation,
            'gridid': gridid
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

    @property
    def elevation(self):
        return self.center.elevation
