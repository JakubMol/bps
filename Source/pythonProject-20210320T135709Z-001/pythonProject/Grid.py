import Cell as Cell
import Elevation
import Neighbours as Neighbours
import copy
import pandas

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
                    if cell.x == x or cell.y == y:
                        if cell.x == x and cell.y == y:
                            neighbours.central = cell
                        else:
                            neighbours.cardinal.append(cell)
                    if cell.x != x and cell.y != y:
                        neighbours.ordinal.append(cell)
        return neighbours

    def next(self):
        grid = copy.deepcopy(self.last())
        for cell in grid:
            state = self.getneighbours(cell.x, cell.y).getstate()
            if state < 0:
                cell.state = 0
            if state > 1:
                cell.state = 1
            if 0 < state < 1:
                cell.state = state

        self.grids.append(grid)

    def map(self, area):
        elevation = Elevation.Elevation(self.x)
        self.update(elevation.map(area, self.last()))

    def mapopen(self, area):
        elevation = Elevation.Elevation(self.x)
        self.update(elevation.mapopen(area, self.last()))

    def todataframe(self):
        grid = self.last()
        return pandas.DataFrame.from_records([_.todict() for _ in grid])

    def todict(self):
        return [_.todict() for _ in self.last()]

    def tocsv(self):
        data = []
        for index, grid in enumerate(self.grids):
            data.extend([_.tocsv(index) for _ in grid])
        return data

    def todf(self):
        return pandas.DataFrame.from_records(self.tocsv())