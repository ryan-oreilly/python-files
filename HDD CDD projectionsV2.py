#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday Sep 23 2021

@author: ryanoreilly

HR01 are no longer used for NUTS 2 classifications 
It will be used to create HR05 & HR06

long term averages will be used

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
cdd_raw =pd.read_excel('./EUROSTAT CDD HDD/NRG_CDD.xlsx')
hdd_raw =pd.read_excel('./EUROSTAT CDD HDD/NRG_HDD.xlsx')
#missing data for PT30 - country average will be used
# covert to long run averages
# wide to long
cdd_lr = pd.melt(cdd_raw,id_vars = 'NUTS2',value_vars = list(cdd_raw.columns)[1:193])
hdd_lr = pd.melt(hdd_raw,id_vars = 'NUTS2',value_vars = list(cdd_raw.columns)[1:193])
cdd_lr['month'] = ""
hdd_lr['month'] = ""

#group by month
for hour in range(0,hdd_lr.shape[0]):
    hdd_lr['month'][hour] = hdd_lr['variable'].loc[hour][5:7]

for hour in range(0,cdd_lr.shape[0]):
    cdd_lr['month'][hour] = cdd_lr['variable'].loc[hour][5:7]


hdd = hdd_lr.groupby(by=["NUTS2","month"],as_index=False).mean() #nuts2 averages
cdd = cdd_lr.groupby(by=["NUTS2","month"],as_index=False).mean() #nuts2 averages

hdd.columns = ["nutscode",'month','hdd']
cdd.columns = ["nutscode",'month','cdd']


