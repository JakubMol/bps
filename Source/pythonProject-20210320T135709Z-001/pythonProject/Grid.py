import Cell as Cell
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
        return self.grids[len(self.grids) - 1]

    def getcell(self, x, y):
        try:
            return copy.deepcopy(next(filter(lambda _: _.y == y, list(filter(lambda _: _.x == x, self.last())))))
        except StopIteration:
            return

    def getneighbours(self, x, y):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                cell = self.getcell((x + i), (y + j))
                if cell is not None:
                    neighbours.append(cell)
        return neighbours
