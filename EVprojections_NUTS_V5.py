#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:59:02 2020

@author: ryanoreilly

The objective of this script is to take the national EV projections and convert them to regional projections

Note: NUTSCODE HR04 is divided equally into HR02, HR05, HR06
      NUTSCODE Norway
                      NO01 -> NO08
                      NO02 -> NO02
                      NO03 -> NO09
                      NO04 -> NO09
                      NO05 -> NO0A
                      NO06 -> NO06
                      NO07 -> NO07
                      https://ec.europa.eu/eurostat/databrowser/view/TRAN_R_VEHST/default/map?lang=en
                      https://ec.europa.eu/eurostat/documents/345175/7451602/2021-NUTS-2-map-NO.pdf
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os
import openpyxl as xl
### Set options
#os.chdir('I:\Projekte\OpenEntrance - WV0173\Durchführungsphase\WP6\CS1\gitlab\datainputs') # set wd - change to server path - IMPORTANT
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data')
## TEST TEST COMMMENT
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format


#########################################
#EV projections for countries
#########################################
df = pd.read_csv('./EV projectionsV5_ave.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False)

#########################################
# NUTS 2 regional share of national vehicle fleet
#########################################
dfnuts = pd.read_excel('./openENTRANCE projection/Euro_Stat - vehicle ownership/Eurostat - Vehicle Nuts.xlsx', index_col=False)
dfnuts = dfnuts[['nutscode','rVS']]
dfnuts['country'] = ""
for i in range(0,len(dfnuts['country'])):
    dfnuts['country'][i] = dfnuts['nutscode'][i][0:2]
    
# make adjustements for Croatia - HR04 is split equally into HR05, HR06, and HR02
temp = dfnuts[dfnuts['nutscode']=="HR04"]
dfnuts = dfnuts[dfnuts.nutscode != 'HR04']
data = {'nutscode':["HR05","HR06","HR02"],
        'rVS':[float(temp['rVS']/3),float(temp['rVS']/3),float(temp['rVS']/3)],
        'country': ["HR","HR","HR"]}
temp2 = pd.DataFrame(data)
dfnuts = dfnuts.append(temp2)
dfnuts = dfnuts.reset_index() 
dfnuts = dfnuts.drop('index', axis=1)


dfnuts = dfnuts.reset_index() 
dfnuts = dfnuts.drop('index', axis=1)

#########################################
#check nuts
#########################################
"""
nhh = pd.read_csv('./openENTRANCE final data/nhhV2.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False)

#identify differences between NUTS 2 sets
carset = set(dfnuts.nutscode)
hhset = set(nhh.nutscode)

hhset -carset

carset -hhset
del carset
del hhset

"""
#########################################
#create df to be filled in
#########################################

df = df.merge(dfnuts, on='country')
for nuts in range(0,df.shape[0]):
    for year in range(1,df.shape[1]-2):
        df.iloc[nuts,year] = round(df['rVS'][nuts]*df.iloc[nuts,year],0)
        
df = df.drop('rVS',axis =1)        
df.to_csv(r'EV NUTS projectionsV5.csv')  
