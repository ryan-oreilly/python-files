#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:27:34 2020

@author: ryanoreilly
This script will create the final dataframes that represent the parameter for all years and all regions
HR04 was split into HR05, HR06 and HR02
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os
import openpyxl as xl
from decimal import Decimal
### Set options
#os.chdir('I:\Projekte\OpenEntrance - WV0173\Durchführungsphase\WP6\CS1\gitlab\datainputs') # set wd - change to server path - IMPORTANT
os.chdir('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data')
## TEST TEST COMMMENT
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

# data that holds gils dissertaion assumptions about future varaibles
gils = pd.read_excel('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/openENTRANCE projection/gils projection assumptions.xlsx') 
gils = gils.sort_values(by = "country")
gils = gils.reset_index() 
gils = gils.drop('index', axis=1)

# regional household data for 2018 and 2019
dfnhh = pd.read_excel('/Users/ryanoreilly/Desktop/Energy Institute/openEntrance/data/number households/EUROSTAT Nuts 2 HH.xlsx') 
# make adjustements for Croatia
temp = dfnhh[dfnhh['nutscode']=="HR04"]
dfnhh = dfnhh[dfnhh.nutscode != 'HR04']
data = {'nutscode':["HR05","HR06","HR02"],
        'nhh_2018':[float(temp['nhh_2018']/3),float(temp['nhh_2018']/3),float(temp['nhh_2018']/3)],
        'nhh_2019':[float(temp['nhh_2019']/3),float(temp['nhh_2019']/3),float(temp['nhh_2019']/3)],
        'rNat_NHH':[float(temp['rNat_NHH']/3),float(temp['rNat_NHH']/3),float(temp['rNat_NHH']/3)],
        'country': ["HR","HR","HR"]}
temp2 = pd.DataFrame(data)
dfnhh = dfnhh.append(temp2)
# drop old nuts regions
dfnhh = dfnhh[dfnhh.nutscode != 'HU10']
dfnhh = dfnhh[dfnhh.nutscode != 'IE01']
dfnhh = dfnhh[dfnhh.nutscode != 'IE02']
dfnhh = dfnhh[dfnhh.nutscode != 'SI01']
dfnhh = dfnhh[dfnhh.nutscode != 'SI02']
dfnhh = dfnhh[dfnhh.nutscode != 'UKI1']
dfnhh = dfnhh[dfnhh.nutscode != 'UKI2']
dfnhh = dfnhh[dfnhh.nutscode != 'UKM2']
dfnhh = dfnhh[dfnhh.nutscode != 'UKM3']
dfnhh = dfnhh[dfnhh.nutscode != 'LT00']
dfnhh = dfnhh.reset_index() 
dfnhh = dfnhh.drop('index', axis=1)
#add norway and switzerland
norway     = pd.read_excel('./number households/norway households.xlsx')
switzerland= pd.read_excel('./number households/switzerland households.xlsx')
CHnutscode = pd.read_excel('./number households/CH code to nutscode.xlsx')
switzerland = switzerland.merge(CHnutscode,on = "Code")
switzerland = switzerland.groupby(['nutscode']).sum()
switzerland['nutscode']= switzerland.index

#concatinate df's
#add norway
frames=[dfnhh,norway]
dfnhh =pd.concat(frames,ignore_index=True)
#add Switzerland
frames=[dfnhh,switzerland]
dfnhh =pd.concat(frames,ignore_index=True)

#add country Acronym
dfnhh['country'] = ""
for row in range(0,len(dfnhh['nutscode'])):
    dfnhh['country'][row]=dfnhh['nutscode'][row][0:2]

