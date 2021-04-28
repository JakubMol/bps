import time
import Grid
import Area
import Data
import math
import numpy


def run(runs, gridwidth, area, active):
    #gridwidth = 40
    #area = Area.new(-22, 131, 1, 1)



    start = time.perf_counter()
    test_grid = Grid.Grid(gridwidth, gridwidth)
    test_grid.addempty()
    test_grid.mapopen(area)
    if len(active.values) > 0:
        for cell in active.values:
            test_grid.grids[0][numpy.int_(cell[5])].state = cell[3]
            test_grid.grids[0][numpy.int_(cell[5])].speedOfFireSpread = cell[4]
    test_grid.next()
    end = time.perf_counter()
    print(f"setup processed in: {end - start} seconds")

    gridPath = r"data/temp/test_grid.csv"
    runs_start = time.perf_counter()
    for i in range(0, runs):
        test_grid.next()
        if i % 10 == 0:
            print(f"{i} grids created")
            test_grid.todf().to_csv(gridPath)

    runs_end = time.perf_counter()
    print(f"{runs} runs in: {runs_end - runs_start} seconds")
    test_grid.todf().to_csv(gridPath)
