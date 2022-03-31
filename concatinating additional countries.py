#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 10:51:34 2020

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
os.chdir('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data')

df = pd.read_csv('df.10.27.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

norway=pd.read_csv('norway.final.csv')
switzerland=pd.read_csv('switzerland.final.csv')

# all code from 27-44 was performed in R
#expand dataframe
#rows= test['country']== 'NO' # identifys rows
#df_exp = test[rows] # creates dataframe of the rows
#nutsunique =np.unique(df_exp['nutscode']) #nuts codes of interest

#expansion for months
#df_exp = df_exp.append([df_exp]*11,ignore_index=True)
#df_exp['month']=""
#for i in nutsunique: 
#    temp= df_exp.loc[(df_exp['nutscode'] == i), 'month'] = range(1,13)
    
#expansion hours
#df_exp['hour'] = ""    
#df_exp = df_exp.append([df_exp]*23,ignore_index=True)
#for i in nutsunique: #expansion for hours
#    for mon in range(1,13):
#        temp= df_exp.loc[(df_exp['nutscode'] == i) & (df_exp['month'] == mon)  , 'hour'] = range(0,24) 

#concatinate df's
frames=[df,norway]
df_w_norway =pd.concat(frames,ignore_index=True)
del df_w_norway['Unnamed: 0']
frames=[df_w_norway,switzerland]
df_final =pd.concat(frames,ignore_index=True)
del df_final['Unnamed: 0']
# adding hour shares for TD, WM and DW
# the shares of TD, WM and DW are the same for all countries and between all nuts regions
# AT21 is selected to apply its values of shares for Norways
s_wm = list(df_final.loc[(df_final['nutscode'] == 'AT21') ,'S_WM'])
s_td = list(df_final.loc[(df_final['nutscode'] == 'AT21') ,'S_TD'])
s_dw = list(df_final.loc[(df_final['nutscode'] == 'AT21') ,'S_DW'])

#add norway
temp = df_final.loc[(df_final['country'] == 'NO')]
for i in range(0,len(list(set(temp.nutscode)))):
    id_region=list(set(temp.nutscode))[i]
    df_final.loc[(df_final['nutscode'] == id_region) ,'S_WM'] = s_wm
    df_final.loc[(df_final['nutscode'] == id_region) ,'S_TD'] = s_td
    df_final.loc[(df_final['nutscode'] == id_region) ,'S_DW'] = s_dw
    
#add switzerland
temp = df_final.loc[(df_final['country'] == 'CH')]
for i in range(0,len(list(set(temp.nutscode)))):
    id_region=list(set(temp.nutscode))[i]
    df_final.loc[(df_final['nutscode'] == id_region) ,'S_WM'] = s_wm
    df_final.loc[(df_final['nutscode'] == id_region) ,'S_TD'] = s_td
    df_final.loc[(df_final['nutscode'] == id_region) ,'S_DW'] = s_dw
    
df_final.to_csv(r'df.all.csv')


