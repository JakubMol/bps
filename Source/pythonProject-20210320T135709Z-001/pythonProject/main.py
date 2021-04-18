import Grid as Grid
import Graph as Graph


test_grid = Grid.Grid(20, 20)
test_grid.addempty()
test_grid.grids[0][0].state = 1
test_grid.grids[0][1].state = 1
Graph.fromgrid(test_grid.grids[0])
test_grid.next()
print(test_grid.tostring())
