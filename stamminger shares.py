#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:11:20 2020

@author: ryanoreilly
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os

#the objective of this file is to get the stamminger file in a working format compatible with the demand potential py fle
#os.chdir('I:\Projekte\OpenEntrance - WV0173\Durchführungsphase\WP6\CS1\gitlab\datainputs') # set wd - change to server path - IMPORTANT
os.chdir('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data')
## TEST TEST COMMMENT
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

#read in file
stamminger =pd.read_excel('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/flexibilities file reference/stamminger.xlsx')
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
    
stamminger_F.to_csv(r'stamminger_11.23.csv')
