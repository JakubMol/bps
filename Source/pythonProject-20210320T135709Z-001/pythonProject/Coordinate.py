class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = 0

    def todict(self):
        return {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'elevation': self.elevation,
        }