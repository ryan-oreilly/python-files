#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 1 2022

@author: ryanoreilly

This script combines stamminger shares.py and s_wash.py to pruduce hourly shares for washing devices for all of the NUTS regions

the objective of this file is to get the stamminger file in a working format compatible with the demand potential py fle

It references stamminger_V2.xlsx which corrected for shares which summed to greater than 1
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os


os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data') # set wd - change to server path - IMPORTANT
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

#read in file
stamminger = pd.read_excel('./stamminger_V2.xlsx')
stamminger = stamminger.reset_index()
stamminger_L= pd.melt(stamminger, id_vars=["Country","Appliance","Power sum in Wh"], value_vars=[0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23])

stamminger_L["share"] =stamminger_L['value']/stamminger_L['Power sum in Wh']

stamminger_L.columns=['Country', 'Appliance', 'Power sum in Wh', 'hour', 'value', 'share']
wm = stamminger_L.loc[(stamminger_L['Appliance'] == 'WM')]
dw = stamminger_L.loc[(stamminger_L['Appliance'] == 'DW')]
td = stamminger_L.loc[(stamminger_L['Appliance'] == 'TD')] #this needs to be merged differently as these shares will be used for every country

td.columns=['Country', 'Appliance', 'Power sum in Wh', 'hour', 'value', 'S_TD']
td=td.drop(['Country','Appliance','Power sum in Wh','value'],axis=1)

wm.columns=['Country', 'Appliance', 'Power sum in Wh', 'hour', 'value', 'S_WM']
dw.columns=['Country', 'Appliance', 'Power sum in Wh', 'hour', 'value', 'S_DW']    
dw=dw.drop(['Appliance', 'Power sum in Wh','value'], axis=1)
stamminger_F=pd.merge(wm,dw, on = ["hour","Country"])
stamminger_F.columns=['country', 'Appliance', 'Power sum in Wh', 'hour', 'value', 'S_WM','S_DW']  
stamminger_F=stamminger_F.drop(   ['Appliance','Power sum in Wh','value'],axis=1)
stamminger_F=pd.merge(stamminger_F,td, on = ["hour"])
    
#stamminger_F.to_csv(r'stamminger_11.23.csv')

########################
# create shares on the NUTS2 leve
# import code from s_wash.py
########################

# nhh used as reference for nutscodes
nhh = pd.read_csv('./openENTRANCE final data/nhhV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
# add data for Tumble Dryer, Washing Machine and Dish Washer; from Stamminger
#s_wash =pd.read_csv('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/stamminger_11.23.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
#s_wash=s_wash.drop(['Unnamed: 0'],axis=1)

temp = nhh[['nutscode']]
temp['country']= ""
for row in range(0,len(temp)):
    temp['country'][row] = temp['nutscode'][row][0:2]
temp = pd.merge(stamminger_F,temp, on = 'country',how = "outer")


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
time = list(range(0,24))*98 # 98 is the number of NUTS regions missing values
nafill['hour'] = time
# fill in the NA's with EU averages of Stamminger
# EU averages
EUWM = list(temp.loc[(temp['country'] == 'EU') ,'S_WM'])*98
EUTD = list(temp.loc[(temp['country'] == 'EU') ,'S_TD'])*98
EUDW = list(temp.loc[(temp['country'] == 'EU') ,'S_DW'])*98
nafill['S_WM'] = EUWM
nafill['S_DW'] = EUDW
nafill['S_TD'] = EUTD
#drop nas from dd. nafill has the nutscode
temp = temp.dropna()


# add nafill to temp
frames=[temp,nafill]
s_wash =pd.concat(frames,ignore_index=True)

os.chdir('./openENTRANCE final data')
s_wash.to_csv(r's_wash nuts_V2.csv', index = False)
