# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:57:00 2018

@author: SateeshSwathi
"""

import pandas as pd
import numpy as np
def answer_one():
     
    Energy = pd.read_excel('Energy Indicators.xls', skip_footer=True, skirows=1)
    #Energy = Energy[1:243]
    Energy.drop(['Unnamed: 0','Unnamed: 1'], inplace=True, axis=1)
    Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000
    Energy.loc[Energy['Country'] == '...','Country'] = np.NaN
    Energy['Country'] = Energy['Country'].str.replace('[0-9]','')                                                      
    country_replace = {
        "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "China, Macao Special Administrative Region": "Macao",
    "China, Hong Kong Special Administrative Region": "Hong Kong",
     "Switzerland17": "Switzerland",
    "Greenland7": "Greenland",
        "Spain16": "Spain",
        "Iran (Islamic Republic of)": "Iran",
        "France6": "France",
    "Bolivia (Plurinational State of)":"Bolivia",
         "Australia1": "Australia"
    } 
    Energy['Country'].replace(country_replace, inplace=True)
    #energy_df['Country'].dropna().head(50)
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    gdp_country_replace = {
        "Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
    }
    GDP['Country Name'].replace(gdp_country_replace, inplace=True)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    GDP.head()
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    df = pd.DataFrame.merge(ScimEn, Energy, on='Country')
    df = df.merge(GDP, on='Country')
    df = df[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 
             'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    df.sort_values('Rank', inplace=True)
    df = df[:15]
    df.set_index('Country', inplace=True)
    #df.head(20)
    #df.loc[df.Rank==3,:]
    #ScimEn.head(20)
    #GDP.head()
    return df
answer_one()
