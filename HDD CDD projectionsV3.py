#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday April 22

@author: ryanoreilly

V3 v V2. V3 uses EOBS dataset for all nuts2 regions

"""
import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os

### Set options
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/')
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
### END - global options
### Load in data
cdd_raw =pd.read_csv('./temperature/CDD_.1deg_11-21_V2.csv')
hdd_raw =pd.read_csv('./temperature/HDD_.1deg_11-21_V2.csv')
cdd_raw = cdd_raw.drop('Unnamed: 0', axis=1)
hdd_raw = hdd_raw.drop('Unnamed: 0', axis=1)
cdd_raw=cdd_raw.rename(columns = {'NUTS':'nutscode'})
hdd_raw=hdd_raw.rename(columns = {'NUTS':'nutscode'})
# filter out non NUTS2 regions with NHHV2 
nhh = pd.read_csv('./openENTRANCE final data/nhhV2.csv')
nhh = nhh[['nutscode']]

cdd_merge = cdd_raw.merge(nhh, how ='right')
set(nhh.nutscode)-set(cdd_merge.nutscode)
hdd_merge = hdd_raw.merge(nhh, how = 'right')

cdd_merge['country']= ""
for row in range(0,cdd_merge.shape[0]):
    cdd_merge['country'][row] = cdd_merge['nutscode'][row][0:2]


hdd_merge['country']= ""
for row in range(0,hdd_merge.shape[0]):
    hdd_merge['country'][row] = hdd_merge['nutscode'][row][0:2]

# create annual hdd and cdd 
months = list(hdd_merge)[1:13]
hdd_merge['yr_HDD'] = hdd_merge[months].sum(axis = 1)
cdd_merge['yr_CDD'] = cdd_merge[months].sum(axis = 1)
# wide to long
# monthly
cdd_lr = pd.melt(cdd_merge,id_vars = ['country','nutscode','yr_CDD'],value_vars = list(cdd_merge.columns)[1:13])
hdd_lr = pd.melt(hdd_merge,id_vars = ['country','nutscode','yr_HDD'],value_vars = list(hdd_merge.columns)[1:13])

cdd_lr['month'] = cdd_lr['variable']
hdd_lr['month'] = cdd_lr['variable']
cdd_lr = cdd_lr.drop('variable', axis=1)
hdd_lr = hdd_lr.drop('variable', axis=1)

#drop PT20, FRY1-5
cdd_lr = cdd_lr.dropna()
hdd_lr = hdd_lr.dropna()
#create monthly shares 
cdd_lr['s_cdd'] = cdd_lr['value']/cdd_lr['yr_CDD']
hdd_lr['s_hdd'] = hdd_lr['value']/hdd_lr['yr_HDD']

#fill nas from 0/0 to 0
cdd_lr['s_cdd'] = cdd_lr['s_cdd'].fillna(0)
hdd_lr['s_hdd'] = hdd_lr['s_hdd'].fillna(0)

# rate of change hdd cdd
dd_change=pd.read_excel('country dd projections.xlsx')

nhh = nhh.reset_index()
temp = nhh[['nutscode']]
temp['country']= ""
for row in range(0,len(temp)):
    temp['country'][row] = temp['nutscode'][row][0:2]
temp = temp.sort_values('nutscode')
del nhh
#list of all countries
country = list(set(temp['country']))


# clean dd
cdd_lr = cdd_lr.reset_index()
cdd_lr = cdd_lr.drop('index',axis=1)
hdd_lr = hdd_lr.reset_index()
hdd_lr = hdd_lr.drop('index',axis=1)
    
#############
# create annual projections of hdd and cdd for each nuts region
#expand dd using nutscodes and country
temp_index = cdd_lr.merge(dd_change,how='left')

columns = []
for i in range(2018,2051):
    columns.append(str(i))
    
yr_hdd = pd.DataFrame(index = hdd_lr[['nutscode','month']], columns = columns)   
for row in range(0,len(yr_hdd['2018'])):
    yr_hdd['2018'][row]= hdd_lr['yr_HDD'][row]

for year in range(1,2051-2018):
    print("year:", year)
    for nutscode in range(0,yr_hdd.shape[0]):
        yr_hdd.iloc[nutscode,year] = temp_index['hdd/year'][nutscode]+yr_hdd.iloc[nutscode,year-1] #hdd/year is the amount that hdd is expected to change each year

yr_cdd = pd.DataFrame(index = cdd_lr[['nutscode','month']], columns = columns)   
for row in range(0,len(yr_cdd['2018'])):
    yr_cdd['2018'][row]= cdd_lr['yr_CDD'][row]

for year in range(1,2051-2018):
    print("year:", year)
    for nutscode in range(0,yr_cdd.shape[0]):
        yr_cdd.iloc[nutscode,year] = temp_index['cdd/year'][nutscode]+yr_cdd.iloc[nutscode,year-1]


# set negative values to 0

yr_hdd[yr_hdd < 0] = 0
yr_cdd[yr_cdd < 0] = 0

# use monthly shares of yearly hdd/cdd to convert to expected monthly hdd/cc
columns = []
for i in range(2018,2051):
    columns.append(str(i))
hdd = pd.DataFrame(index = temp_index[['nutscode','month']], columns = columns)   
cdd = pd.DataFrame(index = temp_index[['nutscode','month']], columns = columns)

for year in range(0,2051-2018):
    print("year:", year)
    for nutscode in range(0,hdd.shape[0]):
        hdd.iloc[nutscode,year] = hdd_lr['s_hdd'][nutscode]*yr_hdd.iloc[nutscode,year] # s_hdd is the share of annual hdd for a given month
        cdd.iloc[nutscode,year] = cdd_lr['s_cdd'][nutscode]*yr_cdd.iloc[nutscode,year]
        
# setting indexing
hdd['nutscode'] = ""
hdd['month'] = ""
for row in range(0,hdd.shape[0]):
    hdd['nutscode'][row] = hdd.index[row][0]
    hdd['month'][row] =hdd.index[row][1]
    
cdd['nutscode'] = ""
cdd['month'] = ""
for row in range(0,cdd.shape[0]):
    cdd['nutscode'][row] = cdd.index[row][0]
    cdd['month'][row] =cdd.index[row][1]


# create monthly shares of annual cdd/hdd hdd/yr_hdd; shares dont change between years
s_hdd = pd.DataFrame(index = temp_index[['nutscode','month']], columns = columns)   
s_cdd = pd.DataFrame(index = temp_index[['nutscode','month']], columns = columns)   
for year in range(0,2051-2018):
    print("year:", year)
    for nutscode in range(0,s_hdd.shape[0]):
        s_hdd.iloc[nutscode,year] = hdd.iloc[nutscode,year]/yr_hdd.iloc[nutscode,year]
        s_cdd.iloc[nutscode,year] = cdd.iloc[nutscode,year]/yr_cdd.iloc[nutscode,year]


# setting indexing for year hdd/cdd
yr_cdd['nutscode'] = ""
yr_cdd['month'] = ""
yr_hdd['nutscode'] = ""
yr_hdd['month'] = ""
for row in range(0,yr_cdd.shape[0]):
    yr_cdd['nutscode'][row] = yr_cdd.index[row][0]
    yr_cdd['month'][row] =     yr_cdd.index[row][1]
    yr_hdd['nutscode'][row] = yr_hdd.index[row][0]
    yr_hdd['month'][row] =     yr_hdd.index[row][1]
    

# setting indexing for share hdd/cdd
s_cdd['nutscode'] = ""
s_cdd['month'] = ""
s_hdd['nutscode'] = ""
s_hdd['month'] = ""
for row in range(0,cdd.shape[0]):
    s_cdd['nutscode'][row] = s_cdd.index[row][0]
    s_cdd['month'][row] =     s_cdd.index[row][1]
    s_hdd['nutscode'][row] = s_hdd.index[row][0]
    s_hdd['month'][row] =     s_hdd.index[row][1]
    

def month_to_numeric(df):
    df['month'][df['month'] == 'Jan'] = 1
    df['month'][df['month'] == 'Feb'] = 2
    df['month'][df['month'] == 'Mar'] = 3
    df['month'][df['month'] == 'Apr'] = 4
    df['month'][df['month'] == 'May'] = 5
    df['month'][df['month'] == 'Jun'] = 6
    df['month'][df['month'] == 'Jul'] = 7 
    df['month'][df['month'] == 'Aug'] = 8
    df['month'][df['month'] == 'Sep'] = 9
    df['month'][df['month'] == 'Oct'] = 10
    df['month'][df['month'] == 'Nov'] = 11
    df['month'][df['month'] == 'Dec'] = 12

month_to_numeric(s_cdd)
month_to_numeric(s_hdd)
month_to_numeric(yr_cdd)
month_to_numeric(yr_hdd)


s_hdd = s_hdd.sort_values(['nutscode','month'])
s_cdd = s_cdd.sort_values(['nutscode','month'])
yr_hdd = yr_hdd.sort_values(['nutscode','month'])
yr_cdd = yr_cdd.sort_values(['nutscode','month'])

os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/openENTRANCE final data/')
s_hdd.to_csv(r's_hdd nutsV3.csv', index = False)
s_cdd.to_csv(r's_cdd nutsV3.csv', index = False)
yr_hdd.to_csv(r'yr_hdd nutsV3.csv', index = False)
yr_cdd.to_csv(r'yr_cdd nutsV3.csv', index = False)



   

