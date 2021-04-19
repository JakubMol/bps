import Cell as Cell
import Elevation
import Neighbours as Neighbours
import copy

class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grids = []

    def addempty(self):
        empty = []
        for x in range(self.y):
            for y in range(self.x):
                empty.append(Cell.Cell(x, y))
        self.grids.append(empty)

    def tostring(self):
        output = ""
        for index, grid in enumerate(self.grids):
            output += f"Grid #{index}\n"
            for cell in grid:
                output += f"{cell.tostring()}\n"
        return output

    def last(self):
        return self.grids[self.lastindex()]

    def lastindex(self):
        return len(self.grids) - 1

    def update(self, grid):
        self.grids[self.lastindex()] = grid

    def getcell(self, x, y):
        try:
            return copy.deepcopy(next(filter(lambda _: _.y == y, list(filter(lambda _: _.x == x, self.last())))))
        except StopIteration:
            return

    def getneighbours(self, x, y):
        neighbours = Neighbours.Neighbours()
        for i in range(-1, 2):
            for j in range(-1, 2):
                cell = self.getcell((x + i), (y + j))
                if cell is not None:
                    if x == 0 or y == 0:
                        if x == 0 and y == 0:
                            neighbours.central = cell
                        else:
                            neighbours.cardinal.append(cell)
                    if x != 0 and y != 0:
                        neighbours.ordinal.append(cell)
        return neighbours

    def next(self):
        grid = copy.deepcopy(self.last())
        for cell in grid:
            cell.state = self.getneighbours(cell.x, cell.y).getstate()
        self.grids.append(grid)

    def map(self, area):
        elevation = Elevation.Elevation(self.x)
        self.update(elevation.map(area, self.last()))

