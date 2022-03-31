#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:28:38 2020

@author: ryanoreilly
####################
Diff between version 4 and 5 are the file locations and dACV6 instead of dACV7. dACV6 is the latest version
####################
The objective of this file is to:
    1) Expand data set to represent hourly energy consumption
    2) create time stamp
    3) cast into IAMC format
    4) test 

Example from: https://github.com/openENTRANCE/nomenclature/commit/7591988c8d41dec8a0f2252a711de838beb168e7

| **model**   | **scenario**        | **region** | **variable**   | **unit** | **subannual**     | **2015** | **2020** | **2025** |
|-------------|---------------------|------------|----------------|----------|-------------------|---------:|---------:|---------:|
| GENeSYS-MOD | Societal Commitment | Europe     | Primary Energy | GJ/y     | 01-01 00:00+01:00 |     7.99 |     7.50 |      ... |
| ...         | ...                 | ...        | ...            | ...      | ...               |      ... |      ... |      ... |

| **model**   | **scenario**        | **region** | **variable**   | **unit** | **subannual**     | **2015** | **2020** | **2025** |
|-------------|---------------------|------------|----------------|----------|-------------------|---------:|---------:|---------:|
| GENeSYS-MOD | Societal Commitment | Europe     | Primary Energy | GJ/y     | 01-01 00:00+01:00 |     7.99 |     7.50 |      ... |
| ...         | ...                 | ...        | ...            | ...      | ...               |      ... |      ... |      ... |

previous: 

    TF_CS1_BE1-Theoretical
    TF_CS1_BE2-Centrally planned
new:    
    TF_CS1_BE1-Full
    TF_CS1_BE2-Realistic
    NEW VERSION V2: updated versions of P_WM, P_DW, and P_TD are used; V2