nhh = pd.read_csv('./openENTRANCE final data/nhhV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
#add norway and switzerland
norway=pd.read_csv('norway.final.csv')
switzerland=pd.read_csv('switzerland.final.csv')
turkey=pd.read_csv('turkey.final.csv')
uk =pd.read_excel('./EUROSTAT CDD HDD/UK_DD.xls')
# add month
#group by month
norway['month']= ""
switzerland['month'] = ""
turkey['month'] = ""
for hour in range(0,norway.shape[0]):
    norway['month'][hour] = norway['TIME'].loc[hour][5:7]
for hour in range(0,switzerland.shape[0]):
    switzerland['month'][hour] = switzerland['TIME'].loc[hour][5:7]    
for hour in range(0,turkey.shape[0]):
    turkey['month'][hour] = turkey['TIME'].loc[hour][5:7]


"""
# make adjustements for Croatia
temp = dd[dd['GEO']=="HR01"]
temp2 = dd[dd['GEO']=="HR01"]
temp.GEO = "HR05"
temp2.GEO = "HR06"
dd = dd[dd.GEO != 'HR01']
dd = dd.append(temp)
dd = dd.append(temp2)
dd = dd.reset_index() 
dd = dd.drop('index', axis=1)
"""
# rate of change hdd cdd
dd_change=pd.read_excel('country dd projections.xlsx')
# drop NA's
#nhh = nhh.dropna(axis=0) is this right?!!!!!!!!!!!!
norway=norway.dropna(axis=0)
nhh = nhh.reset_index()
norway = norway.reset_index()
temp = nhh[['nutscode']]
temp['country']= ""
for row in range(0,len(temp)):
    temp['country'][row] = temp['nutscode'][row][0:2]
temp = temp.sort_values('nutscode')
del nhh
#list of all countries
country = list(set(temp['country']))


#clean norway and switzerland
norway = norway[['nutscode','month','hdd','cdd']]
norway=norway.drop_duplicates()
switzerland=switzerland[['nutscode','month','hdd','cdd']]
switzerland=switzerland.drop_duplicates()

# clean dd
cdd = cdd.reset_index()
cdd = cdd.drop('index',axis=1)
hdd = hdd.reset_index()
hdd = hdd.drop('index',axis=1)
    


dd = pd.merge(temp,hdd, on = ['nutscode'], how = "left")
dd = pd.merge(dd,cdd, on = ['nutscode','month'], how ='left')

#118 nuts regions are missing data on cdd and hdd
#for those countries that have data, the average cdd and hdd will be used to fill missing regions
# NO, CH, and TR do not have any data. They will be added using external sources.
# expansion of regions with nulls
hdd['country'] =""
cdd['country'] =""
for row in range(0,hdd.shape[0]):
    hdd['country'][row] = hdd['nutscode'][row][0:2]
    cdd['country'][row] = cdd['nutscode'][row][0:2]    
    
hddcountry = hdd.groupby(by=["country","month"],as_index=False).mean() #country averages
cddcountry = cdd.groupby(by=["country","month"],as_index=False).mean() #country averages
ddcountry = hddcountry.merge(cddcountry)
# add data on uk
#adjust month
uk['month'] = ddcountry['month'][0:12]
frames=[ddcountry,uk]
ddcountry =pd.concat(frames,ignore_index=True)
#set 
del hddcountry
del cddcountry

indices = list(np.where(dd['hdd'].isnull())[0]) 
nafill = dd.loc[indices,:]
nafill.columns = ['nutscode','country','month','hdd','cdd']
nafill = pd.merge(nafill,ddcountry, on =['country'], how ="left")
nafill = nafill[['nutscode', 'country','month_y', 'hdd_y', 'cdd_y']]
nafill.columns = ['nutscode', 'country', 'month', 'hdd', 'cdd']#
#drop TR CH and NO will be added below
nafill = nafill.dropna()

#drop nas from dd. nafill has the nutscode
dd = dd.dropna()

# add nafill to dd
frames=[dd,nafill]
dd =pd.concat(frames,ignore_index=True)    
        
#concatinate df's
#add norway

frames=[dd,norway]
dd =pd.concat(frames,ignore_index=True)
#add Switzerland
frames=[dd,switzerland]
dd =pd.concat(frames,ignore_index=True)

dd['country']= ""
for row in range(0,len(dd.hdd)):
    dd['country'][row] = dd.nutscode[row][0:2]
    
#create yr_hdd
totals =dd.groupby(by = ["nutscode"]).sum()
totals['country']= ""
for row in range(0,len(totals.values)):
    totals['country'][row] = totals.index[row][0:2]

totals.columns = ['yr_hdd','yr_cdd','country']

dd = pd.merge(dd, totals, on = "nutscode")
dd['rhdd'] = dd['hdd']/dd['yr_hdd']
dd['rcdd'] = dd['cdd']/dd['yr_cdd']
dd['rcdd'] = dd['rcdd'].fillna(0) # all nuts regions that had a 0 cdd in a year caused rcdd to be nan. Setting to zero assumes these regions will have no growth in the future cdd
#temp = pd.DataFrame(set(dd['country_y']))
#temp.to_csv(r'country dd projections.csv', index = False)
dd.columns = ['nutscode', 'month', 'hdd', 'cdd', 'country_x', 'yr_hdd', 'yr_cdd', 'country', 'rhdd', 'rcdd']
dd = dd.drop(['country_x'], axis=1)
# add turkey
# clean turkey
turkey['country'] =""
for i in range(0,turkey.shape[0]):
    turkey['country'][i] = turkey['nutscode'][i][0:2]
turkey['rhdd'] = turkey['s_hdd']
turkey['rcdd'] = turkey['s_cdd']
turkey = turkey.drop(['TIME'],axis =1 )

dd2 = dd.append([turkey])
#merge with country dd projections
test = pd.merge(dd2,dd_change, on ="country")



del row
del temp
del time
del indices
del i
del nafill
del switzerland
del dd2
del frames

#############
# create annual projections of hdd and cdd for each nuts region
columns = []
for i in range(2018,2051):
    columns.append(str(i))
yr_hdd = pd.DataFrame(index = test[['nutscode','month']], columns = columns)   
for row in range(0,len(yr_hdd['2018'])):
    yr_hdd['2018'][row]= test['yr_hdd'][row]

for year in range(1,2051-2018):
    print("year:", year)
    for nutscode in range(0,yr_hdd.shape[0]):
        yr_hdd.iloc[nutscode,year] = test['hdd/year'][nutscode]+yr_hdd.iloc[nutscode,year-1] #hdd/year is the amount that hdd is expected to change each year

yr_cdd = pd.DataFrame(index = test[['nutscode','month']], columns = columns)   
for row in range(0,len(yr_cdd['2018'])):
    yr_cdd['2018'][row]= test['yr_cdd'][row]

for year in range(1,2051-2018):
    print("year:", year)
    for nutscode in range(0,yr_cdd.shape[0]):
        yr_cdd.iloc[nutscode,year] = test['cdd/year'][nutscode]+yr_cdd.iloc[nutscode,year-1]


# use monthly shares of yearly hdd/cdd to convert to expected monthly hdd/cc
columns = []
for i in range(2018,2051):
    columns.append(str(i))
hdd = pd.DataFrame(index = test[['nutscode','month']], columns = columns)   
cdd = pd.DataFrame(index = test[['nutscode','month']], columns = columns)

for year in range(0,2051-2018):
    print("year:", year)
    for nutscode in range(0,hdd.shape[0]):
        hdd.iloc[nutscode,year] = test['rhdd'][nutscode]*yr_hdd.iloc[nutscode,year] # rhdd is the share of annual hdd for a given month
        cdd.iloc[nutscode,year] = test['rcdd'][nutscode]*yr_cdd.iloc[nutscode,year]
        
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
s_hdd = pd.DataFrame(index = test[['nutscode','month']], columns = columns)   
s_cdd = pd.DataFrame(index = test[['nutscode','month']], columns = columns)   
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
    

#adjust NA's that arived because of 0/#
s_cdd['2018'] = s_cdd['2018'].fillna(0)

# add NORWAY NO0B to retain nutscode even though is NA    
norway=pd.read_csv('norway.final.csv')
NO0B = norway[norway['nutscode']=="NO0B"]
NO0B.columns = ['Unnamed: 0','nutscode','month','hdd','cdd'] 
NO0B = NO0B[['nutscode',"month"]]

s_hdd = s_hdd.append(NO0B)
s_cdd = s_cdd.append(NO0B)
yr_hdd = yr_hdd.append(NO0B)
yr_cdd = yr_cdd.append(NO0B)

s_hdd = s_hdd.sort_values(['nutscode','month'])
s_cdd = s_cdd.sort_values(['nutscode','month'])
yr_hdd = yr_hdd.sort_values(['nutscode','month'])
yr_cdd = yr_cdd.sort_values(['nutscode','month'])

os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/openENTRANCE final data/')
s_hdd.to_csv(r's_hdd nutsV2.csv', index = False)
s_cdd.to_csv(r's_cdd nutsV2.csv', index = False)
yr_hdd.to_csv(r'yr_hdd nutsV2.csv', index = False)
yr_cdd.to_csv(r'yr_cdd nutsV2.csv', index = False)



   

