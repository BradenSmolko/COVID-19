# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:59:36 2020

@author: brade

Fork the https://github.com/CSSEGISandData/COVID-19 repo and clone to your local
space. Set up this script in the same working directory. Can use the function to
aggregate columns of interest accross dates by iterating through each file.

columns include:
    - 
"""

import pandas as pd

def get_COVID_df(column_of_interest = 'Incident_Rate', dropna = False):
    '''
    

    Parameters
    ----------
    column_of_interest : String, optional
        The column of interest to aggregate from the daily reports.
        The default is 'Incident_Rate'.
        Other options include:
            - 'Confirmed'
            - 'Deaths'
            - 'Recovered'
            - 'Active'
            - 'People_Tested'
            - 'People_Hospitalized'
            - 'Mortality_Rate'
            
    dropna : Boolean, optional
        Drops States/Provinces that have rows with NaN values. The default is False.

    Returns
    -------
    df : Pandas DataFrame object
        The DataFrame object contains the column of interest from all dates and
        states/provinces.

    '''
    # Iterate over the files in the daily reports (US) folder and get the states 
    # and the column of interest. Add all of these dfs to a list to iterate over later.
    list_of_dfs = []
    import glob
    path = "csse_covid_19_data/csse_covid_19_daily_reports_us/*.csv"
    for file in glob.glob(path):
        df = pd.read_csv(file, header=0)
        df = df[['Province_State', column_of_interest]]
        file_date = file[50:60]
        df.set_index('Province_State', inplace = True)
        df.columns = [file_date]
        list_of_dfs.append(df)
    
    # Iterate over the dfs and join them on State/Province
    df = list_of_dfs[0]
    for dat in list_of_dfs[1:]:
        df = df.join(dat, on = 'Province_State')
    
    # If dropna is True, drop rows with NaN values
    if dropna:
        df = df.dropna()
    
    # Transpose the df and name index ('Date')
    df = df.transpose()
    df.index.name = 'Date'
    
    return df
