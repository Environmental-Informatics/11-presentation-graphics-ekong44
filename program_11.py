#!/bin/env python
# Add your own header comments
#
"""
Template by Professor Cherkauer
Edited by Eric Kong on April 18th, 2020.

Description: This script builds on Assignment 10. The summary metric tables 
            that are outputted are used to generate figures for an oral presentation
            that will not need to be given. 
    
References:
"""
# Importing modules
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "agency_cd", "site_no", "Date", "Discharge", "Quality". The 
    "Date" column should be used as the DataFrame index. The pandas read_csv
    function will automatically replace missing values with np.NaN, but needs
    help identifying other flags used by the USGS to indicate no data is 
    availabiel.  Function returns the completed DataFrame, and a dictionary 
    designed to contain all missing value counts that is initialized with
    days missing between the first and last date of the file."""
    
    # define column names
    colNames = ['agency_cd', 'site_no', 'Date', 'Discharge', 'Quality']

    # open and read the file
    DataDF = pd.read_csv(fileName, header=1, names=colNames,  
                         delimiter=r"\s+",parse_dates=[2], comment='#',
                         na_values=['Eqp'])
    DataDF = DataDF.set_index('Date')
    
    # check for negative streamflow 
    DataDF.loc[~(DataDF['Discharge'] > 0), 'Discharge'] = np.nan
    
    # quantify the number of missing and negative values
    MissingValues = DataDF["Discharge"].isna().sum()   
    
    return( DataDF, MissingValues )

def ClipData( DataDF, startDate, endDate ):
    """This function clips the given time series dataframe to a given range 
    of dates. Function returns the clipped dataframe and and the number of 
    missing values."""
    
    # isolate the date range we want to work with
    DataDF = DataDF.loc[startDate:endDate] # start and end date defined in line 273
    MissingValues = DataDF["Discharge"].isna().sum() # quantify the number of missing values

    return( DataDF, MissingValues )
    
def ReadMetrics( newcsvfiles ):
    """This function takes a filename as input, and returns a dataframe with
    the metrics from the assignment on descriptive statistics and 
    environmental metrics.  Works for both annual and monthly metrics. 
    Date column should be used as the index for the new dataframe. Function 
    returns the completed DataFrame."""
    
    NewDF = pd.read_csv(newcsvfiles, header=0, delimiter=',', parse_dates=['Date'], comment='#', index_col=['Date']) 
    return( NewDF )

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.
    
if __name__ == '__main__':    

    # define full river names as a dictionary so that abbreviations are not used in figures
    riverName = { "Wildcat": "Wildcat Creek",
                  "Tippe": "Tippecanoe River" }
    
    # define filenames as a dictionary
    # NOTE - you could include more than just the filename in a dictionary, 
    # such as full name of the river or gaging site, units, etc. that would
    # be used later in the program, like when plotting the data.
    fileName = { "Wildcat": "WildcatCreek_Discharge_03335000_19540601-20200315.txt",
                 "Tippe": "TippecanoeRiver_Discharge_03331500_19431001-20200315.txt" }
    
    newcsvfiles = { "Annual": "Annual_Metrics.csv", "Monthly": "Monthly_Metrics.csv" }
    
    # define blank dictionaries (these will use the same keys as fileName)
    DataDF = {}
    MissingValues = {} 
    NewDF = {}
    
    # process input datasets
    for file in fileName.keys():
        DataDF[file], MissingValues[file] = ReadData(fileName[file])
        
        # clip to consistent period - last 5 years
        DataDF[file], MissingValues[file] = ClipData( DataDF[file], '2014-10-01', '2019-09-30' )
        
    for file in newcsvfiles.keys(): # using the same code structure to read in the Metrics
        NewDF[file] = ReadMetrics(newcsvfiles[file])
        
    
    # daily flow for both streams for the last 5 years of the record - Original TXT files
    
    
    # Annual coefficient of variation - Annual_metrics.csv
    
    
    # Annual TQMean - Annual_metrics.csv
    
    
    # Annual RB-Index - Annual_metrics.csv
    
    
    # Return period of annual peal flow events - 
 