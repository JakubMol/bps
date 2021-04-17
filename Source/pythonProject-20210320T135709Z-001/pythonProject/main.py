import Grid as Grid


test_grid = Grid.Grid(50, 50)
test_grid.addempty()
for i in test_grid.getneighbours(49, 49):
    print(i.tostring())