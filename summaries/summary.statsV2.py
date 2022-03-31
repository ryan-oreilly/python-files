# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:05:20 2022

@author: AK194059
"""
## Import packages
import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import matplotlib.pyplot as plt
import re

df = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/Full_potential.V6.country.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#

df_yr_sum = df.groupby(['region','variable'], as_index = False).sum()

df_yr_sum['type'] = ""
for row in range(0,600):
    print(row)
    df_yr_sum['type'][row] = df_yr_sum.variable[row][16:33]
    
df_yr_sum_red = df_yr_sum[df_yr_sum['type'] == 'Maximum Reduction']
df_yr_sum_red['device'] = ""
df_yr_sum_red = df_yr_sum_red.reset_index()
for row in range(0,300):
    print(row)
    df_yr_sum_red['device'][row] = df_yr_sum_red.variable[row][72:]
    
df_yr_sum_dis = df_yr_sum[df_yr_sum['type'] == 'Maximum Dispatch|']
df_yr_sum_dis['device'] = ""
df_yr_sum_dis = df_yr_sum_dis.reset_index()
for row in range(0,300):
    print(row)
    df_yr_sum_dis['device'][row] = df_yr_sum_dis.variable[row][71:]    

# create  df template
columns = []
for i in range(2018,2051):
    columns.append(str(i))
    
index_red = df_yr_sum_red[['region','device']]
index_dis = df_yr_sum_dis[['region','device']]  

# =============================================================================
# convert from representative hours to annual totals
# =============================================================================

conv = 365/12
total_year_red = df_yr_sum_red.iloc[0:300,3:36]*conv
total_year_red = index_red.join(total_year_red)
 
total_year_dis = df_yr_sum_dis.iloc[0:300,3:36]*conv
total_year_dis = index_dis.join(total_year_dis)

total_year_red.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/OE_validation/OE_data/Q_red_device_yearV2.csv')   

total_year_dis.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/OE_validation/OE_data/Q_dis_device_yearV2.csv')   


# annual demanded by country
country_yr_sum = df.groupby(['region'], as_index = False).sum()
country_yr_sum.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/OE_validation/OE_data/Q_country_yearV2.csv')   

# =============================================================================
# convert from representative hours to average reduction and discharge potentials
# =============================================================================
# average reduction potential

average_red_hour = df_yr_sum_red.iloc[0:300,3:36]/288
average_red_hour = index_red.join(average_red_hour)

# average increase potential - does not consider inc

average_dis_hour = df_yr_sum_dis.iloc[0:300,3:36]/288
average_dis_hour = index_dis.join(average_dis_hour)

average_red_hour.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/OE_validation/OE_data/Ave_red_device_yearV2.csv')   

average_dis_hour.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/OE_validation/OE_data/Ave_dis_device_yearV2.csv')   

del average_dis_hour
del average_red_hour
del df_yr_sum
del df_yr_sum_dis
del df_yr_sum_red

del index_dis
del index_red
del total_year_dis
del total_year_red




# vizualisations
#variables = df.variable.unique()
max_dis = ['Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Air Conditioning',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dish Washer',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dryer',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Electric Vehicle',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Refrigeration',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Storage Heater',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Washing Machine',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Water Heater',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Heat Pump',
       'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Circulation Pump']

max_red = ['Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Air Conditioning',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dish Washer',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dryer',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Electric Vehicle',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Refrigeration',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Storage Heater',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Washing Machine',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Water Heater',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Heat Pump',
       'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Circulation Pump']

country_profile_red = df[df['variable'].isin(max_red)]
country_profile_dis = df[df['variable'].isin(max_dis)]

# reduction only
"""
country_profile_red['device'] =""
country_profile_red['type'] = ""
for row in range(0,69120):
    print(row)
    country_profile_red['device'][row] = country_profile_red.variable[row][71:]
