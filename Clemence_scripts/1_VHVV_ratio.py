# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:43:00 2020

@author: po63tol
"""

import pandas as pd
import glob
import os

# find all .csv files in the specified folder and count them
datapath = "D:/Paper/2020_ISPRS/Timeseries_zumplotten/Merge_Sammlung_Desc_VV/"
files = sorted(os.listdir(datapath))

os.chdir("D:/Paper/2020_ISPRS/Timeseries_zumplotten/Merge_Sammlung_Desc_VH/")
list_csv = glob.glob('*.csv')
print(len(list_csv))

# List = []

# Build VH/VV ratio for each patch and acquisition date; Calculate then the mean ratio (of all patches) per acquisition date

for i, file in enumerate(list_csv[:len(list_csv)]):
    df = pd.read_csv(file)
    filenamestart = file[:5]
    print(filenamestart)
    for file2 in files:  # enumerate(list_csv[:len(list_csv)]):
        if file2.startswith(filenamestart):
            df2 = pd.read_csv(datapath + file2)
            date_col = pd.DataFrame(df.iloc[:, 1])
            filter_col_df = [col for col in df if col.startswith('VH')]
            df_values = df[filter_col_df]
            filter_col_df2 = [col2 for col2 in df2 if col2.startswith('VV')]
            df2_values = df2[filter_col_df2]
            ratioVHVV = df_values - df2_values.values  # https://stackoverflow.com/questions/38415048/add-subtract-dataframes-with-different-column-labels # ratio is equal to differencing in dB
            ratioVHVV_mean = pd.DataFrame(ratioVHVV.mean(axis=1))
            df_new = date_col.join(ratioVHVV_mean)
            df_new.to_csv(r'D:/Paper/2020_ISPRS/Timeseries_zumplotten/Mean_Merge_Sammlung_Desc_VHVV/' + file + "VV.csv")
            # VH_col=pd.DataFrame(df.iloc[:,2])
            # VV_col=pd.DataFrame(df2.iloc[:,2])
            # ratioVHVV=VH_col/VV_col

        # df_mean=pd.DataFrame(df_values.mean(axis=1))

#   df2= pd.read_csv(file+1)
#    print(file)
#   print(file+1)

# for filename in file:
# if file.startswith(file[0:5]):
#      List.append(file)
# print (List)

#    df = pd.read_csv(file)
# print(file)
#    date_col=pd.DataFrame(df.iloc[:,1])
#    filter_col_df= [col for col in df if col.startswith('VH')]
#    df_values=df[filter_col_df]
#    df_mean=pd.DataFrame(df_values.mean(axis=1))
#    df_new=date_col.join(df_mean)
#    df_new.to_csv(r'D:/Paper/2020_ISPRS/Timeseries_zumplotten/Mean_Merge_Sammlung_Desc_VH/' + file + "_mean.csv")
