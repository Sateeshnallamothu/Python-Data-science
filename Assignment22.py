
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/5cc2f3c0ffe2ed903495aee1bdeb47c948599be38e8c6a8e33c4382a.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Bloomington, Illinois, United States**, and the stations the data comes from are shown on the map below.

# In[5]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'5cc2f3c0ffe2ed903495aee1bdeb47c948599be38e8c6a8e33c4382a')


# In[6]:

get_ipython().magic('matplotlib notebook')


# In[7]:

noaa = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/5cc2f3c0ffe2ed903495aee1bdeb47c948599be38e8c6a8e33c4382a.csv')


# In[21]:

noaa.head(10)


# In[25]:

import numpy as np
leap_ix = np.where(noaa.Date.str.find('-02-29')>0)


# In[28]:

noaa.drop(noaa.index[leap_ix], inplace=True)


# In[41]:

from datetime import datetime


# In[ ]:

noaa['Year'] = noaa.Date.apply(lambda x:x[:4])
noaa['yday'] = noaa.Date.apply(lambda x:datetime.strptime(x, '%Y-%m-%d').timetuple().tm_yday)
 

# In[ ]:

noaa.head(20)


# In[38]:
 yr2015_tmax = pd.DataFrame(tmax.loc[tmax.Year=='2015',:].groupby('yday')['Data_Value'].max()/10)
yr2015_tmin = pd.DataFrame(tmin.loc[tmin.Year=='2015',:].groupby('yday')['Data_Value'].min()/10)

TMAX = tmax.loc[tmax.Year!='2015',:].groupby('yday')['Data_Value'].max()/10
TMIN = tmin.loc[tmin.Year!='2015',:].groupby('yday')['Data_Value'].min()/10
               
               TMAX = pd.DataFrame(TMAX[:-1])
TMIN = pd.DataFrame(TMIN[:-1])
yr2015_tmax['broken'] = yr2015_tmax.Data_Value > TMAX.Data_Value
yr2015_tmin['broken'] = yr2015_tmin.Data_Value < TMIN.Data_Value
yr2015max = yr2015_tmax.loc[yr2015_tmax.broken==True,'Data_Value']
yr2015min = yr2015_tmin.loc[yr2015_tmin.broken==True,'Data_Value']

plt.figure()
# plot the linear data and the exponential data
plt.plot(TMIN, '-o', label='Min')
plt.plot(TMAX, '-o', label='Max')
plt.scatter(yr2015min.index, yr2015min, color='m', s=60, marker='o', label='Record low achieved in 2015')
plt.scatter(yr2015max.index, yr2015max, color='k', s=60, marker='o', label='Record high achieved in 2015')
plt.xlabel('Day of Year')
plt.ylabel('Temparature(C)')
plt.title('Max and Min recorded temparature (day of year between 2005-14)')
plt.legend(loc='best')
# add a legend with legend entries (because we didn't have labels when we plotted the data series)
plt.legend(['Min', 'Max','2015 low','2015 high'])

# fill the area between the max data and min data
plt.gca().fill_between(range(len(TMIN)), 
                       TMIN.Data_Value, TMAX.Data_Value, 
                       facecolor='blue', 
                       alpha=0.25)