del norway
del switzerland
del CHnutscode
dfnhh = dfnhh.sort_values(by = "nutscode")
dfnhh = dfnhh.reset_index() 
dfnhh = dfnhh.drop('index', axis=1)
#############
# nflh ac
#############
#gils = gils.drop('index', axis=1)
temp = gils[['country', 'nflh_ac_2010','nflh_ac_2020','nflh_ac_2030','nflh_ac_2050']]
temp['r10']= (temp['nflh_ac_2020']-temp['nflh_ac_2010'])/10
temp['r20']= (temp['nflh_ac_2030']-temp['nflh_ac_2020'])/10
temp['r30']= (temp['nflh_ac_2050']-temp['nflh_ac_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
nflh_ac = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(nflh_ac)):
    nflh_ac['2020'][row] = temp['nflh_ac_2020'][row]
    nflh_ac['2030'][row] = temp['nflh_ac_2030'][row]
    nflh_ac['2050'][row] = temp['nflh_ac_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(nflh_ac)):
    for _10 in range(0,2): # all years before 2020
        nflh_ac[columns[_10]][row] = round(temp['nflh_ac_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),0)
    for _20 in range(3,12):#  2020 < years < 2030
        nflh_ac[columns[_20]][row] = round(temp['nflh_ac_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),0)
    for _30 in range(13,32):
        nflh_ac[columns[_30]][row] = round(temp['nflh_ac_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),0)
                 

nflh_ac.to_csv(r'./openENTRANCE final data/nflh_ac.csv')  
del nflh_ac

#############
# nflh cp
#############
temp = gils[['country', 'nflh_cp_2010','nflh_cp_2020','nflh_cp_2030','nflh_cp_2050']]
temp['r10']= (temp['nflh_cp_2020']-temp['nflh_cp_2010'])/10
temp['r20']= (temp['nflh_cp_2030']-temp['nflh_cp_2020'])/10
temp['r30']= (temp['nflh_cp_2050']-temp['nflh_cp_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
nflh_cp = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(nflh_cp)):
    nflh_cp['2020'][row] = temp['nflh_cp_2020'][row]
    nflh_cp['2030'][row] = temp['nflh_cp_2030'][row]
    nflh_cp['2050'][row] = temp['nflh_cp_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(nflh_cp)):
    for _10 in range(0,2): # all years before 2020
        nflh_cp[columns[_10]][row] = round(temp['nflh_cp_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),0)
    for _20 in range(3,12):#  2020 < years < 2030
        nflh_cp[columns[_20]][row] = round(temp['nflh_cp_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),0)
    for _30 in range(13,32):
        nflh_cp[columns[_30]][row] = round(temp['nflh_cp_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),0)

nflh_cp.to_csv(r'./openENTRANCE final data/nflh_cp.csv')               
del nflh_cp

#############
#Begin wunit
#############

#############
#rf_fr
#############
temp = gils[['country',  'Wunit_rf_fr_2010', 'Wunit_rf_fr_2020', 'Wunit_rf_fr_2030', 'Wunit_rf_fr_2050']]
temp['r10']= (temp['Wunit_rf_fr_2020']-temp['Wunit_rf_fr_2010'])/10
temp['r20']= (temp['Wunit_rf_fr_2030']-temp['Wunit_rf_fr_2020'])/10
temp['r30']= (temp['Wunit_rf_fr_2050']-temp['Wunit_rf_fr_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
Wunit_rf_fr = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(Wunit_rf_fr)):
    Wunit_rf_fr['2020'][row] = temp['Wunit_rf_fr_2020'][row]
    Wunit_rf_fr['2030'][row] = temp['Wunit_rf_fr_2030'][row]
    Wunit_rf_fr['2050'][row] = temp['Wunit_rf_fr_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(Wunit_rf_fr)):
    for _10 in range(0,2): # all years before 2020
        Wunit_rf_fr[columns[_10]][row] = round(temp['Wunit_rf_fr_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),0)
    for _20 in range(3,12):#  2020 < years < 2030
        Wunit_rf_fr[columns[_20]][row] = round(temp['Wunit_rf_fr_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),0)
    for _30 in range(13,32):
        Wunit_rf_fr[columns[_30]][row] = round(temp['Wunit_rf_fr_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),0)

Wunit_rf_fr.to_csv(r'./openENTRANCE final data/Wunit_rf_fr.csv')               
del Wunit_rf_fr

#############
#Begin Pcycle
#############

#############
#Pcycle wm
#############
temp = gils[['country',  'Pcycle_wm_2010', 'Pcycle_wm_2020', 'Pcycle_wm_2030', 'Pcycle_wm_2050']]
temp['r10']= (temp['Pcycle_wm_2020']-temp['Pcycle_wm_2010'])/10
temp['r20']= (temp['Pcycle_wm_2030']-temp['Pcycle_wm_2020'])/10
temp['r30']= (temp['Pcycle_wm_2050']-temp['Pcycle_wm_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
Pcycle_wm = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(Pcycle_wm)):
    Pcycle_wm['2020'][row] = temp['Pcycle_wm_2020'][row]
    Pcycle_wm['2030'][row] = temp['Pcycle_wm_2030'][row]
    Pcycle_wm['2050'][row] = temp['Pcycle_wm_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(Pcycle_wm)):
    for _10 in range(0,2): # all years before 2020
        Pcycle_wm[columns[_10]][row] = round(temp['Pcycle_wm_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)
    for _20 in range(3,12):#  2020 < years < 2030
        Pcycle_wm[columns[_20]][row] = round(temp['Pcycle_wm_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),2)
    for _30 in range(13,32):
        Pcycle_wm[columns[_30]][row] = round(temp['Pcycle_wm_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),2)

Pcycle_wm.to_csv(r'./openENTRANCE final data/Pcycle_wm.csv')               
del Pcycle_wm

#############
#Pcycle td
#############
temp = gils[['country',  'Pcycle_td_2010', 'Pcycle_td_2020', 'Pcycle_td_2030', 'Pcycle_td_2050']]
temp['r10']= (temp['Pcycle_td_2020']-temp['Pcycle_td_2010'])/10
temp['r20']= (temp['Pcycle_td_2030']-temp['Pcycle_td_2020'])/10
temp['r30']= (temp['Pcycle_td_2050']-temp['Pcycle_td_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
Pcycle_td = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(Pcycle_td)):
    Pcycle_td['2020'][row] = temp['Pcycle_td_2020'][row]
    Pcycle_td['2030'][row] = temp['Pcycle_td_2030'][row]
    Pcycle_td['2050'][row] = temp['Pcycle_td_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(Pcycle_td)):
    for _10 in range(0,2): # all years before 2020
        Pcycle_td[columns[_10]][row] = round(temp['Pcycle_td_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)
    for _20 in range(3,12):#  2020 < years < 2030
        Pcycle_td[columns[_20]][row] = round(temp['Pcycle_td_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),2)
    for _30 in range(13,32):
        Pcycle_td[columns[_30]][row] = round(temp['Pcycle_td_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),2)

Pcycle_td.to_csv(r'./openENTRANCE final data/Pcycle_td.csv')               
del Pcycle_td



#############
#Pcycle dw
#############
temp = gils[['country',  'Pcycle_dw_2010', 'Pcycle_dw_2020', 'Pcycle_dw_2030', 'Pcycle_dw_2050']]
temp['r10']= (temp['Pcycle_dw_2020']-temp['Pcycle_dw_2010'])/10
temp['r20']= (temp['Pcycle_dw_2030']-temp['Pcycle_dw_2020'])/10
temp['r30']= (temp['Pcycle_dw_2050']-temp['Pcycle_dw_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
Pcycle_dw = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(Pcycle_dw)):
    Pcycle_dw['2020'][row] = temp['Pcycle_dw_2020'][row]
    Pcycle_dw['2030'][row] = temp['Pcycle_dw_2030'][row]
    Pcycle_dw['2050'][row] = temp['Pcycle_dw_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(Pcycle_dw)):
    for _10 in range(0,2): # all years before 2020
        Pcycle_dw[columns[_10]][row] = round(temp['Pcycle_dw_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)
    for _20 in range(3,12):#  2020 < years < 2030
        Pcycle_dw[columns[_20]][row] = round(temp['Pcycle_dw_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),2)
    for _30 in range(13,32):
        Pcycle_dw[columns[_30]][row] = round(temp['Pcycle_dw_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),2)

Pcycle_dw.to_csv(r'./openENTRANCE final data/Pcycle_dw.csv')               
del Pcycle_dw



#############
# Begin Punit
#############


#############
# Punit ac
#############
temp = gils[['country',  'Punit_ac_2010', 'Punit_ac_2020', 'Punit_ac_2030', 'Punit_ac_2050']]
temp['r10']= (temp['Punit_ac_2020']-temp['Punit_ac_2010'])/10
temp['r20']= (temp['Punit_ac_2030']-temp['Punit_ac_2020'])/10
temp['r30']= (temp['Punit_ac_2050']-temp['Punit_ac_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
Punit_ac = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(Punit_ac)):
    Punit_ac['2020'][row] = temp['Punit_ac_2020'][row]
    Punit_ac['2030'][row] = temp['Punit_ac_2030'][row]
    Punit_ac['2050'][row] = temp['Punit_ac_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(Punit_ac)):
    for _10 in range(0,2): # all years before 2020
        Punit_ac[columns[_10]][row] = round(temp['Punit_ac_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)
    for _20 in range(3,12):#  2020 < years < 2030
        Punit_ac[columns[_20]][row] = round(temp['Punit_ac_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),2)
    for _30 in range(13,32):
        Punit_ac[columns[_30]][row] = round(temp['Punit_ac_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),2)

Punit_ac.to_csv(r'./openENTRANCE final data/Punit_ac.csv')               
del Punit_ac



#############
# Punit cp
#############
temp = gils[['country',  'Punit_cp_2010', 'Punit_cp_2020', 'Punit_cp_2030', 'Punit_cp_2050']]
temp['r10']= (temp['Punit_cp_2020']-temp['Punit_cp_2010'])/10
temp['r20']= (temp['Punit_cp_2030']-temp['Punit_cp_2020'])/10
temp['r30']= (temp['Punit_cp_2050']-temp['Punit_cp_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
Punit_cp = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(Punit_cp)):
    Punit_cp['2020'][row] = temp['Punit_cp_2020'][row]
    Punit_cp['2030'][row] = temp['Punit_cp_2030'][row]
    Punit_cp['2050'][row] = temp['Punit_cp_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(Punit_cp)):
    for _10 in range(0,2): # all years before 2020
        Punit_cp[columns[_10]][row] = round(temp['Punit_cp_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)
    for _20 in range(3,12):#  2020 < years < 2030
        Punit_cp[columns[_20]][row] = round(temp['Punit_cp_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020)),2)
    for _30 in range(13,32):
        Punit_cp[columns[_30]][row] = round(temp['Punit_cp_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030)),2)

Punit_cp.to_csv(r'./openENTRANCE final data/Punit_cp.csv')               
del Punit_cp



#############
# Begin rates of ownership
#############


#############
# rfr
#############
temp = gils[['country',  'rfr_2010', 'rfr_2050']]
temp['r10']= (temp['rfr_2050']-temp['rfr_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rfr = pd.DataFrame(index = gils['country'], columns = columns)   

#fill in data for known years
for row in range(0,len(rfr)):
    rfr['2050'][row] = temp['rfr_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rfr)):
    for _10 in range(0,len(columns)): # 2018-2050
        rfr[columns[_10]][row] = round(temp['rfr_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rfr.to_csv(r'./openENTRANCE final data/rfr.csv')               
del rfr



#############
# rrf
#############
temp = gils[['country',  'rrf_2010', 'rrf_2050']]
temp['r10']= (temp['rrf_2050']-temp['rrf_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rrf = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rrf)):
    rrf['2050'][row] = temp['rrf_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rrf)):
    for _10 in range(0,len(columns)): # 2018-2050
        rrf[columns[_10]][row] = round(temp['rrf_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rrf.to_csv(r'./openENTRANCE final data/rrf.csv')               
del rrf


#############
# rwm
#############
temp = gils[['country',  'rwm_2010', 'rwm_2050']]
temp['r10']= (temp['rwm_2050']-temp['rwm_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rwm = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rwm)):
    rwm['2050'][row] = temp['rwm_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rwm)):
    for _10 in range(0,len(columns)): # 2018-2050
        rwm[columns[_10]][row] = round(temp['rwm_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rwm.to_csv(r'./openENTRANCE final data/rwm.csv')               
del rwm

#############
# rtd
#############
temp = gils[['country',  'rtd_2010', 'rtd_2050']]
temp['r10']= (temp['rtd_2050']-temp['rtd_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rtd = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rtd)):
    rtd['2050'][row] = temp['rtd_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rtd)):
    for _10 in range(0,len(columns)): # 2018-2050
        rtd[columns[_10]][row] = round(temp['rtd_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rtd.to_csv(r'./openENTRANCE final data/rtd.csv')               
del rtd

#############
# rdw
#############
temp = gils[['country',  'rdw_2010', 'rdw_2050']]
temp['r10']= (temp['rdw_2050']-temp['rdw_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rdw = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rdw)):
    rdw['2050'][row] = temp['rdw_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rdw)):
    for _10 in range(0,len(columns)): # 2018-2050
        rdw[columns[_10]][row] = round(temp['rdw_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rdw.to_csv(r'./openENTRANCE final data/rdw.csv')               
del rdw



#############
# rac
#############
temp = gils[['country',  'rac_2010', 'rac_2050']]
temp['r10']= (temp['rac_2050']-temp['rac_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rac = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rac)):
    rac['2050'][row] = temp['rac_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rac)):
    for _10 in range(0,len(columns)): # 2018-2050
        rac[columns[_10]][row] = round(temp['rac_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rac.to_csv(r'./openENTRANCE final data/rac.csv')               
del rac


#############
# rwh
#############
temp = gils[['country',  'rwh_2010', 'rwh_2050']]
temp['r10']= (temp['rwh_2050']-temp['rwh_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rwh = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rwh)):
    rwh['2050'][row] = temp['rwh_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rwh)):
    for _10 in range(0,len(columns)): # 2018-2050
        rwh[columns[_10]][row] = round(temp['rwh_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rwh.to_csv(r'./openENTRANCE final data/rwh.csv')               
del rwh

#############
# rcp
#############
temp = gils[['country',  'rcp_2010', 'rcp_2050']]
temp['r10']= (temp['rcp_2050']-temp['rcp_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rcp = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rcp)):
    rcp['2050'][row] = temp['rcp_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rcp)):
    for _10 in range(0,len(columns)): # 2018-2050
        rcp[columns[_10]][row] = round(temp['rcp_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rcp.to_csv(r'./openENTRANCE final data/rcp.csv')               
del rcp

#############
# rsh
#############
temp = gils[['country',  'rsh_2010', 'rsh_2050']]
temp['r10']= (temp['rsh_2050']-temp['rsh_2010'])/40

columns = []
for i in range(2018,2051):
    columns.append(str(i))
rsh = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(rsh)):
    rsh['2050'][row] = temp['rsh_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(rsh)):
    for _10 in range(0,len(columns)): # 2018-2050
        rsh[columns[_10]][row] = round(temp['rsh_2010'][row]+(temp['r10'][row]*(int(columns[_10])-2010)),2)

rsh.to_csv(r'./openENTRANCE final data/rsh.csv')               
del rsh

#############
# sreduction & sincrease
#############


#############
# sred_wm
#############
temp = gils[['country',  'sred_wm_2020', 'sred_wm_2030','sred_wm_2050']]
temp['r20']= (temp['sred_wm_2030']-temp['sred_wm_2020'])/10
temp['r30']= (temp['sred_wm_2050']-temp['sred_wm_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sred_wm = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sred_wm)):
    sred_wm['2020'][row] = temp['sred_wm_2020'][row]
    sred_wm['2030'][row] = temp['sred_wm_2030'][row]
    sred_wm['2050'][row] = temp['sred_wm_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sred_wm)):
    for _10 in range(1,-1,-1): # all years before 2020
        sred_wm[columns[_10]][row] = temp['sred_wm_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sred_wm[columns[_20]][row] = temp['sred_wm_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sred_wm[columns[_30]][row] = temp['sred_wm_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))

sred_wm.to_csv(r'./openENTRANCE final data/sred_wm.csv')               
del sred_wm



#############
# sinc_wm
#############
temp = gils[['country',  'sinc_wm_2020', 'sinc_wm_2030','sinc_wm_2050']]
temp['r20']= (temp['sinc_wm_2030']-temp['sinc_wm_2020'])/10
temp['r30']= (temp['sinc_wm_2050']-temp['sinc_wm_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sinc_wm = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sinc_wm)):
    sinc_wm['2020'][row] = temp['sinc_wm_2020'][row]
    sinc_wm['2030'][row] = temp['sinc_wm_2030'][row]
    sinc_wm['2050'][row] = temp['sinc_wm_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sinc_wm)):
    for _10 in range(1,-1,-1): # all years before 2020
        sinc_wm[columns[_10]][row] = temp['sinc_wm_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sinc_wm[columns[_20]][row] = temp['sinc_wm_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sinc_wm[columns[_30]][row] = temp['sinc_wm_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))

sinc_wm.to_csv(r'./openENTRANCE final data/sinc_wm.csv')               
del sinc_wm


#############
# sred_td
#############
temp = gils[['country',  'sred_td_2020', 'sred_td_2030','sred_td_2050']]
temp['r20']= (temp['sred_td_2030']-temp['sred_td_2020'])/10
temp['r30']= (temp['sred_td_2050']-temp['sred_td_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sred_td = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sred_td)):
    sred_td['2020'][row] = temp['sred_td_2020'][row]
    sred_td['2030'][row] = temp['sred_td_2030'][row]
    sred_td['2050'][row] = temp['sred_td_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sred_td)):
    for _10 in range(1,-1,-1): # all years before 2020
        sred_td[columns[_10]][row] = temp['sred_td_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sred_td[columns[_20]][row] = temp['sred_td_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sred_td[columns[_30]][row] = temp['sred_td_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))
        
        
sred_td.to_csv(r'./openENTRANCE final data/sred_td.csv')               
del sred_td


 
#############
# sinc_td
#############
temp = gils[['country',  'sinc_td_2020', 'sinc_td_2030','sinc_td_2050']]
temp['r20']= (temp['sinc_td_2030']-temp['sinc_td_2020'])/10
temp['r30']= (temp['sinc_td_2050']-temp['sinc_td_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sinc_td = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sinc_td)):
    sinc_td['2020'][row] = temp['sinc_td_2020'][row]
    sinc_td['2030'][row] = temp['sinc_td_2030'][row]
    sinc_td['2050'][row] = temp['sinc_td_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sinc_td)):
    for _10 in range(1,-1,-1): # all years before 2020
        sinc_td[columns[_10]][row] = temp['sinc_td_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sinc_td[columns[_20]][row] = temp['sinc_td_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sinc_td[columns[_30]][row] = temp['sinc_td_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))
        
        
sinc_td.to_csv(r'./openENTRANCE final data/sinc_td.csv')               
del sinc_td



#############
# sred_dw
#############
temp = gils[['country',  'sred_dw_2020', 'sred_dw_2030','sred_dw_2050']]
temp['r20']= (temp['sred_dw_2030']-temp['sred_dw_2020'])/10
temp['r30']= (temp['sred_dw_2050']-temp['sred_dw_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sred_dw = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sred_dw)):
    sred_dw['2020'][row] = temp['sred_dw_2020'][row]
    sred_dw['2030'][row] = temp['sred_dw_2030'][row]
    sred_dw['2050'][row] = temp['sred_dw_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sred_dw)):
    for _10 in range(1,-1,-1): # all years before 2020
        sred_dw[columns[_10]][row] = temp['sred_dw_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sred_dw[columns[_20]][row] = temp['sred_dw_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sred_dw[columns[_30]][row] = temp['sred_dw_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))
        
        
sred_dw.to_csv(r'./openENTRANCE final data/sred_dw.csv')               
del sred_dw


#############
# sinc_dw
#############
temp = gils[['country',  'sinc_dw_2020', 'sinc_dw_2030','sinc_dw_2050']]
temp['r20']= (temp['sinc_dw_2030']-temp['sinc_dw_2020'])/10
temp['r30']= (temp['sinc_dw_2050']-temp['sinc_dw_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sinc_dw = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sinc_dw)):
    sinc_dw['2020'][row] = temp['sinc_dw_2020'][row]
    sinc_dw['2030'][row] = temp['sinc_dw_2030'][row]
    sinc_dw['2050'][row] = temp['sinc_dw_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sinc_dw)):
    for _10 in range(1,-1,-1): # all years before 2020
        sinc_dw[columns[_10]][row] = temp['sinc_dw_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sinc_dw[columns[_20]][row] = temp['sinc_dw_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sinc_dw[columns[_30]][row] = temp['sinc_dw_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))
        
        
sinc_dw.to_csv(r'./openENTRANCE final data/sinc_dw.csv')               
del sinc_dw


#############
# sred_ac
#############
temp = gils[['country',  'sred_ac_2020', 'sred_ac_2030','sred_ac_2050']]
temp['r20']= (temp['sred_ac_2030']-temp['sred_ac_2020'])/10
temp['r30']= (temp['sred_ac_2050']-temp['sred_ac_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sred_ac = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sred_ac)):
    sred_ac['2020'][row] = temp['sred_ac_2020'][row]
    sred_ac['2030'][row] = temp['sred_ac_2030'][row]
    sred_ac['2050'][row] = temp['sred_ac_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sred_ac)):
    for _10 in range(1,-1,-1): # all years before 2020
        sred_ac[columns[_10]][row] = temp['sred_ac_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sred_ac[columns[_20]][row] = temp['sred_ac_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sred_ac[columns[_30]][row] = temp['sred_ac_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))
        
        
sred_ac.to_csv(r'./openENTRANCE final data/sred_ac.csv')               
del sred_ac



#############
# sred_cp
#############
temp = gils[['country',  'sred_cp_2020', 'sred_cp_2030','sred_cp_2050']]
temp['r20']= (temp['sred_cp_2030']-temp['sred_cp_2020'])/10
temp['r30']= (temp['sred_cp_2050']-temp['sred_cp_2030'])/20

columns = []
for i in range(2018,2051):
    columns.append(str(i))
sred_cp = pd.DataFrame(index = gils['country'], columns = columns)  

#fill in data for known years
for row in range(0,len(sred_cp)):
    sred_cp['2020'][row] = temp['sred_cp_2020'][row]
    sred_cp['2030'][row] = temp['sred_cp_2030'][row]
    sred_cp['2050'][row] = temp['sred_cp_2050'][row]
    
# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(sred_cp)):
    for _10 in range(1,-1,-1): # all years before 2020
        sred_cp[columns[_10]][row] = temp['sred_cp_2020'][row]+(temp['r20'][row]*(int(columns[_10])-2020))
    for _20 in range(3,12):#  2020 < years < 2030
        sred_cp[columns[_20]][row] = temp['sred_cp_2020'][row]+(temp['r20'][row]*(int(columns[_20])-2020))
    for _30 in range(13,32):
        sred_cp[columns[_30]][row] = temp['sred_cp_2030'][row]+(temp['r30'][row]*(int(columns[_30])-2030))
        
        
sred_cp.to_csv(r'./openENTRANCE final data/sred_cp.csv')               
del sred_cp



#############
# NHH to regional NHH projections
#############


#############
# nhh
#############
# gils is missing Serbia, Masedonia, Montenegro while Household data file does not have lichtenstein
# I need to merge the two to get the final list of nuts 2 regions to be used in the loop below
temp1 = dfnhh
temp2 = gils[['country','nhh_2010','nhh_2020', 'nhh_2030', 'nhh_2050']]
temp3 = temp2.merge(temp1)
temp3 = temp3.reset_index() 
temp3 = temp3.drop('index', axis=1)
temp3['nhh30'] =temp3['nhh_2030']*temp3['rNat_NHH']*10**6
temp3['nhh50'] =temp3['nhh_2050']*temp3['rNat_NHH']*10**6
del temp1
del temp2

columns = []
for i in range(2018,2051):
    columns.append(str(i))
nhh = pd.DataFrame(index = temp3['nutscode'], columns = columns)  


country_list =np.unique(temp3['country']) #countries used in the analysis

cntry_nuts = {} # countries nuts codes or regions
for i in country_list: 
    temp_df = temp3[temp3['country']== i]
    cntry_nuts[i] = np.unique(temp_df['nutscode'])
        
#fill in data for known years
for row in range(0,len(nhh)):
    nhh['2018'][row] = temp3['nhh_2018'][row]
    nhh['2019'][row] = temp3['nhh_2019'][row]
    nhh['2030'][row] = temp3['nhh30'][row]
    nhh['2050'][row] = temp3['nhh50'][row]
   
temp3['r19']= ((temp3['nhh30']-temp3['nhh_2019'])/11)
temp3['r30']= ((temp3['nhh50']-temp3['nhh30'])/20)


# use linear growth function to find data for unknown years pv+growth*(t present - t beginning))
for row in range(0,len(temp3)):
    for _20 in range(2,12):#  2020 < years < 2030
        nhh[columns[_20]][row] = nhh['2019'][row]+(temp3['r19'][row]*(int(columns[_20])-2019))
    for _30 in range(13,32):
        nhh[columns[_30]][row] = nhh['2030'][row]+(temp3['r30'][row]*(int(columns[_30])-2030))
        



nhh.to_csv(r'./openENTRANCE final data/nhh.csv')               











