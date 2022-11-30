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


# def calculate_access(geopandas_dataframe, building_type_1, building_type_2, identifier_column, geo_column, output_format, access_distance=1):
def calculate_access(res_location_array, comm_location_array):

    """ 
    Create a distance matrix and an access matrix between 2 arrays of coordinates

    Parameters
    ----------
    res_location_array: An array containing coordinates of all residential building locatons
    comm_location_array: An array containing coordinates of all commercial building locatons

    Returns
    -------
    A matrix of distances and access binaries
    """


    def distance_function(res_coordinate, comm_coordinate):
        return hs.haversine(res_coordinate, comm_coordinate, unit=hs.Unit.MILES)

    fv = np.vectorize(distance_function)

    distance_matrix = fv(res_location_array[:, np.newaxis], comm_location_array)

    def func(distance):
        if distance <=1:
            return 1
        else:
            return 0


    access_matrix = np.vectorize(func)(distance_matrix)

    return distance_matrix, access_matrix