
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[4]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    with open('university_towns.txt','r') as file:
        state = []
        town = []
        for l in file:
            nm = l.split("\n")[0]
            if nm.find('edit') > 0:
                st = nm.split('[')[0]
            else:
                t = nm.split(' (')[0]
                state.append(st)
                town.append(t)
        u_town = pd.DataFrame(list(zip(state,town)), columns=["State", "RegionName"] )
    return u_town
#get_list_of_university_towns()


# In[62]:

gdplev = pd.read_excel('gdplev.xls', skiprows=219, usecols=[4,5])
#gdplev = gdplev.loc[:,['Unnamed: 4','Unnamed: 5']]
gdplev.columns= ['YearQ','GDP']

#gdplev.head(100)


# In[48]:

gdplev.loc[gdplev.YearQ.str.find('2009')>=0,:]
for i in range(0, gdplev.shape[0] - 2):
    gdp1 = gdplev.loc[i,'GDP'] 
    gdp2 = gdplev.loc[i+1,'GDP']
    gdp3 = gdplev.loc[i+2, 'GDP']
    if (gdp1 > gdp2) & (gdp2 > gdp3):
        recession_start = gdplev.loc[i, 'YearQ']
        print(recession_start)
        break
for j in range(i+2, gdplev.shape[0]-2):
    gdp1 = gdplev.loc[j,'GDP'] 
    gdp2 = gdplev.loc[j+1,'GDP']
    gdp3 = gdplev.loc[j+2, 'GDP']
    if (gdp1 < gdp2) & (gdp2 < gdp3):
        recession_end = gdplev.loc[j+2, 'YearQ']
        print(recession_end)
        break


# In[60]:

gdplev.iloc[2:20].GDP.argmin()


# In[39]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdplev = pd.read_excel('gdplev.xls', skiprows=219, usecols=[4,5])
    gdplev.columns= ['YearQ','GDP']
    for i in range(0, gdplev.shape[0] - 2):
        gdp1 = gdplev.loc[i,'GDP'] 
        gdp2 = gdplev.loc[i+1,'GDP']
        gdp3 = gdplev.loc[i+2, 'GDP']
        if (gdp1 > gdp2) & (gdp2 > gdp3):
            recession_start = gdplev.loc[i, 'YearQ']
            break
    return recession_start
get_recession_start()


# In[47]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    gdplev = pd.read_excel('gdplev.xls', skiprows=219, usecols=[4,5])
    gdplev.columns= ['YearQ','GDP']
    for i in range(0, gdplev.shape[0] - 2):
        gdp1 = gdplev.loc[i,'GDP'] 
        gdp2 = gdplev.loc[i+1,'GDP']
        gdp3 = gdplev.loc[i+2, 'GDP']
        if (gdp1 > gdp2) & (gdp2 > gdp3):
            recession_start = gdplev.loc[i, 'YearQ']
            break
    for j in range(i+2, gdplev.shape[0]-2):
        gdp1 = gdplev.loc[j,'GDP'] 
        gdp2 = gdplev.loc[j+1,'GDP']
        gdp3 = gdplev.loc[j+2, 'GDP']
        if (gdp1 < gdp2) & (gdp2 < gdp3):
            recession_end = gdplev.loc[j+2, 'YearQ']
            break        
    return recession_end
get_recession_end()


# In[61]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    gdplev = pd.read_excel('gdplev.xls', skiprows=219, usecols=[4,5])
    gdplev.columns= ['YearQ','GDP']
    rstart = get_recession_start()
    rend = get_recession_end()
    i = gdplev.iloc[gdplev[gdplev['YearQ']==rstart].index[0] : gdplev[gdplev['YearQ']==rend].index[0]].GDP.argmin()   
    return gdplev.iloc[i].YearQ
get_recession_bottom()

 
# In[112]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing.State = housing.State.map(states)
    housing.drop(['RegionID','Metro','CountyName','SizeRank'], inplace=True, axis=1)
    housing.set_index(['State','RegionName'], inplace=True)
    housing = housing.iloc[:,45:]
    new_cols = [str(i)+'q'+str(j) for i in range(2000,2017) for j in range (1,5)]
    h_cols = housing.columns.tolist()
    q_cols = [h_cols[x:x+3] for x in range(0, len(h_cols),3)]
    for nc, qc in zip(new_cols[:len(q_cols)], q_cols):
        housing[nc] = housing.loc[:,qc].mean(axis=1)
    housing = housing[new_cols[:len(q_cols)]]
    return housing
convert_housing_data_to_quarters()


# In[164]:

 

# In[181]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    rstart = get_recession_start()
    rbottom = get_recession_bottom()
    u_towns = get_list_of_university_towns()
    u_towns = list(zip(u_towns.State,u_towns.RegionName))
    housing = convert_housing_data_to_quarters().loc[:,rstart:rbottom].copy()
    housing['pratio'] = housing.apply(lambda x: (x[rstart] - x[rbottom])/x[rstart], axis=1)
    housing['utown'] = [housing.index[i] in u_towns for i in range(0, housing.shape[0])]
    utown_pratio = housing.loc[housing.utown,'pratio'].dropna()
    non_utown_pratio = housing.loc[housing.utown == False, 'pratio'].dropna()
    pval = ttest_ind(utown_pratio,non_utown_pratio)[1]
    
    return (pval<0.01,pval,'university town' if utown_pratio.mean() < non_utown_pratio.mean() else 'non-university town')
run_ttest()


# In[ ]:



