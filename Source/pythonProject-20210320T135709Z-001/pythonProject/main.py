import time
import Grid as Grid
import Graph as Graph
import aseg_gdf2

gdf = aseg_gdf2.read(r'data/elevation/out4830223565355185480/ga/National_Gravity_Database_Sept2017', enginge="pandas")
names = gdf.field_names()
#elevation = gdf.get_field_data("GEOID_GRAVITY_METER_HEIGHT")
#elevation = gdf.get_field_data("GEOID_GROUND_ELEVATION")
elevation = gdf.get_fields_data(["GEOID_GROUND_ELEVATION", "LONGITUDE", "LATITUDE"])



#gdf = aseg_gdf2.read(r'data/elevation/out4830223565355185480/nsw/Southern_Thomson_Gravity_Traverses_P201401')
#names = gdf.field_names()
#gdf = aseg_gdf2.read(r'data/elevation/out4830223565355185480/qld/P201441_Boulia_2D_Regional_Sesimic_Gravity')
#names = gdf.field_names()


start = time.perf_counter()
test_grid = Grid.Grid(100, 100)
test_grid.addempty()
test_grid.grids[0][0].state = 1
test_grid.grids[0][1].state = 1
# Graph.fromgrid(test_grid.grids[0])
test_grid.next()
test_grid.next()
test_grid.next()
test_grid.next()
test_grid.next()
end = time.perf_counter()
print(test_grid.tostring())
print(f"processed in: {end - start} seconds")
