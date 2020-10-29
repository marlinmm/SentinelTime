# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 08:39:59 2020

@author: po63tol
"""

import pandas as pd
import glob
import os

# find all .csv files in the specified folder and count them
os.chdir("D:/Paper/2020_ISPRS/Timeseries_zumplotten/Merge_Sammlung_Desc_VH/")
list_csv = glob.glob('*.csv')
print(len(list_csv))

# Build for each acquisition date the mean of the 20 patches

for i, file in enumerate(list_csv[:len(list_csv)]):
    df = pd.read_csv(file)
    # print(file)
    date_col = pd.DataFrame(df.iloc[:, 1])
    filter_col_df = [col for col in df if col.startswith('VH')]
    df_values = df[filter_col_df]
    df_mean = pd.DataFrame(df_values.mean(axis=1))
    df_new = date_col.join(df_mean)
    df_new.to_csv(r'D:/Paper/2020_ISPRS/Timeseries_zumplotten/Mean_Merge_Sammlung_Desc_VH/' + file + "_mean.csv")

# i=0
# for file in glob.glob("*.csv"):
#    i=i+1
#    print(file)


# data_path= "D:/Paper/2020_ISPRS/Timeseries_zumplotten/Merge_Sammlung_Asc_VH/"
# c311= "Broad-Leaved_Forest_Asc_VH.csv"
# with open(os.path.join(data_path, c311), "r") as f:
#    content = f.read()
# print(content)

# path= "D:/Paper/2020_ISPRS/Timeseries_zumplotten/Merge_Sammlung_Asc_VH/"
# extension = 'csv'
# list_csv = glob.glob('*.{}'.format(extension))
# folder_name = str(basename(path))
# print(len(list_csv))

# Einlesen der ersten csv-Datei
# data = pd.read_csv("Broad-Leaved_Forest_Asc_VH.csv")

# Schleife zur Extraktion der einzelnen Datenwerte aus den einzelnen
# csv-Dateien
# for i,file in enumerate(list_csv[:len(list_csv)-1]):
#    read = pd.read_csv(file)
#    print(file)
#    data["VV" + str(i)] = read["VV"].values
