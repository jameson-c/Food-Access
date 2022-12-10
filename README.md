# FoodAccess
A respository for a project attempting to optimize the location of a new food access point in Pittsburgh.
Report - https://docs.google.com/document/d/184_CkN6iypQQOGuoTpGk3ZHd0l7heHULW_OR4nTHVyA/edit?usp=sharing
Presentation - https://docs.google.com/presentation/d/1kGsfcFFK2ssEczBRGKjMudWvYdUN8B3zCjCe041ir9w/edit?usp=sharing

# TO_DO
1. put and upload input data 6 in drive folder
2. CLean up equity analysis
3. In equity analysis, change how food dessert data is being imported (use UDA, filter in code itself)

# Optimization models

## Baseline model
The purpose of creating a baseline is to understand what a decision maker would do without any optimization models. This can then be used to compare the performance of other optimization models. In this project, the baseline is defined as follows:
Choose the census tract that has highest number of people experiencing food insecurity as per USDA. Pick a random commercial building in that census tract, place a grocery store there. 

## Model 1
This model maximizes the marginal access (i.e. # of new people who would gain access) gained by placing n grocery stores. This model does a sequential search for optimum locations and places n stores in greedy way. 

## Model 2
This model minimizes the weighted distance of residential buildings to grocery stores in pittsburgh. The aim of this model is to simultaneously place n stores in such a way that the total weighted distance (weight being defined by population) of every residential building to it's closest grocery store is minimized. 

# Data structure

## Input data (contains the raw data downloaded directly from sources)
1. 2010_Census_Tracts.* - Shapefiles for census tracts in Pittsburgh
2. allegheny_county_building_footprint_locations.geojson - Building footprints for all buildings in Allegheny County
3. Zoning.* - Zoning information for Pittsburgh. This is a shapefile. 
4. Allegheny_county_assets.csv - Allegheny county asset information including location data on supermarkets, food banks and WIC vendors. 
5. usda_lowincomelowaccess.csv - Dataset that identifies which census tracts are low income low access to food as defined by USDA
6. Demographics_Combined_Updated.csv - Demographic information of interest for equity analysis


## Processed data (contains processed data, generated using code)
1. pittsburgh_footprint.shp - Building footprints in pittsburgh. Is a spatial join between 1 and 2 from Input data. Created in 1- Filter footprints for Pittsburgh.ipynb
2. relevant_buildings.* - Uses 2, 3 and 4 from Input data to create building footprints and categories for all residential, commercial and grocery stores in Pittsburgh. Created in 2- Generate spatial dataset.ipynb
3. ACSData.csv - Census tract demographic information. Sourced using API in 3- getPopulation.py
4. res_comm_distance_matrix.npy - Pairwise Haversine distance (in miles) between all residential buildings and commercial buildings. Code to generate is in modelling code files (4- Baseline model.ipynb, 5- Model 1.ipynb). It is saved into the processed data folder because of large size (5.5 GB). 
5. new_store_ids.csv - additional optimized store details chosen by model 1
6. new_store_ids_assuming_no_existing_access.csv - optimized store details assuming no existing grocery stores, chosen by model 1

# Code structure
To run the entire pipeline, please consider the prefix number for each file as the order in which it should be run. 

## Files whose outputs are provided in the dataset (processed data) and need not be run (pre processing). 

1. 1- Filter footprints for Pittsburgh.ipynb - Performs a spatial join between 1 and 2 from Input data to get building footprints for Pittsburgh
2. 2- Generate spatial dataset.ipynb - Uses 2-4 from Input data as well as output from code file 1 to create and clean building footprints and categories for all residential, commercial and grocery stores in Pittsburgh. 
3. 3- getPopulation.py - Sources population information from ACS dataset

## Files which need to be run (modelling and analysis)
4. 4- Baseline mode.ipynb - Creates and analyzes the baseline model's result
5. 5- Model 1.ipynb - Creates and analyzes model 1's results
6. 6- Model 2.ipynb - Creates and analyzes model 2's results
7. 7- Equity Analysis.ipynb - Analyzing the fairness of optimization algorithm
8. 8- Visualize Results.ipynb - Visualizing the outputs of all the models

## Helper files 
1. helper_distance_calculation.py - Calculates haversine distance between any geo-coordinates
2. helper_population_allocation.py - Estimates population at each residential building

# How to implement the pipeline

- Clone this repository
- `pip install -r requirements.txt`
- Download dataset from this google drive link and place it inside your local repo folder. Please don't change the folder name or structure.
- Run files in order as mentioned in code structure
    - If you download the entire dataset from google drive, then code files 1,2 and 3 need not be run. 
    - Irrespective of this, the input data needs to be downloaded and present in the local repo folder. 

# Other notes?