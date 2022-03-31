#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:45:36 2020

@author: ryanoreilly
"""

##############################
#summary statistics for countries
##############################
#create 
Austria = df.loc[(df['country'] == 'AT')]# & (df['nutsno'] == 3)]
Austria.to_csv(r'Austria.csv')

Austria.sort_values(by=['month', 'hour'], inplace=True)
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
os.chdir('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data')
## TEST TEST COMMMENT
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
### END - global options
### Load in data
df = pd.read_csv('df.final.10.9.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
df = df.sort_values(by=['month', 'hour']) #sorts df by day and hour

country_list =np.unique(df['country']) #countries used in the analysis

cntry_nuts = {} # countries nuts codes or regions
for i in country_list: 
    temp_df = df[df['country']== i]
    cntry_nuts[i] = np.unique(temp_df['nutsno'])
    
    
##############################
#summary statistics for countries
##############################

#Austria summary

AustriaTD =pd.DataFrame()
AustriaWM =pd.DataFrame()
AustriaDW =pd.DataFrame()
AustriaTD.to_csv(r'Austria.TD.csv')
for i in range(0,len(cntry_nuts['AT'])): 
    temp = df.loc[(df['nutsno'] == cntry_nuts['AT'][i])]
    temp.sort_values(by=['month', 'hour'], inplace=True)
    TDhr = list(temp['hrly_TD'])
    capTD= list(temp['installed_adj_TD'])
    incTD= list(temp['Pincrease_TD'])
    WMhr = list(temp['hrly_WM'])
    capWM= list(temp['installed_adj_WM'])
    incWM= list(temp['Pincrease_WM'])
    DWhr = list(temp['hrly_DW'])
    capDW= list(temp['installed_adj_DW'])
    incDW= list(temp['Pincrease_DW'])
    AustriaTD['hrly_TD'+str(i+1)] = TDhr
    AustriaTD['cap_TD'+str(i+1)]  = capTD
    AustriaTD['incr_TD'+str(i+1)] = incTD
    AustriaWM['hrly_WM'+str(i+1)] = WMhr
    AustriaWM['cap_WM'+str(i+1)]  = capWM
    AustriaWM['incr_WM'+str(i+1)] = incWM
    AustriaDW['hrly_DW'+str(i+1)] = DWhr
    AustriaDW['cap_DW'+str(i+1)]  = capDW
    AustriaDW['incr_DW'+str(i+1)] = incDW
    
AustriaTD=AustriaTD.sort_index(axis = 1) 
A_cap_TD  = list(AustriaTD)[0:9]
A_hrly_TD = list(AustriaTD)[9:18]
A_incr_TD = list(AustriaTD)[18:27]

AustriaTD['cap_sum'] = AustriaTD[A_cap_TD].sum(axis=1)
AustriaTD['hrly_sum'] = AustriaTD[A_hrly_TD].sum(axis=1)
AustriaTD['incr_sum'] = AustriaTD[A_incr_TD].sum(axis=1)

AustriaWM=AustriaWM.sort_index(axis = 1) 
A_cap_WM  = list(AustriaWM)[0:9]
A_hrly_WM = list(AustriaWM)[9:18]
A_incr_WM = list(AustriaWM)[18:27]

AustriaWM['cap_sum'] = AustriaWM[A_cap_WM].sum(axis=1)
AustriaWM['hrly_sum'] = AustriaWM[A_hrly_WM].sum(axis=1)
AustriaWM['incr_sum'] = AustriaWM[A_incr_WM].sum(axis=1)

AustriaDW=AustriaDW.sort_index(axis = 1) 
A_cap_DW  = list(AustriaDW)[0:9]
A_hrly_DW = list(AustriaDW)[9:18]
A_incr_DW = list(AustriaDW)[18:27]

AustriaDW['cap_sum'] = AustriaDW[A_cap_DW].sum(axis=1)
AustriaDW['hrly_sum'] = AustriaDW[A_hrly_DW].sum(axis=1)
AustriaDW['incr_sum'] = AustriaDW[A_incr_DW].sum(axis=1)

# UK summaries

UK_TD =pd.DataFrame()
UK_WM =pd.DataFrame()
UK_DW =pd.DataFrame()
for i in range(0,len(cntry_nuts['UK'])): 
    temp = df.loc[(df['nutsno'] == cntry_nuts['UK'][i])]
    temp.sort_values(by=['month', 'hour'], inplace=True)
    TDhr = list(temp['hrly_TD'])
    capTD= list(temp['installed_adj_TD'])
    incTD= list(temp['Pincrease_TD'])
    WMhr = list(temp['hrly_WM'])
    capWM= list(temp['installed_adj_WM'])
    incWM= list(temp['Pincrease_WM'])
    DWhr = list(temp['hrly_DW'])
    capDW= list(temp['installed_adj_DW'])
    incDW= list(temp['Pincrease_DW'])
    UK_TD['hrly_TD'+str(i+1)] = TDhr
    UK_TD['cap_TD'+str(i+1)]  = capTD
    UK_TD['incr_TD'+str(i+1)] = incTD
    UK_WM['hrly_WM'+str(i+1)] = WMhr
    UK_WM['cap_WM'+str(i+1)]  = capWM
    UK_WM['incr_WM'+str(i+1)] = incWM
    UK_DW['hrly_DW'+str(i+1)] = DWhr
    UK_DW['cap_DW'+str(i+1)]  = capDW
    UK_DW['incr_DW'+str(i+1)] = incDW




 
UK_TD=UK_TD.sort_index(axis = 1) 
U_cap_TD  = list(UK_TD)[0:36]
U_hrly_TD = list(UK_TD)[36:72]
U_incr_TD = list(UK_TD)[72:108]

UK_TD['cap_sum']  =  UK_TD[U_cap_TD].sum(axis=1)
UK_TD['hrly_sum'] = UK_TD[U_hrly_TD].sum(axis=1)
UK_TD['incr_sum'] = UK_TD[U_incr_TD].sum(axis=1)

UK_WM=UK_WM.sort_index(axis = 1) 
U_cap_WM  = list(UK_WM)[0:36]
U_hrly_WM = list(UK_WM)[36:72]
U_incr_WM = list(UK_WM)[72:108]

UK_WM['cap_sum']  =  UK_WM[U_cap_WM].sum(axis=1)
UK_WM['hrly_sum'] = UK_WM[U_hrly_WM].sum(axis=1)
UK_WM['incr_sum'] = UK_WM[U_incr_WM].sum(axis=1)

UK_DW=UK_DW.sort_index(axis = 1) 
U_cap_DW  = list(UK_DW)[0:36]
U_hrly_DW = list(UK_DW)[36:72]
U_incr_DW = list(UK_DW)[72:108]

UK_DW['cap_sum']  =  UK_DW[U_cap_DW].sum(axis=1)
UK_DW['hrly_sum'] = UK_DW[U_hrly_DW].sum(axis=1)
UK_DW['incr_sum'] = UK_DW[U_incr_DW].sum(axis=1)


# France Summaries
France = pd.DataFrame()
FR_TD =pd.DataFrame()
FR_WM =pd.DataFrame()
FR_DW =pd.DataFrame()
for i in range(0,len(cntry_nuts['FR'])): 
    temp = df.loc[(df['nutsno'] == cntry_nuts['FR'][i])]
    temp.sort_values(by=['month', 'hour'], inplace=True)
    TDhr = list(temp['hrly_TD'])
    capTD= list(temp['installed_adj_TD'])
    incTD= list(temp['Pincrease_TD'])
    WMhr = list(temp['hrly_WM'])
    capWM= list(temp['installed_adj_WM'])
    incWM= list(temp['Pincrease_WM'])
    DWhr = list(temp['hrly_DW'])
    capDW= list(temp['installed_adj_DW'])
    incDW= list(temp['Pincrease_DW'])
    FR_TD['hrly_TD'+str(i+1)] = TDhr
    FR_TD['cap_TD'+str(i+1)]  = capTD
    FR_TD['incr_TD'+str(i+1)] = incTD
    FR_WM['hrly_WM'+str(i+1)] = WMhr
    FR_WM['cap_WM'+str(i+1)]  = capWM
    FR_WM['incr_WM'+str(i+1)] = incWM
    FR_DW['hrly_DW'+str(i+1)] = DWhr
    FR_DW['cap_DW'+str(i+1)]  = capDW
    FR_DW['incr_DW'+str(i+1)] = incDW


FR_TD=FR_TD.sort_index(axis = 1) 
F_cap_TD  = list(FR_TD)[0:22]
F_hrly_TD = list(FR_TD)[22:44]
F_incr_TD = list(FR_TD)[44:66]

FR_TD['cap_sum']  =  FR_TD[F_cap_TD].sum(axis=1)
FR_TD['hrly_sum'] = FR_TD[F_hrly_TD].sum(axis=1)
FR_TD['incr_sum'] = FR_TD[F_incr_TD].sum(axis=1)

FR_WM=FR_WM.sort_index(axis = 1) 
F_cap_WM  = list(FR_WM)[0:22]
F_hrly_WM = list(FR_WM)[22:44]
F_incr_WM = list(FR_WM)[44:66]

FR_WM['cap_sum']  =  FR_WM[F_cap_WM].sum(axis=1)
FR_WM['hrly_sum'] = FR_WM[F_hrly_WM].sum(axis=1)
FR_WM['incr_sum'] = FR_WM[F_incr_WM].sum(axis=1)

FR_DW=FR_DW.sort_index(axis = 1) 
F_cap_DW  = list(FR_DW)[0:22]
F_hrly_DW = list(FR_DW)[22:44]
F_incr_DW = list(FR_DW)[44:66]

FR_DW['cap_sum']  =  FR_DW[F_cap_DW].sum(axis=1)
FR_DW['hrly_sum'] = FR_DW[F_hrly_DW].sum(axis=1)
FR_DW['incr_sum'] = FR_DW[F_incr_DW].sum(axis=1)


###############
import matplotlib.pyplot as plt
import re
# Visual summaries
###############
#UK
###############

UK_TD['yr_hrs'] = range(0,len(UK_TD))
UK_DW['yr_hrs'] = range(0,len(UK_DW))
UK_WM['yr_hrs'] = range(0,len(UK_WM))
U_WM, ax = plt.subplots()
ax.plot(UK_WM['yr_hrs'],UK_WM['hrly_sum'],'r--',          label="Hourly Demand")
ax.plot(UK_WM['yr_hrs'],UK_WM['cap_sum'],'b--',           label="Installed Capacity")
ax.plot(UK_WM['yr_hrs'],UK_WM['incr_sum'], 'g--',         label="Energy Shifted foward")
ax.set_xlabel('Hour in 2018')
ax.set_ylabel('Energy in MW')
ax.set_title("UK: Washing Machine energy consumption characteristics")
ax.axis([0,288,-100,max(UK_WM['cap_sum']+50)])
leg = ax.legend()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
U_TD # Austria Tumble Drier
U_DW # Autria Dish Washer
U_WM # Austria Washing Machine

U_TDpinc = UK_TD['incr_sum'].mean()
U_DWpinc = UK_DW['incr_sum'].mean()
U_WMpinc = UK_WM['incr_sum'].mean()

U_TDhr = UK_TD['hrly_sum'].mean()
U_DWhr = UK_DW['hrly_sum'].mean()
U_WMhr = UK_WM['hrly_sum'].mean()
###############
#Austria
###############
AustriaTD['yr_hrs'] = range(0,len(AustriaTD))
AustriaDW['yr_hrs'] = range(0,len(AustriaDW))
AustriaWM['yr_hrs'] = range(0,len(AustriaWM))
A_DW, ax = plt.subplots()
ax.plot(AustriaDW['yr_hrs'],AustriaDW['hrly_sum'],'r--',          label="Hourly Demand")
ax.plot(AustriaDW['yr_hrs'],AustriaDW['cap_sum'],'b--',           label="Installed Capacity")
ax.plot(AustriaDW['yr_hrs'],AustriaDW['incr_sum'], 'g--',         label="Energy Shifted foward")
ax.set_xlabel('Hour in 2018')
ax.set_ylabel('Energy in MW')
ax.set_title("Austria: Dish Washer energy consumption characteristics")
ax.axis([0,288,-100,max(AustriaDW['cap_sum']+50)])
leg = ax.legend()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
A_TD # Austria Tumble Drier
A_DW # Autria Dish Washer
A_WM # Austria Washing Machine

A_TDpinc = AustriaTD['incr_sum'].mean()
A_DWpinc = AustriaDW['incr_sum'].mean()
A_WMpinc = AustriaWM['incr_sum'].mean()

A_TDhr = AustriaTD['hrly_sum'].mean()
A_DWhr = AustriaDW['hrly_sum'].mean()
A_WMhr = AustriaWM['hrly_sum'].mean()
###############
#France
###############
FR_TD['yr_hrs'] = range(0,len(FR_TD))
FR_DW['yr_hrs'] = range(0,len(FR_DW))
FR_WM['yr_hrs'] = range(0,len(FR_WM))
F_WM, ax = plt.subplots()
ax.plot(FR_WM['yr_hrs'],FR_WM['hrly_sum'],'r--',          label="Hourly Demand")
ax.plot(FR_WM['yr_hrs'],FR_WM['cap_sum'],'b--',           label="Installed Capacity")
ax.plot(FR_WM['yr_hrs'],FR_WM['incr_sum'], 'g--',         label="Energy Shifted foward")
ax.set_xlabel('Hour in 2018')
ax.set_ylabel('Energy in MW')
ax.set_title("France: Washing Machine energy consumption characteristics")
ax.axis([0,288,-100,max(FR_WM['cap_sum']+50)])
leg = ax.legend()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
F_TD # Austria Tumble Drier
F_DW # Autria Dish Washer
F_WM # Austria Washing Machine

F_TDpinc = FR_TD['incr_sum'].mean()
F_DWpinc = FR_DW['incr_sum'].mean()
F_WMpinc = FR_WM['incr_sum'].mean()

F_TDhr = FR_TD['hrly_sum'].mean()
F_DWhr = FR_DW['hrly_sum'].mean()
F_WMhr = FR_WM['hrly_sum'].mean()



#######
# test


ss_later = df[['country','Pred_CP','Pred_RF','Pred_FR','Pred_WM','Pred_TD','Pred_DW','Pred_AC']]
ss_sooner = df[['country','Pincrease_SH','Pincrease_WH','Pincrease_WM','Pincrease_TD','Pincrease_DW']]
ss_sooner['Pincrease_SH'] = ss_sooner['Pincrease_SH'].astype(float)
ss_sooner['Pincrease_WH'] = ss_sooner['Pincrease_WH'].astype(float)
ss_sooner['Pincrease_TD'] = ss_sooner['Pincrease_TD'].astype(float)
ss_sooner['Pincrease_DW'] = ss_sooner['Pincrease_DW'].astype(float)
ss_sooner['Pincrease_WM'] = ss_sooner['Pincrease_WM'].astype(float)
#ss_sooner['country'] = df['country']
later_summary=ss_later.groupby(by=["country"]).mean()
sooner_summary=ss_sooner.groupby(by=["country"]).mean()

df.loc[(df['country'] == 'AT')]['Pincrease_TD'].mean()


