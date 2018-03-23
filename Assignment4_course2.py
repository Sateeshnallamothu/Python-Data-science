import pandas as pd
from scipy import stats
import numpy as np
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
##
## https://fred.stlouisfed.org/series/SMS17140100000000001   download data from here for other cities. 


blm_df = pd.read_csv('c:\\Users\\SateeshSwathi\\Documents\\Python Scripts\\bloomington_nonfarm_employment.csv',
                     names=['Date','Employment'], skiprows=1)
peoria_df = pd.read_csv('c:\\Users\\SateeshSwathi\\Documents\\Python Scripts\\peoria_nonfarm_employment.csv',
                     names=['Date','Employment'], skiprows=1)
chicago_df = pd.read_csv('c:\\Users\\SateeshSwathi\\Documents\\Python Scripts\\chicago_nonfarm_employment.csv',
                     names=['Date','Employment'], skiprows=1)
champaign_df = pd.read_csv('c:\\Users\\SateeshSwathi\\Documents\\Python Scripts\\champaign_nonfarm_employment.csv',
                     names=['Date','Employment'], skiprows=1)
decator_df = pd.read_csv('c:\\Users\\SateeshSwathi\\Documents\\Python Scripts\\decator_nonfarm_employment.csv',
                     names=['Date','Employment'], skiprows=1)
il_df = pd.read_csv('c:\\Users\\SateeshSwathi\\Documents\\Python Scripts\\il_nonfarm_employment.csv',
                     names=['Date','Employment'], skiprows=1)

def aggregate_data(emp_df, city):
    """
    This function will create year column and aggreates the employement numbers by year
    """
    temp_df = emp_df.copy()
    temp_df['Year'] = [dt[:4] for dt in temp_df.Date]
    return round(temp_df.groupby('Year')['Employment'].mean(), 3)
 
blm_agg = aggregate_data(blm_df, 'Bloomington')
peoria_agg = aggregate_data(peoria_df, 'Peoria')
chicago_agg = aggregate_data(chicago_df, 'Chicago')
champaign_agg = aggregate_data(champaign_df, 'Champaign')
decator_agg = aggregate_data(decator_df, 'Decator')
il_agg = aggregate_data(il_df, 'Illinois')
final_df = pd.DataFrame({'Bloomington':blm_agg, 'Peoria':peoria_agg, 
                         'Decator': decator_agg, 'Champaign':champaign_agg })
chi_df = pd.DataFrame({'Chicago':chicago_agg})
                       # 'IL': il_agg/100})
fig, axs = plt.subplots(1,2, figsize=(12,12))
final_df.plot(kind='line', ax=axs[0], linewidth=3.0)
axs[0].set_title('Year to Year Nonfarm Job numbers in \n Illinois towns')
axs[0].set_ylabel('Thousands of Persons')
rows, cols = final_df.shape
for c in final_df.columns:
    axs[0].text(0,final_df[c][0] + .05, str(final_df[c][0]))
    axs[0].text(rows-1,final_df[c][rows-1] + .05, str(final_df[c][rows-1]))
chi_df.plot(kind='line', ax = axs[1], ylim=(4000,5000), linewidth=3.0)
rows, cols = chi_df.shape
for c in chi_df.columns:
    axs[1].text(0,chi_df[c][0] + .05, str(chi_df[c][0]))
    axs[1].text(rows-1,chi_df[c][rows-1] + .05, str(chi_df[c][rows-1]))
axs[1].set_title('Year to Year Nonfarm Job numbers in \n Chicago and its suburbs')
axs[1].set_ylabel('Thousands of Persons')
fig.suptitle('Hypothesis showing Nonfarm job gain in Metro Area and job loss in small towns \n over 10 year period in Illions, USA', 
             fontsize=14, fontweight='bold')
fig.savefig('C:\\Users\\SateeshSwathi\\Documents\\assignment4_course2.png')