import copy
import Data


class Elevation:
    def __init__(self, gridwidth):
        self.gridwidth = gridwidth

    def map(self, area, grid):
        longitude_delta = area.topleft.longitude - area.topright.longitude
        latitude_delta = area.topleft.latitude - area.bottomright.latitude
        longitude_unit = longitude_delta / self.gridwidth
        latitude_unit = latitude_delta / self.gridwidth
        new_grid = copy.deepcopy(grid)
        allcoordinates = Data.getcoordinates()
        for cell in new_grid:
            center_longitude = (longitude_unit * cell.x) + (longitude_unit / 2)
            center_latitude = (latitude_unit * cell.y) + (latitude_unit / 2)
            min_longitude = min(list(map(lambda _: _.longitude, allcoordinates)), key=lambda _: center_longitude)
            # min_latitude = min(list(map(lambda _: _.latitude, allcoordinates)), key=lambda _: center_latitude)
            cell.elevation = next(filter(lambda _: _.longitude == min_longitude, allcoordinates)).elevation
        return new_grid
