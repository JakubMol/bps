import Cell as Cell


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grids = []

    def initialise(self):
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
