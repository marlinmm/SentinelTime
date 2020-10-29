# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 14:02:31 2020

@author: po63tol
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import glob
import os
from os.path import basename

os.chdir("D:/Paper/2020_ISPRS/Timeseries_zumplotten/")
list_csv = glob.glob('*.csv')
print(len(list_csv))

datapath_desc = "D:/Paper/2020_ISPRS/Timeseries_zumplotten/Mean_Merge_Sammlung_Desc_VV/"
files_desc = sorted(os.listdir(datapath_desc))

datapath_asc = "D:/Paper/2020_ISPRS/Timeseries_zumplotten/Mean_Merge_Sammlung_Asc_VV/"
files_asc = sorted(os.listdir(datapath_asc))
idx = pd.date_range('07-01-2016', '04-30-2019')

# Filter meteo data in order to get only values at acquisition dates. Build dailymean

for i, file in enumerate(list_csv[:len(list_csv)]):
    df = pd.read_csv(file, sep=';')
    files_desc_data = pd.read_csv(datapath_desc + files_desc[0])
    files_asc_data = pd.read_csv(datapath_asc + files_asc[0])
    df['Date'] = pd.to_datetime(pd.Series(df.iloc[:, 0]), format='%Y%m%d%H')
    files_desc_data['Date'] = pd.to_datetime(pd.Series(files_desc_data.iloc[:, 1]), dayfirst=True)
    files_asc_data['Date'] = pd.to_datetime(pd.Series(files_asc_data.iloc[:, 1]), dayfirst=True)
    df_daily_mean = df.set_index('Date').groupby(pd.TimeGrouper('1D')).mean()
    copy_files_desc_data = files_desc_data
    # copy_files_desc_data_series=copy_files_desc_data.iloc[:,3]
    copy_files_desc_data.index = pd.DatetimeIndex(copy_files_desc_data.iloc[:, 3])
    desc_series_final = copy_files_desc_data.reindex(idx)  # s.reindex(idx, fill_value=0)
    copy_files_asc_data = files_asc_data
    # copy_files_asc_data_series=copy_files_asc_data.iloc[:,3]
    copy_files_asc_data.index = pd.DatetimeIndex(copy_files_asc_data.iloc[:, 3])
    asc_series_final = copy_files_asc_data.reindex(idx)

    copy_df = df
    # copy_df_series=copy_df.iloc[:,2]
    copy_df.index = pd.DatetimeIndex(copy_df.iloc[:, 2])
    df_final = copy_df.reindex(idx)

    df_final.to_csv(r'D:/Paper/2020_ISPRS/Timeseries_zumplotten/Enddateien/' + file + "_dailymean.csv")
