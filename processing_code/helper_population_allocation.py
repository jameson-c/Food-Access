""" 
This script creates a dataset that has the population estimate for each building in our buildings dataset. 

NOTE:
Currently, since I don't fully understand the mapping of geoids in ACS to geoids in buildings dataset, I am randomly allocating population, to create a pipeline. This needs to be modified soon. 

"""
# Import libraries
import geopandas as gpd
import pandas as pd
from shapely import wkt

def get_population(geopandas_dataframe):
    population = pd.read_csv('ACSData.csv')
    # Allocate population based on number of units (random, needs to be changed later)
    res_buildings = geopandas_dataframe[geopandas_dataframe['class_reco'].str.contains('Residential')]
    # res_buildings = geopandas_dataframe   # Trying to save population values to the larger dataframe. Will contain values only for residential buildings.   
    population['geometry'] = population['geometry'].apply(wkt.loads) # get population geometries
    geo_population = gpd.GeoDataFrame(population, geometry = 'geometry').set_crs(res_buildings.crs) # turn into polygons
    # Merge buildings with acs Data
    merge = res_buildings.sjoin(geo_population, how='inner')

    # generate initial popultion multiplier
    merge['population'] = 0 # baseline is nobody lives in a building
    merge.loc[merge['class_reco'] == '1-Unit Residential', 'population'] = 1
    merge.loc[merge['class_reco'] == '2-Unit Residential', 'population'] = 2
    merge.loc[merge['class_reco'] == '3-Unit Residential', 'population'] = 3
    merge.loc[merge['class_reco'] == '4+ Unit Residential', 'population'] = 4
    # multiply by average household size
    merge['population'] = merge['population']*merge['B25010_001E'] 

    return merge

