""" 
This script creates a dataset that has the population estimate for each building in our buildings dataset. 
Authors: Jamie + Abhilash
"""
# Import libraries
import geopandas as gpd
import pandas as pd
from shapely import wkt

def get_population(geopandas_dataframe):
    ''' 
    geopandas_dataframe: The dataframe containing all building footprints
    
    returns:
    the same dataframe with a population column added
    '''

    # Read ACS data which contains information for population estimation
    population = pd.read_csv('../processed_data/ACSData.csv')

    # Allocate population based on number of units (random, needs to be changed later)
    res_buildings = geopandas_dataframe[geopandas_dataframe['class_reco'].str.contains('Residential')]
    
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
    
    # Recode missing to whatever the county average is
    # Obtained: https://data.census.gov/table?text=B25010_001E&g=0500000US42003&tid=ACSDT1Y2021.B25010
    merge.loc[merge['B25010_001E'].isna(), 'B25010_001E'] = 2.2
    
    # multiply by average household size
    merge['population'] = merge['population']*merge['B25010_001E'] 

    return merge

