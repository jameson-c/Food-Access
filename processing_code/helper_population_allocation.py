""" 
This script creates a dataset that has the population estimate for each building in our buildings dataset. 

NOTE:
Currently, since I don't fully understand the mapping of geoids in ACS to geoids in buildings dataset, I am randomly allocating population, to create a pipeline. This needs to be modified soon. 

"""
# Import libraries
import geopandas as gpd
import pandas as pd

def get_population():

    # Get the dataset
    buildings_df = gpd.read_file('../processed_data/relevant_buildings.shp')

    # Allocate population based on number of units (random, needs to be changed later)
    res_buildings = buildings_df[buildings_df['class_reco'].str.contains('Residential')]


    def allocation_rule(input_string):

        if input_string == '1-Unit Residential':
            return 1
        elif input_string == '2-Unit Residential':
            return 2
        elif input_string == '3-Unit Residential':
            return 3
        elif input_string == '4+ Unit Residential':
            return 10
    

    res_buildings['population'] = res_buildings.apply(lambda row: allocation_rule(row['class_reco']), axis = 1)



    return res_buildings

