import copy

import Coordinate
import Data
import Open


class Elevation:
    def __init__(self, gridwidth, open=True):
        self.gridwidth = gridwidth
        if not open:
            self.coordinates = Data.getcoordinates()
            self.longitudes = copy.deepcopy(self.coordinates)
            self.longitudes.sort(key=lambda _: _.longitude)
            self.latitudes = copy.deepcopy(self.coordinates)
            self.latitudes.sort(key=lambda _: _.latitude)


    def map(self, area, grid):
        longitude_delta = abs(area.topleft.longitude - area.topright.longitude)
        latitude_delta = abs(area.topleft.latitude - area.bottomright.latitude)
        longitude_unit = longitude_delta / self.gridwidth
        latitude_unit = latitude_delta / self.gridwidth
        new_grid = copy.deepcopy(grid)
        for cell in new_grid:
            center_longitude = self.getsign(area.topleft.longitude) * ((longitude_unit * cell.x) + (longitude_unit / 2) + abs(area.topleft.longitude))
            center_latitude = ((latitude_unit * cell.y) + (latitude_unit / 2) + area.topleft.latitude)
            min_longitude = self.findlongitude(center_longitude)
            min_latitude = self.findlatitude(center_latitude)
            elevation = (min_longitude.elevation + min_latitude.elevation) / 2
            cell.center = Coordinate.Coordinate(center_longitude, center_latitude)
            cell.center.elevation = elevation
        return new_grid

    def mapopen(self, area, grid):
        longitude_delta = abs(area.topleft.longitude - area.topright.longitude)
        latitude_delta = abs(area.topleft.latitude - area.bottomright.latitude)
        longitude_unit = longitude_delta / self.gridwidth
        latitude_unit = latitude_delta / self.gridwidth
        new_grid = copy.deepcopy(grid)
        for cell in new_grid:
            center_longitude = self.getsign(area.topleft.longitude) * ((longitude_unit * cell.x) + (longitude_unit / 2) + abs(area.topleft.longitude))
            center_latitude = ((latitude_unit * cell.y) + (latitude_unit / 2) + area.topleft.latitude)
            cell.center = Coordinate.Coordinate(center_latitude, center_longitude)
        coordinates = [_.todict() for _ in new_grid]
        open = Open.todict(coordinates)
        for cell in new_grid:
            cell.center.elevation = next(filter(lambda _: _["latitude"] == cell.center.latitude and _["longitude"] == cell.center.longitude, open))["elevation"]
        return new_grid



    def findlongitude(self, longitude):
        current = copy.deepcopy(self.coordinates[0])
        for i in self.longitudes:
            if i.longitude <= abs(longitude):
                current = copy.deepcopy(i)
        return current

    def findlatitude(self, latitude):
        current = copy.deepcopy(self.coordinates[0])
        for i in self.latitudes:
            if i.latitude <= latitude:
                current = copy.deepcopy(i)
        return current

    def getsign(self, value):
        if value < 0:
            return -1
        else:
            return 1
