#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:13:44 2021

@author: ryanoreilly
"""

## Import packages
import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email.MIMEText import MIMEText
import requests # for API
### Set options
#os.chdir('I:\Projekte\OpenEntrance - WV0173\Durchführungsphase\WP6\CS1\gitlab\datainputs') # set wd - change to server path - IMPORTANT
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential')
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
### END - global options
### Load in data
d_WM = pd.read_csv('./d_WMV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_WH = pd.read_csv('./d_WHV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_TD = pd.read_csv('./d_TDV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_SH = pd.read_csv('./d_SHV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_RF = pd.read_csv('./d_RFV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_FR = pd.read_csv('./d_FRV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_EV = pd.read_csv('./d_EVV5.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_DW = pd.read_csv('./d_DWV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
d_AC = pd.read_csv('./d_ACV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)

# create index for iterations
country_list = np.unique(d_WM['country']) #countries used in the analysis

cntry_nuts = {} # countries nuts codes or regions
for i in country_list: 
    temp_df = d_WM[d_WM['country']== i] # change to d_AC
    cntry_nuts[i] = np.unique(temp_df['nutscode'])
    
    
  


# air conditioning
ac2 = d_AC.drop('hour', axis=1)
ac2 = ac2.groupby('nutscode').sum()
ac2['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    ac2['country'][i] = ac2.index[i][0:2]
    
ac2 = ac2.groupby('country').sum()/288
ac = ac.groupby('country').sum()/288

# dish washer
dw = d_DW.drop(['hour','Unnamed: 0'], axis=1)
dw = dw.groupby('nutscode').sum()
dw['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    dw['country'][i] = dw.index[i][0:2]
    
dw = dw.groupby('country').sum()/288

# electric vehicle
ev = d_EV.drop(['hour','Unnamed: 0'], axis=1)
ev = ev.groupby('nutscode').sum()
ev['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    ev['country'][i] = ev.index[i][0:2]
    
ev = ev.groupby('country').sum()/288

# FREEZER
fr = d_FR.drop(['hour','Unnamed: 0'], axis=1)
fr = fr.groupby('nutscode').sum()
fr['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    fr['country'][i] = fr.index[i][0:2]
    
fr = fr.groupby('country').sum()/288

# REFRIGERATOR
rf = d_RF.drop(['hour','Unnamed: 0'], axis=1)
rf = rf.groupby('nutscode').sum()
rf['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    rf['country'][i] = rf.index[i][0:2]
    
rf = rf.groupby('country').sum()/288

# STORAGE HEATER
sh = d_SH.drop('hour', axis=1)
sh = sh.groupby('nutscode').sum()
sh['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    sh['country'][i] = sh.index[i][0:2]
    
sh = sh.groupby('country').sum()/288

# TUMBLE DRIER
td = d_TD.drop(['hour','Unnamed: 0'], axis=1)
td = td.groupby('nutscode').sum()
td['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    td['country'][i] = td.index[i][0:2]
    
td = td.groupby('country').sum()/288


# WATER HEATER
wh = d_WH.drop('hour', axis=1)
wh = wh.groupby('nutscode').sum()
wh['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    wh['country'][i] = wh.index[i][0:2]
    
wh = wh.groupby('country').sum()/288
    
# WASHING MACHINE
wm = d_WM.drop(['hour','Unnamed: 0'], axis=1)
wm = wm.groupby('nutscode').sum()
wm['country'] =  "" 
for i in range(0,len(set(d_AC['nutscode']))):
    wm['country'][i] = wm.index[i][0:2]
    
wm = wm.groupby('country').sum()/288

yr_2020 = pd.DataFrame(ac.index)

yr_2020 ={ 'ac' : ac['2020'],'dw' : dw['2020'], 'ev' : ev['2020'],'fr' : fr['2020'], 'rf' : rf['2020'],'sh': sh['2020'],'td':td['2020'],'wh' : wh['2020'],'wm': wm['2020']}
yr_2020 = pd.DataFrame(data = yr_2020)
 
#yr 2018

yr_2018 = pd.DataFrame(ac.index)

yr_2018 ={ 'ac' : ac['2018'],'dw' : dw['2018'], 'ev' : ev['2018'],'fr' : fr['2018'], 'rf' : rf['2018'],'sh': sh['2018'],'td':td['2018'],'wh' : wh['2018'],'wm': wm['2018']}
yr_2018 = pd.DataFrame(data = yr_2018)

yr_2018.to_csv(r'/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/OE Twitter image/yr_2018.csv')
   

yr_2020.to_csv(r'/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/theoretical potential/yr_2020.2.csv')
   
test = pd.DataFrame(yr_2020.sum(axis=1)).sum() # average energy in any given hour for Europe^* in MW
test2 = test*12*30*24/1000/1000

#old method 
"""
# begin appliances
# air conditioning

