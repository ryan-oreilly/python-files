# -*- coding: utf-8 -*-
"""
The objective of this file is to:
    1 create yr_cdd and yr_hdd for the turkish regions
    2 create hourly shares
Steps

    
https://www.ecad.eu/dailydata/predefinedseries.php

RIZE (STAID: 343) 
KASTAMONU (STAID: 344).
SIVAS (STAID: 345).
VAN (STAID: 1439).
ISTANBUL (STAID: 248).
ISPARTA (STAID: 346).
FINIKE (STAID: 347).
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os
from smtplib import SMTP_SSL ## for sending emails
import pyam
import nomenclature
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email.MIMEText import MIMEText
import requests # for API
### Set options
#os.chdir('I:\Projekte\OpenEntrance - WV0173\Durchführungsphase\WP6\CS1\gitlab\datainputs') # set wd - change to server path - IMPORTANT
os.chdir('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/openENTRANCE projection/Turkey HDD.CDD/ECA_blended_custom/temp data')
"""
Extract files and subset observations from 1994-2005
Create columns for subsetting
"""
file = list(os.listdir())
ID = ['f248','f1439','f347','f346','f343','f344','f345']
count = 0
for f in file:
    print(count)
    temp = pd.read_table(f,sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
    temp['year']  = ""
    temp['month'] = ""
    temp['day']   = ""
    temp['t_av']  = ""
    for i in range(0,temp.shape[0]):
        temp['year'][i]  =int(str(temp['DATE'].loc[i])[0:4]) #year
        #temp['month'][i] =int(str(temp['DATE'].loc[i])[4:6]) # month
        #temp['day'][i]   =int(str(temp['DATE'].loc[i])[6:8]) # month
        #temp['t_av'][i]   =   temp['TG'].loc[i]*0.1
    temp = temp[(temp['year']>=1993) & (temp['year']<=2003)]
    for i in range(0,temp.shape[0]):
            temp['month'].iloc[i] =int(str(temp['DATE'].iloc[i])[4:6]) # month
            temp['day'].iloc[i]   =int(str(temp['DATE'].iloc[i])[6:8]) # month
            temp['t_av'].iloc[i]   =   temp['TG'].iloc[i]*0.1
    temp = temp[['year','month','day','t_av','Q_TG']]
    temp = temp.reset_index()
    temp = temp.drop('index',axis =1)
    temp['hdd'] = ""
    temp['cdd'] = ""
    for day in range(0, temp.shape[0]):
    #hdd
        if temp['t_av'][day] <=15:
            temp['hdd'][day] = 18 - temp['t_av'][day] 
        else:
            temp['hdd'][day]=0
        #cdd
        if temp['t_av'][day] >=24:
            temp['cdd'][day] = temp['t_av'][day] -21
        else:
            temp['cdd'][day]= 0
        if temp['Q_TG'][day] != 0: # if 1 or 9 there is an error in data collection
            temp['hdd'][day] = ""
            temp['cdd'][day] = ""
    temp = temp.apply(pd.to_numeric)
    M_mean = temp.groupby(['Q_TG','month']).mean()
    for day in range(0, temp.shape[0]):
        if temp['Q_TG'][day] != 0:
            month = temp['month'][day]
            hdd = M_mean.loc[0].iloc[month-1].iloc[3] # the first iloc identifies the subset of average daily temperature for results that are valid hence Q_TG= 0
            cdd = M_mean.loc[0].iloc[month-1].iloc[4] # the -1 comes from 0 indexing
            temp['hdd'][day] = hdd
            temp['cdd'][day] = cdd
    ID[count] = temp
    count +=1
    
f248 = ID[0]
f1439 = ID[1]
f347= ID[2]
f346= ID[3]
f343= ID[4]
f344= ID[5]
f345= ID[6]

del ID
del temp
del file
del i
del f
del count
del day
del hdd
del month
del cdd
del M_mean

# read in format for TIME
switzerland=pd.read_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/switzerland.final.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
TIME = list(switzerland['TIME'][0:12])

# shares of hdd and cdd
D248  = f248.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D248['yr_hdd'] =D248.sum()[0]
D248['yr_cdd'] = D248.sum()[1]
D248['ID'] = 248
D248['s_hdd'] = ""
D248['s_cdd'] = ""
D248['TIME'] = TIME
D1439 = f1439.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D1439['yr_hdd'] =D1439.sum()[0]
D1439['yr_cdd'] =D1439.sum()[1]
D1439['ID'] = 1439
D1439['s_hdd'] = ""
D1439['s_cdd'] = ""
D1439['TIME'] = TIME
D347  = f347.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D347['yr_hdd'] =D347.sum()[0]
D347['yr_cdd'] =D347.sum()[1]
D347['ID'] = 347
D347['s_hdd'] = ""
D347['s_cdd'] = ""
D347['TIME'] = TIME
D346  = f346.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D346['yr_hdd'] =D346.sum()[0]
D346['yr_cdd'] =D346.sum()[1]
D346['ID'] = 346
D346['s_hdd'] = ""
D346['s_cdd'] = ""
D346['TIME'] = TIME
D343  = f343.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D343['yr_hdd'] =D343.sum()[0]
D343['yr_cdd'] =D343.sum()[1]
D343['ID'] = 343
D343['s_hdd'] = ""
D343['s_cdd'] = ""
D343['TIME'] = TIME
D344  = f344.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D344['yr_hdd'] =D344.sum()[0]
D344['yr_cdd'] =D344.sum()[1]
D344['ID'] = 344
D344['s_hdd'] = ""
D344['s_cdd'] = ""
D344['TIME'] = TIME
D345  = f345.groupby(['month','day']).mean().groupby('month').sum()[['hdd','cdd']]
D345['yr_hdd'] =D345.sum()[0]
D345['yr_cdd'] =D345.sum()[1]
D345['ID'] = 345
D345['s_hdd'] = ""
D345['s_cdd'] = ""
D345['TIME'] = TIME


for mon in range(1,D248.shape[0]+1):
    D248['s_hdd'][mon] = D248['hdd'][mon]/D248['yr_hdd'][mon]
    D248['s_cdd'][mon] = D248['cdd'][mon]/D248['yr_cdd'][mon]
    D1439['s_hdd'][mon] = D1439['hdd'][mon]/D1439['yr_hdd'][mon]
    D1439['s_cdd'][mon] = D1439['cdd'][mon]/D1439['yr_cdd'][mon]
    D347['s_hdd'][mon] = D347['hdd'][mon]/D347['yr_hdd'][mon]
    D347['s_cdd'][mon] = D347['cdd'][mon]/D347['yr_cdd'][mon]
    D346['s_hdd'][mon] = D346['hdd'][mon]/D346['yr_hdd'][mon]
    D346['s_cdd'][mon] = D346['cdd'][mon]/D346['yr_cdd'][mon]
    D343['s_hdd'][mon] = D343['hdd'][mon]/D343['yr_hdd'][mon]
    D343['s_cdd'][mon] = D343['cdd'][mon]/D343['yr_cdd'][mon]
    D344['s_hdd'][mon] = D344['hdd'][mon]/D344['yr_hdd'][mon]
    D344['s_cdd'][mon] = D344['cdd'][mon]/D344['yr_cdd'][mon]
    D345['s_hdd'][mon] = D345['hdd'][mon]/D345['yr_hdd'][mon]
    D345['s_cdd'][mon] = D345['cdd'][mon]/D345['yr_cdd'][mon]

reg = D248.append(D1439)
reg = reg.append(D347)
reg = reg.append(D346)
reg = reg.append(D343)
reg = reg.append(D344)
reg = reg.append(D345)
# create index
index = pd.read_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/turkey.final.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
index = index[['ID','nutscode']]
index = index.drop_duplicates()
index.to_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/openENTRANCE projection/Turkey HDD.CDD/turkey nuts.csv')


final = index.merge(reg, on ='ID',how="outer")
final = final.drop(['ID'],axis=1)
final.to_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/turkey.final.csv')