"""

country_profile_red_group = country_profile_red.groupby(['region','subannual'], as_index = False).sum()
sample_profile_red_group = country_profile_red.groupby(['variable','subannual'], as_index = False).sum()


AT = country_profile_red_group[country_profile_red_group['region'] == 'AT']
ATsub = AT[['subannual','2020','2030','2040','2050']]
ATsub.plot(subplots=True, figsize = (10,12))

NO = country_profile_red_group[country_profile_red_group['region'] == 'NO']
NOsub = NO[['subannual','2020','2030','2040','2050']]
NOsub.plot(subplots=True, figsize = (10,12))

EL = country_profile_red_group[country_profile_red_group['region'] == 'EL']
ELsub = EL[['subannual','2020','2030','2040','2050']]
ELsub.plot(subplots=True, figsize = (10,12))

for region in country_profile_red.region.unique():
    for year in ['2020','2030','2040','2050']:
        print(region+':   '+ year)
        temp_device = country_profile_red[country_profile_red['region'] == region]
        # country 2020
        temp_device2020 = temp_device[['subannual','variable',year]]
        
        pivoted_temp = temp_device2020.pivot(index = 'subannual', columns = 'variable')
        pivoted_temp.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']
        
        plt.stackplot(range(0,288), 
                      pivoted_temp['AC'],
                      pivoted_NO['CP'],  
                      pivoted_temp['DW'],
                      pivoted_temp['TD'],
                      pivoted_temp['EV'],
                      pivoted_temp['HP'],   
                      pivoted_temp['Ref'],
                      pivoted_temp['SH'],
                      pivoted_temp['WM'],
                      pivoted_temp['WH']
                      , labels = pivoted_temp.columns)
        #plt.ylim(0,max(temp_device[year]))
        plt.legend(loc='upper left')
        plt.title([str(region)+":  "+ year])    
        plt.show()
        
        
# =============================================================================
# Sample
# =============================================================================

# JUST HP
sample_HP_18 = sample_profile_red_group[['subannual','variable','2018']]
sample_HP_18['2018'] = sample_HP_18['2018']/1000
sample_HP_18 = sample_HP_18.pivot(index = 'subannual', columns = 'variable')
sample_HP_18.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']

plt.stackplot(range(0,288), 
              sample_HP_18['HP']           
              , labels = "HP")

# Sample 2020
sample_profile_red_group2020 = sample_profile_red_group[['subannual','variable','2020']]
sample_profile_red_group2020['2020'] = sample_profile_red_group2020['2020']/1000
sample_profile_red_group2020 = sample_profile_red_group2020.pivot(index = 'subannual', columns = 'variable')
sample_profile_red_group2020.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']

plt.stackplot(range(0,288), 
              sample_profile_red_group2020['AC'],
              sample_profile_red_group2020['CP'],              
              sample_profile_red_group2020['DW'],
              sample_profile_red_group2020['TD'],
              sample_profile_red_group2020['EV'],
              sample_profile_red_group2020['HP'],              
              sample_profile_red_group2020['Ref'],
              sample_profile_red_group2020['SH'],
              sample_profile_red_group2020['WM'],
              sample_profile_red_group2020['WH']
              , labels = sample_profile_red_group2020.columns)


plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
          fancybox=True, shadow=True, ncol=5)
plt.title('Sample: 2020 (GWh)')

# Sample 2030
sample_profile_red_group2030 = sample_profile_red_group[['subannual','variable','2030']]
sample_profile_red_group2030['2030'] = sample_profile_red_group2030['2030']/1000
sample_profile_red_group2030 = sample_profile_red_group2030.pivot(index = 'subannual', columns = 'variable')
sample_profile_red_group2030.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']

plt.stackplot(range(0,288), 
              sample_profile_red_group2030['AC'],
              sample_profile_red_group2030['CP'],              
              sample_profile_red_group2030['DW'],
              sample_profile_red_group2030['TD'],
              sample_profile_red_group2030['EV'],
              sample_profile_red_group2030['HP'],              
              sample_profile_red_group2030['Ref'],
              sample_profile_red_group2030['SH'],
              sample_profile_red_group2030['WM'],
              sample_profile_red_group2030['WH']
              , labels = sample_profile_red_group2030.columns)


plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
          fancybox=True, shadow=True, ncol=5)
plt.title('Sample: 2030')
# Sample 2040
sample_profile_red_group2040 = sample_profile_red_group[['subannual','variable','2040']]
sample_profile_red_group2040['2040'] = sample_profile_red_group2040['2040']/1000
sample_profile_red_group2040 = sample_profile_red_group2040.pivot(index = 'subannual', columns = 'variable')
sample_profile_red_group2040.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']

plt.stackplot(range(0,288), 
              sample_profile_red_group2040['AC'],
              sample_profile_red_group2040['CP'],              
              sample_profile_red_group2040['DW'],
              sample_profile_red_group2040['TD'],
              sample_profile_red_group2040['EV'],
              sample_profile_red_group2040['HP'],              
              sample_profile_red_group2040['Ref'],
              sample_profile_red_group2040['SH'],
              sample_profile_red_group2040['WM'],
              sample_profile_red_group2040['WH']
              , labels = sample_profile_red_group2040.columns)


plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
          fancybox=True, shadow=True, ncol=5)
plt.title('Sample: 2040 (GWh)')
# Sample 2050
sample_profile_red_group2050 = sample_profile_red_group[['subannual','variable','2050']]
sample_profile_red_group2050['2050'] = sample_profile_red_group2050['2050']/1000
sample_profile_red_group2050 = sample_profile_red_group2050.pivot(index = 'subannual', columns = 'variable')
sample_profile_red_group2050.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']

plt.stackplot(range(0,288), 
              sample_profile_red_group2050['AC'],
              sample_profile_red_group2050['CP'],              
              sample_profile_red_group2050['DW'],
              sample_profile_red_group2050['TD'],
              sample_profile_red_group2050['EV'],
              sample_profile_red_group2050['HP'],              
              sample_profile_red_group2050['Ref'],
              sample_profile_red_group2050['SH'],
              sample_profile_red_group2050['WM'],
              sample_profile_red_group2050['WH']
              , labels = sample_profile_red_group2050.columns)


plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
          fancybox=True, shadow=True, ncol=5)
plt.title('Sample: 2050 (GWh)')
# NO ALL DEVICES
# =============================================================================
# NORWAY
# =============================================================================

NO_device = country_profile_red[country_profile_red['region'] == 'NO']
# NORWAY 2020
NO_device2020 = NO_device[['subannual','variable','2020']]

pivoted_NO = NO_device2020.pivot(index = 'subannual', columns = 'variable')
pivoted_NO.columns=['AC','CP','DW', 'TD','EV','HP','Ref','SH','WM','WH']

plt.stackplot(range(0,288), 
              pivoted_NO['AC'],
              pivoted_NO['CP'],              
              pivoted_NO['DW'],
              pivoted_NO['TD'],
              pivoted_NO['EV'],
              pivoted_NO['HP'],              
              pivoted_NO['Ref'],
              pivoted_NO['SH'],
              pivoted_NO['WM'],
              pivoted_NO['WH']
              , labels = pivoted_NO.columns)
plt.ylim(0,7500)
plt.legend(loc='upper left')
plt.title('Norway: 2020')
# NORWAY 2020
NO_device2030 = NO_device[['subannual','variable','2030']]

pivoted_NO = NO_device2030.pivot(index = 'subannual', columns = 'variable')
pivoted_NO.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_NO['AC'],
              pivoted_NO['DW'],
              pivoted_NO['TD'],
              pivoted_NO['EV'],
              pivoted_NO['Ref'],
              pivoted_NO['SH'],
              pivoted_NO['WM'],
              pivoted_NO['WH']
              , labels = pivoted_NO.columns)
plt.ylim(0,5500)
plt.legend(loc='upper left')
plt.title('Norway: 2030')
# NORWAY 2040
NO_device2040 = NO_device[['subannual','variable','2040']]

pivoted_NO = NO_device2040.pivot(index = 'subannual', columns = 'variable')
pivoted_NO.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_NO['AC'],
              pivoted_NO['DW'],
              pivoted_NO['TD'],
              pivoted_NO['EV'],
              pivoted_NO['Ref'],
              pivoted_NO['SH'],
              pivoted_NO['WM'],
              pivoted_NO['WH']
              , labels = pivoted_NO.columns)
plt.ylim(0,5500)
plt.legend(loc='upper left')
plt.title('Norway: 2040')
# NORWAY 2050
NO_device2050 = NO_device[['subannual','variable','2050']]

pivoted_NO = NO_device2050.pivot(index = 'subannual', columns = 'variable')
pivoted_NO.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_NO['AC'],
              pivoted_NO['DW'],
              pivoted_NO['TD'],
              pivoted_NO['EV'],
              pivoted_NO['Ref'],
              pivoted_NO['SH'],
              pivoted_NO['WM'],
              pivoted_NO['WH']
              , labels = pivoted_NO.columns)
plt.ylim(0,5500)
plt.legend(loc='upper left')
plt.title('Norway: 2050')

# GERMANY
# =============================================================================

DE_device = country_profile_red[country_profile_red['region'] == 'DE']
# GERMANY 2020
DE_device2020 = DE_device[['subannual','variable','2020']]

pivoted_DE = DE_device2020.pivot(index = 'subannual', columns = 'variable')
pivoted_DE.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_DE['AC'],
              pivoted_DE['DW'],
              pivoted_DE['TD'],
              pivoted_DE['EV'],
              pivoted_DE['Ref'],
              pivoted_DE['SH'],
              pivoted_DE['WM'],
              pivoted_DE['WH']
              , labels = pivoted_DE.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('GERMANY: 2020')
# GERMANY 2030
DE_device2030 = DE_device[['subannual','variable','2030']]

pivoted_DE = DE_device2030.pivot(index = 'subannual', columns = 'variable')
pivoted_DE.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_DE['AC'],
              pivoted_DE['DW'],
              pivoted_DE['TD'],
              pivoted_DE['EV'],
              pivoted_DE['Ref'],
              pivoted_DE['SH'],
              pivoted_DE['WM'],
              pivoted_DE['WH']
              , labels = pivoted_DE.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('GERMANY: 2030')
# GERMANY 2040
DE_device2040 = DE_device[['subannual','variable','2040']]

pivoted_DE = DE_device2040.pivot(index = 'subannual', columns = 'variable')
pivoted_DE.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_DE['AC'],
              pivoted_DE['DW'],
              pivoted_DE['TD'],
              pivoted_DE['EV'],
              pivoted_DE['Ref'],
              pivoted_DE['SH'],
              pivoted_DE['WM'],
              pivoted_DE['WH']
              , labels = pivoted_DE.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('GERMANY: 2040')
# GERMANY 2050
DE_device2050 = DE_device[['subannual','variable','2050']]

pivoted_DE = DE_device2050.pivot(index = 'subannual', columns = 'variable')
pivoted_DE.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_DE['AC'],
              pivoted_DE['DW'],
              pivoted_DE['TD'],
              pivoted_DE['EV'],
              pivoted_DE['Ref'],
              pivoted_DE['SH'],
              pivoted_DE['WM'],
              pivoted_DE['WH']
              , labels = pivoted_DE.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('GERMANY: 2050')


# TURKEY
# =============================================================================

TR_device = country_profile_red[country_profile_red['region'] == 'TR']
# TURKEY 2020
TR_device2020 = TR_device[['subannual','variable','2020']]

pivoted_TR = TR_device2020.pivot(index = 'subannual', columns = 'variable')
pivoted_TR.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_TR['AC'],
              pivoted_TR['DW'],
              pivoted_TR['TD'],
              pivoted_TR['EV'],
              pivoted_TR['Ref'],
              pivoted_TR['SH'],
              pivoted_TR['WM'],
              pivoted_TR['WH']
              , labels = pivoted_TR.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('TURKEY: 2020')
# TURKEY 2030
TR_device2030 = TR_device[['subannual','variable','2030']]

pivoted_TR = TR_device2030.pivot(index = 'subannual', columns = 'variable')
pivoted_TR.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_TR['AC'],
              pivoted_TR['DW'],
              pivoted_TR['TD'],
              pivoted_TR['EV'],
              pivoted_TR['Ref'],
              pivoted_TR['SH'],
              pivoted_TR['WM'],
              pivoted_TR['WH']
              , labels = pivoted_TR.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('TURKEY: 2030')
# TURKEY 2040
TR_device2040 = TR_device[['subannual','variable','2040']]

pivoted_TR = TR_device2040.pivot(index = 'subannual', columns = 'variable')
pivoted_TR.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_TR['AC'],
              pivoted_TR['DW'],
              pivoted_TR['TD'],
              pivoted_TR['EV'],
              pivoted_TR['Ref'],
              pivoted_TR['SH'],
              pivoted_TR['WM'],
              pivoted_TR['WH']
              , labels = pivoted_TR.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('TURKEY: 2040')
# TURKEY 2050
TR_device2050 = TR_device[['subannual','variable','2050']]

pivoted_TR = TR_device2050.pivot(index = 'subannual', columns = 'variable')
pivoted_TR.columns=['AC','DW', 'TD','EV','Ref','SH','WM','WH']

plt.stackplot(range(0,288), pivoted_TR['AC'],
              pivoted_TR['DW'],
              pivoted_TR['TD'],
              pivoted_TR['EV'],
              pivoted_TR['Ref'],
              pivoted_TR['SH'],
              pivoted_TR['WM'],
              pivoted_TR['WH']
              , labels = pivoted_TR.columns)
plt.ylim(0,17500)
plt.legend(loc='upper left')
plt.title('TURKEY: 2050')
TR = country_profile_red_group[country_profile_red_group['region'] == 'TR']
TRsub = TR[['subannual','2020','2030','2040','2050']]
TRsub.plot(subplots=True, figsize = (10,12))





















# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 08:20:32 2022

@author: AK194059
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data\openENTRANCE final data')

# parameters
nhh = pd.read_csv('./nhhV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
# remove NAs - {'IS00', 'LI00', 'UKI1', 'UKI2', 'UKM2', 'UKM3'}
nhh = nhh.dropna()
nhh.index = nhh['nutscode']
# drop malta
nhh = nhh.drop(['MT00'], axis =0)
nhh = nhh.drop(['nutscode'], axis = 1)
nhh = nhh.reset_index()
nhh= nhh.sort_values('nutscode')

# add data for yr_hdd & yr_cdd
yr_hdd =pd.read_csv('./yr_hdd nutsV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
yr_cdd=pd.read_csv('./yr_cdd nutsV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

# rate of ownership
rwh = pd.read_csv('./rwh.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rsh = pd.read_csv('./rsh.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

"""
NFLH_WH = (YR_HDD/1000)*25+175
PUNIT_WH = 2                    # unit installed capacity; assumed constant across years kW
WUNIT_WH = NFLH_WH*PUNIT_WH     # annual electricity demand per unit of WH; kWh
W_WH = WUNIT_WH*NHH*RWH       
    
"""

NHH_AT = sum(nhh['2018'][0:9])
yr_hdd_AT = sum(yr_hdd['2018'][0:108])/len(yr_hdd['2018'][0:108])

NFLH_WH = (yr_hdd_AT/1000)*25+175
PUNIT_WH = 2
WUNIT_WH = NFLH_WH*PUNIT_WH 
RWH = 0.32
W_WH = WUNIT_WH*NHH_AT*RWH /1000 #Mwh
W_WH_Gwh = W_WH/1000 #Gwh



NFLH_SH = (yr_hdd_AT/1000)*150+200 
PUNIT_SH = 14   
WUNIT_SH = NFLH_SH*PUNIT_SH 
RSH = 0.04
W_SH = WUNIT_SH*NHH_AT*RSH /1000 #Mwh
W_SH_Gwh = W_SH/1000 #Gwh