"""

### BEGIN - global options ###
## Import packages
import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os
from smtplib import SMTP_SSL ## for sending emails
#pip install pyam-iamc
import pyam
from pyam import IamDataFrame
#pip install git+https://github.com/openENTRANCE/nomenclature
#import nomenclature
import pint #pyam dependency
#import matplotlib #pyam dependency
#import seaborn #pyam dependency
#import six #pyam dependency
#import requests # for API
### Set options
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/')

# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
### END - global options
### Load in data
d_WM = pd.read_csv('./d_WMV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_WH = pd.read_csv('./d_WHV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_TD = pd.read_csv('./d_TDV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_SH = pd.read_csv('./d_SHV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_RF = pd.read_csv('./d_RFV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_FR = pd.read_csv('./d_FRV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_EV = pd.read_csv('./d_EVV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_EVfit55 = pd.read_csv('./d_EVV6_fit55.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_DW = pd.read_csv('./d_DWV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_AC = pd.read_csv('./d_ACV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_HP = pd.read_csv('./d_HPV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_CP = pd.read_csv('./d_CPV5.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#

p_WM = pd.read_csv('./p_WMV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_WH = pd.read_csv('./p_WHV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_SH = pd.read_csv('./p_SHV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_EV = pd.read_csv('./p_EVV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_EVfit55 = pd.read_csv('./p_EVV6_fit55.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_DW = pd.read_csv('./p_DWV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_AC = pd.read_csv('./p_ACV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_TD = pd.read_csv('./p_TDV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_RF = pd.read_csv('./p_RFV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_FR = pd.read_csv('./p_FRV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_CP = pd.read_csv('./p_CPV5.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_HP = pd.read_csv('./p_HP.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#

# sort all dataframes
d_WM = d_WM.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_WH = d_WH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_TD = d_TD.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_SH = d_SH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_RF = d_RF.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_FR = d_FR.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_EV = d_EV.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_EVfit55 = d_EVfit55.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_DW = d_DW.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_AC = d_AC.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_CP = d_CP.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_HP = d_HP.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)


p_WM = p_WM.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_WH = p_WH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_SH = p_SH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_EV = p_EV.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_EVfit55 = p_EVfit55.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_DW = p_DW.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_AC = p_AC.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_TD = p_TD.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_RF = p_RF.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_FR = p_FR.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_CP = p_CP.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_HP = p_HP.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)

# p_Device = P_device - d_device; the electricity available in hour t = maximum dispatchable load - hourly demand
p_WM = p_WM.iloc[0:p_WM.shape[0],1:34]-d_WM.iloc[0:d_WM.shape[0],1:34] # WM
p_WH = p_WH.iloc[0:p_WH.shape[0],1:34]-d_WH.iloc[0:d_WH.shape[0],1:34] # WH
p_SH = p_SH.iloc[0:p_SH.shape[0],1:34]-d_SH.iloc[0:d_SH.shape[0],1:34] # SH
p_EV = p_EV.iloc[0:p_EV.shape[0],1:34]-d_EV.iloc[0:d_EV.shape[0],1:34] # EV
p_EVfit55 = p_EVfit55.iloc[0:p_EVfit55.shape[0],1:34]-d_EVfit55.iloc[0:d_EVfit55.shape[0],1:34] # EV
p_DW = p_DW.iloc[0:p_DW.shape[0],1:34]-d_DW.iloc[0:d_DW.shape[0],1:34] # DW
p_AC = p_AC.iloc[0:p_AC.shape[0],1:34]-d_AC.iloc[0:d_AC.shape[0],1:34] # AC
p_TD = p_TD.iloc[0:p_TD.shape[0],1:34]-d_TD.iloc[0:d_TD.shape[0],1:34] # TD
p_RF = p_RF.iloc[0:p_RF.shape[0],1:34]-d_RF.iloc[0:d_RF.shape[0],1:34] # RF
p_FR = p_FR.iloc[0:p_FR.shape[0],1:34]-d_FR.iloc[0:d_FR.shape[0],1:34] # FR
p_CP = p_CP.iloc[0:p_CP.shape[0],1:34]-d_CP.iloc[0:d_CP.shape[0],1:34] # CP
p_HP = p_HP.iloc[0:p_HP.shape[0],1:34]-d_HP.iloc[0:d_HP.shape[0],1:34] # HP

p_WM['country'] = d_WM['country']
p_WH['country'] = d_WH['country']
p_SH['country'] = d_SH['country']
p_EV['country'] = d_EV['country']
p_EVfit55['country'] = d_EVfit55['country']
p_DW['country'] = d_DW['country']
p_AC['country'] = d_AC['country']
p_TD['country'] = d_TD['country']
p_RF['country'] = d_RF['country']
p_FR['country'] = d_FR['country']
p_CP['country'] = d_CP['country']
p_HP['country'] = d_HP['country']

for year in range(2018-2018,2050+1-2018):
    yr = p_EVfit55.columns[year]
    d_neg = p_EVfit55[p_EVfit55[yr]<0]
    print(yr,len(d_neg))

# WASHING MACHINE WILL BE USED AS TEMPLATE 
# WASHING MACHINE DEMENAD
d_WM['unit']      = 'MW'
d_WM['model']     = 'Flexibilities 2.2'
d_WM['scenario']  = 'TF_CS1_BE1-Full'
d_WM['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Washing Machine'
d_WM['region']    = d_WM['nutscode']
# CREATION OF TIMESTAMP/ SUBANNUAL
#month
d_WM['month'] = ""
d_WM['h'] = ""
for i in range(0,d_WM.shape[0]):
    print(i)
    d_WM['month'][i] = d_WM['TIME'].loc[i][5:7]
    d_WM['h'][i] = "%.2d" % d_WM['hour'][i]
    
# create timestamp to be used for all dfs since they are all in the same format
d_WM['subannual'] = (d_WM['month']+'-'+'01'+' '+d_WM['h']+':00+01:00')

timestamp = list(d_WM['subannual'])

d_WM=d_WM.drop(['hour','nutscode','TIME','h','month','Unnamed: 0'],axis=1) # remove redundant variable
nutscode = d_WM['region']
# WASHING MACHINE PINCREASE
p_WM['unit']      = 'MW'
p_WM['model']     = 'Flexibilities 2.2'
p_WM['scenario']  = 'TF_CS1_BE1-Full'
p_WM['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Washing Machine'
p_WM['region']    = nutscode
p_WM['subannual'] = timestamp


# WATER HEATER DEMAND
d_WH['unit']      = 'MW'
d_WH['model']     = 'Flexibilities 2.2'
d_WH['scenario']  = 'TF_CS1_BE1-Full'
d_WH['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Water Heater'
d_WH['region']    =  nutscode
d_WH['subannual'] = timestamp

d_WH=d_WH.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# WATER HEATER PINCREASE
p_WH['unit']      = 'MW'
p_WH['model']     = 'Flexibilities 2.2'
p_WH['scenario']  = 'TF_CS1_BE1-Full'
p_WH['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Water Heater'
p_WH['region']    = nutscode
p_WH['subannual'] = timestamp



# TUMBLE DRIER DEMAND
d_TD['unit']      = 'MW'
d_TD['model']     = 'Flexibilities 2.2'
d_TD['scenario']  = 'TF_CS1_BE1-Full'
d_TD['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dryer'
d_TD['region']    = nutscode
d_TD['subannual'] = timestamp


d_TD=d_TD.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# TUMBLE DRIER PINCREASE
p_TD['unit']      = 'MW'
p_TD['model']     = 'Flexibilities 2.2'
p_TD['scenario']  = 'TF_CS1_BE1-Full'
p_TD['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dryer'
p_TD['region']    = nutscode
p_TD['subannual'] = timestamp


# STORAGE HEATER DEMAND

d_SH['unit']      = 'MW'
d_SH['model']     = 'Flexibilities 2.2'
d_SH['scenario']  = 'TF_CS1_BE1-Full'
d_SH['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Storage Heater'
d_SH['region']    = nutscode
d_SH['subannual'] = timestamp


d_SH=d_SH.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable


# STORAGE HEATER PINCREASE
p_SH['unit']      = 'MW'
p_SH['model']     = 'Flexibilities 2.2'
p_SH['scenario']  = 'TF_CS1_BE1-Full'
p_SH['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Storage Heater'
p_SH['region']    = nutscode
p_SH['subannual'] = timestamp


# Combine refrigerator and Freezer
# REFRIGERATOR/FREEZER DEMAND
d_RF=d_RF.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable
d_RF=d_FR.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable
d_RF_FR = d_RF+d_FR

d_RF_FR['country'] = d_RF['country']

d_RF_FR['unit']      = 'MW'
d_RF_FR['model']     = 'Flexibilities 2.2'
d_RF_FR['scenario']  = 'TF_CS1_BE1-Full'
d_RF_FR['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Refrigeration'
d_RF_FR['region']    = nutscode
d_RF_FR['subannual'] = timestamp

d_RF_FR=d_RF_FR.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable
del d_RF
del d_FR
# REFRIGERATOR/FREEZER PINCREASE
p_RF_FR = p_RF+p_FR
p_RF_FR['country'] = p_RF['country']
p_RF_FR['unit']      = 'MW'
p_RF_FR['model']     = 'Flexibilities 2.2'
p_RF_FR['scenario']  = 'TF_CS1_BE1-Full'
p_RF_FR['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Refrigeration'
p_RF_FR['region']    = nutscode
p_RF_FR['subannual'] = timestamp
del p_RF
del p_FR

# ELECTRIC VEHICLE DEMAND
d_EV['unit']      = 'MW'
d_EV['model']     = 'Flexibilities 2.2'
d_EV['scenario']  = 'TF_CS1_BE1-Full'
d_EV['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Electric Vehicle'
d_EV['region']    = nutscode
d_EV['subannual'] = timestamp


d_EV=d_EV.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable


# ELECTRIC VEHICLE PINCREASE
p_EV['unit']      = 'MW'
p_EV['model']     = 'Flexibilities 2.2'
p_EV['scenario']  = 'TF_CS1_BE1-Full'
p_EV['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Electric Vehicle'
p_EV['region']    = nutscode
p_EV['subannual'] = timestamp

# ELECTRIC VEHICLE DEMAND - fit55
d_EVfit55['unit']      = 'MW'
d_EVfit55['model']     = 'Flexibilities 2.2'
d_EVfit55['scenario']  = 'TF_CS1_BE1-Full'
d_EVfit55['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Electric Vehicle_55'
d_EVfit55['region']    = nutscode
d_EVfit55['subannual'] = timestamp


d_EVfit55=d_EVfit55.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# ELECTRIC VEHICLE PINCREASE - fit55
p_EVfit55['unit']      = 'MW'
p_EVfit55['model']     = 'Flexibilities 2.2'
p_EVfit55['scenario']  = 'TF_CS1_BE1-Full'
p_EVfit55['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Electric Vehicle_55'
p_EVfit55['region']    = nutscode
p_EVfit55['subannual'] = timestamp


# DISH WASHER DEMAND
d_DW['unit']      = 'MW'
d_DW['model']     = 'Flexibilities 2.2'
d_DW['scenario']  = 'TF_CS1_BE1-Full'
d_DW['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dish Washer'
d_DW['region']    = nutscode
d_DW['subannual'] = timestamp


d_DW=d_DW.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# DISH WASHER PINCREASE
p_DW['unit']      = 'MW'
p_DW['model']     = 'Flexibilities 2.2'
p_DW['scenario']  = 'TF_CS1_BE1-Full'
p_DW['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dish Washer'
p_DW['region']    = nutscode
p_DW['subannual'] = timestamp



# AIR CONDITIONING DEMAND
d_AC['unit']      = 'MW'
d_AC['model']     = 'Flexibilities 2.2'
d_AC['scenario']  = 'TF_CS1_BE1-Full'
d_AC['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Air Conditioning'
d_AC['region']    = nutscode
d_AC['subannual'] = timestamp


d_AC=d_AC.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# AIR CONDITIONING PINCREASE
p_AC['unit']      = 'MW'
p_AC['model']     = 'Flexibilities 2.2'
p_AC['scenario']  = 'TF_CS1_BE1-Full'
p_AC['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Air Conditioning'
p_AC['region']    = nutscode
p_AC['subannual'] = timestamp

# FRY5 has NAs for d_EV and p_EV; need to remove in order to validate dataframe

d_EVfit55 = d_EVfit55.dropna()
p_EVfit55 = p_EVfit55.dropna()
d_EV = d_EV.dropna()
p_EV = p_EV.dropna()

# CIRCULATION PUMP DEMAND
d_CP['unit']      = 'MW'
d_CP['model']     = 'Flexibilities 2.2'
d_CP['scenario']  = 'TF_CS1_BE1-Full'
d_CP['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Circulation Pump'
d_CP['region']    = nutscode
d_CP['subannual'] = timestamp


d_CP=d_CP.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# CIRCULATION PUMP PINCREASE
p_CP['unit']      = 'MW'
p_CP['model']     = 'Flexibilities 2.2'
p_CP['scenario']  = 'TF_CS1_BE1-Full'
p_CP['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Circulation Pump'
p_CP['region']    = nutscode
p_CP['subannual'] = timestamp


# Heat Pump demand
d_HP['unit']      = 'MW'
d_HP['model']     = 'Flexibilities 2.2'
d_HP['scenario']  = 'TF_CS1_BE1-Full'
d_HP['variable']  = 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Heat Pump'
d_HP['region']    = nutscode
d_HP['subannual'] = timestamp


d_HP = d_HP.drop(['hour','nutscode','TIME','Unnamed: 0'],axis=1) # remove redundant variable

# Heat PUMP PINCREASE
p_HP['unit']      = 'MW'
p_HP['model']     = 'Flexibilities 2.2'
p_HP['scenario']  = 'TF_CS1_BE1-Full'
p_HP['variable']  = 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Heat Pump'
p_HP['region']    = nutscode
p_HP['subannual'] = timestamp





final  = d_AC.append(p_AC,ignore_index=True) # AC can only be delayed not advanced
final = final.append(d_DW,ignore_index=True)
final = final.append(p_DW,ignore_index=True)
final = final.append(d_EV,ignore_index=True)
final = final.append(p_EV,ignore_index=True) # can only be delayed
final = final.append(d_EVfit55,ignore_index=True)  # can only be delayed
final = final.append(p_EVfit55,ignore_index=True)
final = final.append(d_RF_FR,ignore_index=True)
final = final.append(p_RF_FR,ignore_index=True)
final = final.append(d_SH,ignore_index=True) # energy from STORAGE HEATER can not be advanced
final = final.append(p_SH,ignore_index=True)
final = final.append(d_TD,ignore_index=True)
final = final.append(p_TD,ignore_index=True)
final = final.append(d_WH,ignore_index=True) # energy from WATER HEATER can not be advanced
final = final.append(p_WH,ignore_index=True)
final = final.append(d_WM,ignore_index=True)
final = final.append(p_WM,ignore_index=True)
final = final.append(d_CP,ignore_index=True)
final = final.append(p_CP,ignore_index=True)
final = final.append(d_HP,ignore_index=True)
final = final.append(p_HP,ignore_index=True)

del(d_AC)
del(p_AC)
del(d_DW)
del(p_DW)
del(d_EV)
del(p_EV)
del(d_SH)
del(p_SH)
del(d_TD)
del(p_TD)
del(d_WH)
del(p_WH)
del(d_WM)
del(p_WM)
del(d_RF_FR)
del(p_RF_FR)
del(d_CP)
del(p_CP)
del(d_HP)
del(p_HP)

# =============================================================================
# country aggregated - separate devices
# =============================================================================


final_country = final.groupby(['country','subannual','variable'], as_index = False).sum()
final_country = final_country.sort_values(['country','variable','subannual'])

final_country['unit']      = 'MW'
final_country['model']     = 'Flexibilities 2.2'
final_country['scenario']  = 'TF_CS1_BE1-Full'
final_country.columns = ['region', 'subannual', 'variable', '2018', '2019', '2020', '2021',
       '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030',
       '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039',
       '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048',
       '2049', '2050', 'unit', 'model', 'scenario']
final_country = final_country[
['model',
 'scenario',
 'region',
 'variable',
 'unit',
 'subannual',
 '2018',
 '2019',
 '2020',
 '2021',
 '2022',
 '2023',
 '2024',
 '2025',
 '2026',
 '2027',
 '2028',
 '2029',
 '2030',
 '2031',
 '2032',
 '2033',
 '2034',
 '2035',
 '2036',
 '2037',
 '2038',
 '2039',
 '2040',
 '2041',
 '2042',
 '2043',
 '2044',
 '2045',
 '2046',
 '2047',
 '2048',
 '2049',
 '2050']]

final_country.to_csv(r'./Full_potential.V7.country.csv', index = False)

#################################################
# nuts 2
#################################################

# rearrange columns
#| **model**   | **scenario**        | **region** | **variable**   | **unit** | **subannual**     | **2015** | **2020** | **2025** |
list(final)
final = final[
['model',
 'scenario',
 'region',
 'variable',
 'unit',
 'subannual',
 '2018',
 '2019',
 '2020',
 '2021',
 '2022',
 '2023',
 '2024',
 '2025',
 '2026',
 '2027',
 '2028',
 '2029',
 '2030',
 '2031',
 '2032',
 '2033',
 '2034',
 '2035',
 '2036',
 '2037',
 '2038',
 '2039',
 '2040',
 '2041',
 '2042',
 '2043',
 '2044',
 '2045',
 '2046',
 '2047',
 '2048',
 '2049',
 '2050']]

#validate df
iamcdf = pyam.IamDataFrame(final)

final.to_csv(r'./Full_potential.V7.csv', index = False)

'''
# =============================================================================
# country aggregate and variable aggregate - this no longer works because of the two EV scenarios
# =============================================================================



# aggregate all countries
final_agg = final_country.groupby(['subannual','variable'], as_index = False).sum()
final_agg.to_csv(r'./Full_potential.V.Agg.csv', index = False)
'''
"""

# iamc validate df
iamcdf = pyam.IamDataFrame(df)
