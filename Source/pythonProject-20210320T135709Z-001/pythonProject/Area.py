import Coordinate


class Area:
    def __init__(self, topleft, topright, bottomleft, bottomright):
        self.bottomright = bottomright
        self.bottomleft = bottomleft
        self.topright = topright
        self.topleft = topleft


def new(longitude, latitude, longitudedelta, latitudedelta):
    topleft = Coordinate.Coordinate(longitude, latitude)
    topright = Coordinate.Coordinate(topleft.longitude + longitudedelta, topleft.latitude)
    bottomleft = Coordinate.Coordinate(topleft.longitude, topleft.latitude - latitudedelta)
    bottomright = Coordinate.Coordinate(topleft.longitude + longitudedelta, topleft.latitude - latitudedelta)
    return Area(topleft, topright, bottomleft, bottomright)
