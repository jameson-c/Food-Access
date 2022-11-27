''' 
This script creates a function that can calculate haversine distance between any 2 building footprints. These functions are intended
to generate the following parameters:

- A binary variable indicating whether an existing building has access to a grocery store
- A binary variable indicating whether a given residential building and commercial building pair are within each other's access limits

'''

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import haversine as hs

def get_geocoordinate(geopandas_dataframe, polygon_column):
    """ 
    Get's the geo-coordinates of the centroid of a building footprint polygon

    Parameters
    ----------
    geopandas_dataframe: A dataframe containing the footprint shapefiles
    polygon_column: A string indicating the column name containing the polygons

    Returns
    -------
    geopandas_dataframe: The same as input dataset, with a new column containing lat-long of polygon centroids
    """

    # Project to CRS
    geopandas_dataframe[polygon_column] = geopandas_dataframe[polygon_column].to_crs(epsg=3035)

    # Convert to centroids
    geopandas_dataframe['centroids'] = geopandas_dataframe[polygon_column].centroid.to_crs(4326)
        
    # Get the geocoordinates
    geopandas_dataframe['coordinates'] = geopandas_dataframe.apply(lambda row: (row['centroids'].x, row['centroids'].y), axis = 1)

    return geopandas_dataframe


def calculate_access(geopandas_dataframe, building_type_1, building_type_2, identifier_column, geo_column, output_format, access_distance=1):
    """ 
    Calculate whether 2 entities are within the access_distance of each other

    Parameters
    ----------
    geopandas_dataframe: A dataframe containing the footprint shapefiles
    building_type_1: Building 1 type ('Residential', 'commercial', 'Grocery Store')
    building_type_2: Building 2 type ('Residential', 'commercial', 'Grocery Store)
    identifier_column: A string indicating the column name containing the building type
    geo_column: A string indicating the column name containing geographic information for that building (either the polygon or coordinates)
    output_format: ('dataframe', 'matrix') - Whether the output should be a dataframe, each row containing a unique building_type_1, building_type_2 
                   or should it be a matrix
    access_distance (int): Miles defining the access parameter (default=1) 


    Returns
    -------
    A dataframe or a matrix containing a binary access variable
    """

    # Filter the dataset to keep the 2 relevant building types
    building_1_df = geopandas_dataframe[geopandas_dataframe[identifier_column].str.contains(building_type_1)]
    building_2_df = geopandas_dataframe[geopandas_dataframe[identifier_column].str.contains(building_type_2)]

    # Get centroid coordinates for each building
    building_1_df = get_geocoordinate(building_1_df, geo_column)
    building_2_df = get_geocoordinate(building_2_df, geo_column)

    # Calculate distance
    if output_format == 'dataframe':
        print('modified script')
        # Rename columns for cross joining
        building_1_df = building_1_df[['geoid10', 'tractce10', 'coordinates', 'building_id']]
        building_1_df.rename(columns={'coordinates': building_type_1 + "_coordinates", 'geoid10': "geoid_" + building_type_1, 'tractce10':"tract_id_" + building_type_1, 'building_id': 'building_id' + building_type_1},inplace=True)

        building_2_df = building_2_df[['geoid10', 'tractce10', 'coordinates', 'building_id']]
        building_2_df.rename(columns={'coordinates': building_type_2 + "_coordinates", 'geoid10': "geoid_" + building_type_2, 'tractce10':"tract_id_" + building_type_2, 'building_id': 'building_id' + building_type_2},inplace=True)

        # Cross join the 2 files
        building_1_df['key'] = 1
        building_2_df['key'] = 1
        
        df_cross_joined = pd.merge(building_1_df, building_2_df, on ='key').drop("key", 1)

        # Calculate haversine distance
        df_cross_joined['distance'] = df_cross_joined.apply(lambda row: hs.haversine(row[building_type_1 + "_coordinates"], row[building_type_2 + "_coordinates"], unit=hs.Unit.MILES), axis = 1)

        df_cross_joined['access'] = df_cross_joined.apply(lambda row: 1 if row['distance'] <= 1 else 0, axis=1)

    # TO DO: If output_format = 'matrix'




    return df_cross_joined