df_long_AC = d_AC.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_AC['country']))

AC_final = pd.DataFrame()
AC_final['Country']= country_list
AC_final['hourlyAC']=""
for country in range(0,len(country_list)): #sums across rows, nuts for hour t, then sums the column of row sums, then divides by number of hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    ac=(df_long_AC.loc[row_min:row_max])
    AC_final['hourlyAC'][country]= ac.iloc[:,0:ac.shape[1]].sum().sum()/288
    
    
    
'''
# heat circulation pump    
df_long_CP = d_CP.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_CP['country']))

CP_final = pd.DataFrame()
CP_final['Country']= country_list
CP_final['hourlyCP']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    cp=(df_long_CP.loc[row_min:row_max])
    CP_final['hourlyCP'][country]= cp.iloc[:,0:cp.shape[1]].sum().sum()/288
  '''  
    
    
    
# water heater; multiplying the hourly demand by the shiftability of the technology creates results similiar to GIls table 10; tshift 12 

df_long_WH = d_WH.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_WH['country']))

WH_final = pd.DataFrame()
WH_final['Country']= country_list
WH_final['hourlyWH']=""
for country in range(0,len(country_list)): #sums across rows, nuts for hour t, then sums the column of row sums, then divides by number of hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    wh=(df_long_WH.loc[row_min:row_max])
    WH_final['hourlyWH'][country]= wh.iloc[:,0:wh.shape[1]].sum().sum()/288
 
# storage heater; multiplying the hourly demand by the shiftability of the technology creates results similiar to GIls table 10; tshift 12 

df_long_SH = d_SH.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_SH['country']))

SH_final = pd.DataFrame()
SH_final['Country']= country_list
SH_final['hourlySH']=""
for country in range(0,len(country_list)): #sums across rows, nuts for hour t, then sums the column of row sums, then divides by number of hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    sh=(df_long_SH.loc[row_min:row_max])
    SH_final['hourlySH'][country]= sh.iloc[:,0:sh.shape[1]].sum().sum()/288
 

               
# refridgerator
  
df_long_RF = d_RF.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_RF['country']))

RF_final = pd.DataFrame()
RF_final['Country']= country_list
RF_final['hourlyRF']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    rf=(df_long_RF.loc[row_min:row_max])
    RF_final['hourlyRF'][country]= rf.iloc[:,0:rf.shape[1]].sum().sum()/288
    

# freezer
  
df_long_FR = d_FR.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_FR['country']))

FR_final = pd.DataFrame()
FR_final['Country']= country_list
FR_final['hourlyFR']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    fr=(df_long_FR.loc[row_min:row_max])
    FR_final['hourlyFR'][country]= fr.iloc[:,0:fr.shape[1]].sum().sum()/288
    

# washing machine
  
df_long_WM = d_WM.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_WM['country']))

WM_final = pd.DataFrame()
WM_final['Country']= country_list
WM_final['hourlyWM']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    wm=(df_long_WM.loc[row_min:row_max])
    WM_final['hourlyWM'][country]= wm.iloc[:,0:wm.shape[1]].sum().sum()/288
    


# tumble drier
  
df_long_TD = d_TD.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_TD['country']))

TD_final = pd.DataFrame()
TD_final['Country']= country_list
TD_final['hourlyTD']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    td=(df_long_TD.loc[row_min:row_max])
    TD_final['hourlyTD'][country]= td.iloc[:,0:td.shape[1]].sum().sum()/288
    

# dish washer
  
df_long_DW = d_DW.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_DW['country']))

DW_final = pd.DataFrame()
DW_final['Country']= country_list
DW_final['hourlyDW']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    dw=(df_long_DW.loc[row_min:row_max])
    DW_final['hourlyDW'][country]= dw.iloc[:,0:dw.shape[1]].sum().sum()/288
    
# electric vehicles
  
df_long_EV = d_EV.pivot_table(index=['nutscode'],
                           columns=['country','TIME','hour'],
                           values=['2018'])
country_list=list(set(d_EV['country']))

EV_final = pd.DataFrame()
EV_final['Country']= country_list
EV_final['hourlyEV']=""
for country in range(0,len(country_list)): #sums across rows, represantative hours in year, then sums the column of row sums (nuts 2 totals), then divides by number of representative hours
    name=str(country_list[country])
    row_min = cntry_nuts[name].min()
    row_max = cntry_nuts[name].max()
    print(country)
    ev=(df_long_EV.loc[row_min:row_max])
    EV_final['hourlyEV'][country]= ev.iloc[:,0:ev.shape[1]].sum().sum()/288    
"""    
    
  
    
    