# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:27:33 2020

@author: po63tol
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:51:35 2020

@author: po63tol
"""

"""
Created on Tue Jan  7 14:02:31 2020

@author: po63tol
"""

# this script plots the data according to the ISPRS paper layout

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.dates as mdates

os.chdir("D:/Paper/2020_ISPRS/Timeseries_zumplotten/NeueOrdnung/Pastures/")
list_csv = glob.glob('*.csv')
print(len(list_csv))

datapath_met = "D:/Paper/2020_ISPRS/Timeseries_zumplotten/Enddateien/"
files_meteo = os.listdir(datapath_met)

idx = pd.date_range('07-01-2016', '04-30-2019')

temp = pd.read_csv(datapath_met + files_meteo[0])
time = temp.iloc[:, 3]
temp = temp.iloc[:, 2]
precip = pd.read_csv(datapath_met + files_meteo[1])
precip = precip.iloc[:, 2]

s0 = pd.read_csv(list_csv[0])
s0['Date'] = pd.to_datetime(pd.Series(s0.iloc[:, 1]), dayfirst=True)
s0.index = pd.DatetimeIndex(s0.iloc[:, 3])
s0 = s0.reindex(idx)

df = pd.DataFrame(index=s0.index)
df['temp'] = temp.values
df['precip'] = precip.values

for i, file in enumerate(list_csv[:len(list_csv)]):
    s0_new = pd.read_csv(file)
    s0_new['Date'] = pd.to_datetime(pd.Series(s0_new.iloc[:, 1]), dayfirst=True)
    s0_new.index = pd.DatetimeIndex(s0_new.iloc[:, 3])
    s0_new = s0_new.reindex(idx)
    df[str(i)] = s0_new.iloc[:, 2]

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=2, top=1.5)
par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))

par1.axis["right"].toggle(all=True)
par2.axis["right"].toggle(all=True)

host.set_xlim(df.index.values[0], df.index.values[len(df.index.values) - 1])
host.set_ylim(-25, 1)

host.set_xlabel("Date")
host.set_ylabel("Backscatter [dB]")
par1.set_ylabel("Temperature [°C]")
par2.set_ylabel("Precipitation [mm]")

p1, = host.plot(df.index.values, df['0'].values, '.', color='tomato', label="Asc_VH")
p2, = host.plot(df.index.values, df['1'].values, '.', color='salmon', label="Asc_VV")
p3, = host.plot(df.index.values, df['2'].values, '.', color='blueviolet', label="Desc_VH/VV")
p4, = host.plot(df.index.values, df['3'].values, '.', color='forestgreen', label="Desc_VH")
p5, = host.plot(df.index.values, df['4'].values, '.', color='limegreen', label="Desc_VV")
p6, = par1.plot(df.index.values, df['temp'].values, color='peachpuff', label="Temperature")
p7, = par2.plot(df.index.values, df['precip'].values, color='skyblue', label="Precipitation")
p8, = host.plot(df.index.values, df['5'].values, '.', color='mediumslateblue', label="Desc_RVI")

par1.set_ylim(-10, 35)
par2.set_ylim(0, 10)

host.legend(loc='upper left', fontsize=14)

host.axis["left"].label.set_color('black')
par1.axis["right"].label.set_color('orange')
par2.axis["right"].label.set_color('dodgerblue')

host.axis["bottom"].label.set_fontsize(20)
host.axis["left"].label.set_fontsize(20)
par1.axis["right"].label.set_fontsize(20)
par2.axis["right"].label.set_fontsize(20)

host.axis["bottom"].major_ticklabels.set_fontsize(14)
host.axis["left"].major_ticklabels.set_fontsize(14)
par1.axis["right"].major_ticklabels.set_fontsize(14)
par2.axis["right"].major_ticklabels.set_fontsize(14)

host.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
host.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
host.xaxis.set_minor_locator(mdates.MonthLocator())

# plt.draw()
plt.title('Pastures', fontsize=20)
# plt.show()
plt.savefig('D:/Paper/2020_ISPRS/Timeseries_zumplotten/NeueOrdnung/Pastures/TimeSeries_RVI_VHVV.png', dpi=320,
            bbox_inches='tight')
