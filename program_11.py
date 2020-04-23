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
monthlycolumnheader = ['Discharge'];

# Importing modules
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams

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

def GetMonthlyStatistics( stripped_monthly ):
    """This function calculates monthly descriptive statistics and metrics 
    for the given streamflow time series. Values are returned as a dataframe
    of monthly values for each year."""
    
    # combination of GetMonthlyAverages and GetMonthlyStatistics from assignment 10
    # take the clipped data and resample it. Group by month 

    monthly_index = stripped_monthly.resample('MS').mean() # resample index - monthly
    MoDataDF = pd.DataFrame(index = monthly_index.index, columns = monthlycolumnheader) # setting new DF with proper index and headers
    MDF = stripped_monthly.resample('MS') # resampled DF stored as a simple variable name 
    
    #metrics and statistics 
    MoDataDF['Discharge'] = MDF['Discharge'].mean()
    
    isolated_months = MoDataDF.index.month # tip for extracting month from Cherkauer
    MoDataDF = MoDataDF.groupby(isolated_months).mean() # group the new DF using the months and find the mean of that data

    return ( MoDataDF )

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
        DataDF[file], MissingValues[file] = ClipData( DataDF[file], '1969-10-01', '2019-09-30' )
        
######### daily flow for both streams for the last 5 years of the record - Original TXT files ###############
        plt.plot(DataDF[file]['2014-10-01':'2019-09-30']['Discharge'], label=riverName[file]) # indent so the code runs for both data sets 
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Discharge (cfs)')
    plt.title('Daily Flow of Wildcat Creek and Tippecanoe River - Last 5 Years')
    rcParams['figure.figsize'] = 7, 5 # figure size in inches (width, height)
    plt.savefig('DailyFlow.png', dpi = 96)
    plt.close()    
  
########### reading in the metrics data sets################################################################
      
    for newfile in newcsvfiles.keys(): # using the same code structure to read in the Metrics
        NewDF[newfile] = ReadMetrics(newcsvfiles[newfile])
          
    # isolate the data by station name 
    tippe = NewDF['Annual'].loc[NewDF['Annual']['Station']=='Tippe']
    wildcat = NewDF['Annual'].loc[NewDF['Annual']['Station']=='Wildcat']
    
    # plotting Annual coefficient of variation - Annual_metrics.csv
    # date range 50 years
    plt.plot(tippe['Coeff Var'],'ko')
    plt.plot(wildcat['Coeff Var'],'ro')  
    plt.legend([riverName['Wildcat'],riverName['Tippe']], loc='upper left')
    plt.xlabel('Date', fontsize = 14)
    plt.ylabel('Coefficient of Variation (unitless)', fontsize = 14)
    plt.title('Coefficient of Variation of Flow', fontsize = 14)
    rcParams['figure.figsize'] = 7, 5 # figure size in inches (width, height)
    plt.savefig('Coeff_Var.png', dpi = 96)
    plt.close()  
    
    # plotting Annual TQMean - Annual_metrics.csv
    plt.plot(tippe['Tqmean'],'ko')
    plt.plot(wildcat['Tqmean'],'ro')   
    plt.legend([riverName['Tippe'],riverName['Wildcat']], loc='best')
    plt.xlabel('Date', fontsize = 14)
    plt.ylabel('Time (Days)', fontsize = 14)
    plt.title('Fraction of Days that Flow Exceeds Mean Annual Flow \n(T-Q Mean)', fontsize = 14)
    rcParams['figure.figsize'] = 7, 5 # figure size in inches (width, height)
    plt.savefig('Tqmean.png', dpi = 96)
    plt.close()  
    
    # plotting Annual RB-Index - Annual_metrics.csv
    plt.plot(tippe['R-B Index'],'ko')
    plt.plot(wildcat['R-B Index'],'ro')   
    plt.legend([riverName['Wildcat'],riverName['Tippe']], loc='best')
    plt.xlabel('Date', fontsize = 14)
    plt.ylabel('R-B Index (cfs/cfs)', fontsize = 14)
    plt.title('Richards-Baker Flashiness Index \n(R-B Index)', fontsize = 14)
    rcParams['figure.figsize'] = 7, 5 # figure size in inches (width, height)
    plt.savefig('RBindex.png', dpi = 96)
    plt.close()    
    
#    # plotting average annual monthly flow 
    raw_tippe = DataDF['Tippe']['Discharge'].to_frame() # use function to process them
    raw_wild = DataDF['Wildcat']['Discharge'].to_frame()
    
    process_t = GetMonthlyStatistics(raw_tippe)
    process_w = GetMonthlyStatistics(raw_wild)
#    
#    # same values as the MonthlyAverages dict/DF in assignment 10
    plt.plot(process_w['Discharge'],'ko')
    plt.plot(process_t['Discharge'],'ro')   
    plt.legend([riverName['Wildcat'],riverName['Tippe']], loc='best')
    plt.xlabel('Month', fontsize = 14)
    plt.xticks(np.arange(1, 13, 1)) # show all months on axis
    plt.ylabel('Discharge (cfs)', fontsize = 14)
    plt.title('Average Annual Monthly Flow', fontsize = 14)
    rcParams['figure.figsize'] = 7, 5 # figure size in inches (width, height)
    plt.savefig('Avg_Annual_Flow.png', dpi = 96)
    plt.close()         
    
    
    # Return period of annual peal flow events - 
    sort_wild = wildcat.sort_values('Peak Flow', ascending = False) # sort annual wildcat data with highest at the top 
    sort_tippe = tippe.sort_values('Peak Flow', ascending = False) # sort annual tippe data with highest at the top 
    
    sort_wild['Rank'] = np.arange(1,51,1) # highest flow is rank one 
    sort_tippe['Rank'] = np.arange(1,51,1)
    
    sort_tippe['exceed_prob'] = sort_tippe['Rank'] / 51 # plotting positions is equal to rank divided by 51 observations 
    sort_wild['exceed_prob'] = sort_wild['Rank'] / 51
    
    plt.plot(sort_wild['exceed_prob'], sort_wild['Peak Flow'], 'ko')
    plt.plot(sort_tippe['exceed_prob'], sort_tippe['Peak Flow'], 'ro')   
    plt.legend([riverName['Wildcat'],riverName['Tippe']], loc='best')
    plt.xlabel('Exceedence Probability', fontsize = 14)
    plt.xlim(1,0) # flip x-axis
    plt.ylabel('Peak Discharge (cfs)', fontsize = 14)
    plt.title('Return Period of Annual Peak Flow Events', fontsize = 14)
    rcParams['figure.figsize'] = 7, 5 # figure size in inches (width, height)
    plt.savefig('Period_Peak.png', dpi = 96)
    plt.close()     