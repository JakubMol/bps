import time
import Grid
import Area
import Data

Data.getnetcdf()

gridwidth = 25
area = Area.new(-22, 131, 1, 1)
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
test_grid.todataframe().to_csv(r"data/temp/test_grid.csv")

