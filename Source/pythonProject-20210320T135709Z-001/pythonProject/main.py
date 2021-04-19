import time
import Grid
import Area

gridwidth = 25
area = Area.new(135.440455, -27.551875, 1, 1)
start = time.perf_counter()
test_grid = Grid.Grid(gridwidth, gridwidth)
test_grid.addempty()
test_grid.map(area)
test_grid.grids[0][0].state = 1
test_grid.grids[0][1].state = 1
test_grid.next()
end = time.perf_counter()
print(test_grid.tostring())
print(f"processed in: {end - start} seconds")
