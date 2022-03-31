#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:14:03 2020

@author: ryanoreilly
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

# nhh used as reference for nutscodes
nhh = pd.read_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/openENTRANCE final data/nhh.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
# add data for Tumble Dryer, Washing Machine and Dish Washer; from Stamminger
s_wash =pd.read_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/stamminger_11.23.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_wash=s_wash.drop(['Unnamed: 0'],axis=1)

temp = nhh[['nutscode']]
temp['country']= ""
for row in range(0,len(temp)):
    temp['country'][row] = temp['nutscode'][row][0:2]
temp = pd.merge(s_wash,temp, on = 'country',how = "outer")


#regions that do not have hourly shares from stamminger will use EU averages
# expansion of regions with nulls
indices = list(np.where(temp['S_WM'].isnull())[0]) 
nafill = temp.loc[indices,:]
for i in range(0,len(nafill.values)): #expansion of dataset
    nafill=nafill.append([nafill.iloc[i]]*(23),ignore_index=True)
# sort na fill
nafill = nafill.sort_values('nutscode')
nafill = nafill.reset_index()
nafill = nafill.drop(['index'],axis=1)
# create time stamp
time = list(range(0,24))*97
nafill['hour'] = time
# fill in the NA's with EU averages of Stamminger
# EU averages
EUWM = list(temp.loc[(temp['country'] == 'EU') ,'S_WM'])*97
EUTD = list(temp.loc[(temp['country'] == 'EU') ,'S_TD'])*97
EUDW = list(temp.loc[(temp['country'] == 'EU') ,'S_DW'])*97
nafill['S_WM'] = EUWM
nafill['S_DW'] = EUDW
nafill['S_TD'] = EUTD
#drop nas from dd. nafill has the nutscode
temp = temp.dropna()


# add nafill to temp
frames=[temp,nafill]
s_wash =pd.concat(frames,ignore_index=True)

os.chdir('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/openENTRANCE final data')
s_wash.to_csv(r's_wash nuts.csv', index = False)
