# -*- coding: utf-8 -*-
"""
projection of HP thermal  energy demand 
assumes a linear decomposition of non RE non EE heating products thermal energy into HP thermal energy demand

"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os
import openpyxl as xl


# read in assumptions for HP
df = pd.read_csv("I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/HP_transition.csv", sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
df.HP_thermal_2019[df.country =="CH"] = df.HP_thermal_2018[df.country =="CH"]
df.columns = ('#', 'country', 'final_energy_15-19',
       'final_energy_15-19_nonEE', 'Total_nonEE_thermal',
       'final_energy_15-19_nonEE_share', 'HP_thermal_2018', 'HP_thermal_2019', 'MWh')
df['add'] = df.Total_nonEE_thermal/(2050-2019)



# df that represents the future thermal energy provision assuming thermal requirements remain constant between 2018 and 2050
df_final = df[['country','HP_thermal_2019']]

index = df.country
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_HP = pd.DataFrame(index = index, columns = columns)  

d_HP['2018'] = list(df.HP_thermal_2018)
d_HP['2019'] = list(df.HP_thermal_2019)

for NUTS0 in range(0, len(df.country)):
    for year in range(2, len(columns)):
        prev = int(year)-1
        d_HP.iloc[NUTS0,year] = d_HP.iloc[NUTS0,prev] +df['add'][NUTS0]
        
# distribute thermal energy provision across NUTS2 regions based on #HH in the respective regions

nhh = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data\openENTRANCE final data/nhhV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
# remove NAs - {'IS00', 'LI00', 'UKI1', 'UKI2', 'UKM2', 'UKM3'}
nhh = nhh.dropna()
nhh = nhh.reset_index()
nhh = nhh[['nutscode','2018']]

nhh['country'] = ""
for nuts2 in range(0, len(nhh['nutscode'])):
    nhh['country'][nuts2] = nhh['nutscode'][nuts2][0:2]

cntry_tot = nhh.groupby(['country']).sum()    
cntry_tot = cntry_tot.reset_index()
cntry_tot.columns = ("country","NUTS0_HH")


nhhV2 = pd.merge(nhh, cntry_tot)
nhhV2['HH_share'] = nhhV2['2018']/nhhV2['NUTS0_HH']

#This will be done in the final script that converts to hourly energy demand
# convert to final energy demand using COP of the respective regions 
#cop = pd.read_csv("I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/temperature/NUTS2_2011_2021_tgmean.csv",sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

#cop = cop[['Unnamed: 0','Average COP']]    
#cop.columns = ('nutscode','COP')
#cop.nutscode[cop.nutscode == 'Dec-00'] = "DEC0"

#set(cop.nutscode) - set(nhh.nutscode)

#combine hh share and cop

#df_combined = nhhV2.merge(cop,'left')
#df_combined['COP'] = df_combined['COP'].astype(float)

# convert NUTS0 thermal provision to NUTS2 energy provision

index = nhhV2.nutscode
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_HP2 = pd.DataFrame(index = index, columns = columns)  
for nuts in range(0,len(nhhV2.nutscode)):
    nuts2 = nhhV2.nutscode[nuts]
    nuts0 = nhhV2.country[nuts]
    #temp_COP = df_combined['COP'][nuts]
    temp_country = list(d_HP.loc[nuts0]) 
    temp_share = nhhV2['HH_share'][nuts]
    for year in range(0,d_HP2.shape[1]):
        d_HP2.iloc[nuts,year] = temp_country[year]*temp_share
        
        
d_HP2.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/openENTRANCE final data/Qhp_thermal_MWh_projected.csv')  
        
        
        
        
        
        
        
        
        
        
        