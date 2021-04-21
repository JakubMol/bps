import aseg_gdf2
import pandas
import Coordinate
import xarray

def getcoordinates():
    gdf = aseg_gdf2.read(r'data/elevation/out4830223565355185480/ga/National_Gravity_Database_Sept2017',
                         enginge="pandas")
    # gdf = aseg_gdf2.read(r'data/elevation/out4830223565355185480/nsw/Southern_Thomson_Gravity_Traverses_P201401')
    # names = gdf.field_names()
    # gdf = aseg_gdf2.read(r'data/elevation/out4830223565355185480/qld/P201441_Boulia_2D_Regional_Sesimic_Gravity')
    # names = gdf.field_names()
    elevation = gdf.get_fields_data(["GEOID_GROUND_ELEVATION", "LONGITUDE", "LATITUDE"])
    coordinates = []
    for i in range(0, len(elevation[0]) - 1):
        coordinate = Coordinate.Coordinate(elevation[1][i], elevation[2][i])
        coordinate.elevation = elevation[0][i]
        coordinates.append(coordinate)
    return coordinates


def todataframe():
    return pandas.DataFrame.from_records([_.todict() for _ in getcoordinates()])

def getnetcdf():
    ds = xarray.open_dataset(r"data/elevation/north/Gravmap2019-grid-dem_geoid.nc")
    df = ds.to_dataframe()



