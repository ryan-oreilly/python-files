# -*- coding: utf-8 -*-
"""
Estimation of average pincrease
"""

### BEGIN - global options ###
## Import packages
import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os
pip install country-converter
import country_converter as coco

### Set options
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/')

# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
### END - global options
### Load in data
d_WM = pd.read_csv('./d_WMV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_WH = pd.read_csv('./d_WHV7.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_TD = pd.read_csv('./d_TDV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_SH = pd.read_csv('./d_SHV7.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_DW = pd.read_csv('./d_DWV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
d_HP = pd.read_csv('./d_HPV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#

p_WM = pd.read_csv('./p_WMV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_WH = pd.read_csv('./p_WHV7.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_SH = pd.read_csv('./p_SHV7.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_DW = pd.read_csv('./p_DWV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_TD = pd.read_csv('./p_TDV6.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
p_HP = pd.read_csv('./p_HPV4.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#

# sort all dataframes
d_WM = d_WM.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_WH = d_WH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_TD = d_TD.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_SH = d_SH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_DW = d_DW.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
d_HP = d_HP.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)


p_WM = p_WM.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_WH = p_WH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_SH = p_SH.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_DW = p_DW.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_TD = p_TD.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)
p_HP = p_HP.sort_values(['nutscode', 'TIME','hour'],ignore_index=True)


# read in metadata
df1 = pd.read_excel('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis\openEntrance/data/theoretical potential/metaData.TheoreticalV8.xlsx', 'energy shift constraints ')
df2 = df1.iloc[0:9,0:3]
df2['DLC_move'] = ""
df2['DLC_move'][df2['Demand Response Measure'] =="Delay"] = "Delay"
df2['DLC_move'][df2['Demand Response Measure'] =="Advance"] = "Advance"
df2['DLC_move'][df2['Demand Response Measure'] =="Delay and Advance"] = "Both"

# days per month
_31 = ['2018M01','2018M03','2018M05','2018M07','2018M08','2018M10','2018M12']
_30 = ['2018M04','2018M06','2018M09','2018M11']

# calc pincrease for WM
columns = []
for i in range(2018,2051):
    columns.append(str(i))
p_inc_WM = pd.DataFrame(index = set(d_WM.nutscode), columns = columns)   

t_shift = int(df2['t.shift'][df2['Appliance']=='Washing Machine'])
for region in set(d_WM.nutscode):
    print(region)
    temp_df = d_WM[d_WM['nutscode'] == region]
    max_dispatch = p_WM[p_WM['nutscode'] == region]
    for year in list(p_inc_WM):
        print(year)
        temp_year = temp_df[['hour','TIME',year]]
        temp_year_final =pd.DataFrame()
        max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
        for month in set(temp_year['TIME']):
            #print(month)
            temp_month = temp_year[temp_year['TIME'] == month]
            if month in _31: #expansion of the data set to prevent issues from between days
                temp_month_exp = [temp_month]*31
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            elif month in _30:
                temp_month_exp = [temp_month]*30
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            else:
                temp_month_exp = [temp_month]*28
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
        temp_year_final = temp_year_final.sort_values(['TIME','day','hour'],ignore_index=True)
        for hour in range(0,temp_year_final.shape[0]):
            #print(hour)
            count = 0
            while (hour+count+1<8760) and (temp_year_final[year][hour]+temp_year_final[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
                #print(count)
                count = count +1
                temp_year_final[year][hour] = temp_year_final[year][hour]+temp_year_final[year][hour+count]
                #if hour+count >= temp_year_final.shape[0]-3 and hour != temp_year_final.shape[0]: # the last observation
                    #print('here')
                 #   break
        p_inc_WM[year][region] = temp_year_final[year][0:len(temp_year_final[year])-t_shift].mean()
p_inc_WM['country'] = ""

for  row in range(0,len(p_inc_WM.index)):
   p_inc_WM['country'][row] =  p_inc_WM.index[row][0:2]   
     
p_inc_WM.to_csv(r'./P_inc/P_inc_WM.csv')       
# calc pincrease for DW
columns = []
for i in range(2018,2051):
    columns.append(str(i))
p_inc_DW = pd.DataFrame(index = set(d_DW.nutscode), columns = columns)   

t_shift = int(df2['t.shift'][df2['Appliance']=='Dish Washer'])
for region in set(d_DW.nutscode):
    print(region)
    temp_df = d_DW[d_DW['nutscode'] == region]
    max_dispatch = p_DW[p_DW['nutscode'] == region]
    for year in list(p_inc_DW):
        print(year)
        temp_year = temp_df[['hour','TIME',year]]
        temp_year_final =pd.DataFrame()
        max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
        for month in set(temp_year['TIME']):
            #print(month)
            temp_month = temp_year[temp_year['TIME'] == month]
            if month in _31: #expansion of the data set to prevent issues from between days
                temp_month_exp = [temp_month]*31
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            elif month in _30:
                temp_month_exp = [temp_month]*30
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            else:
                temp_month_exp = [temp_month]*28
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
        temp_year_final = temp_year_final.sort_values(['TIME','day','hour'],ignore_index=True)
        for hour in range(0,temp_year_final.shape[0]):
            #print(hour)
            count = 0
            while (hour+count+1<8760) and (temp_year_final[year][hour]+temp_year_final[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
                #print(count)
                count = count +1
                temp_year_final[year][hour] = temp_year_final[year][hour]+temp_year_final[year][hour+count]
                #if hour+count >= temp_year_final.shape[0]-3 and hour != temp_year_final.shape[0]: # the last observation
                    #print('here')
                 #   break
        p_inc_DW[year][region] = temp_year_final[year][0:len(temp_year_final[year])-t_shift].mean()
p_inc_DW['country'] = ""

for  row in range(0,len(p_inc_DW.index)):
   p_inc_DW['country'][row] =  p_inc_DW.index[row][0:2]        
p_inc_DW.to_csv(r'./P_inc/P_inc_DW.csv') 
      
# calc pincrease for TD
columns = []
for i in range(2018,2051):
    columns.append(str(i))
p_inc_TD = pd.DataFrame(index = set(d_TD.nutscode), columns = columns)   

t_shift = int(df2['t.shift'][df2['Appliance']=='Dryer'])
for region in set(d_TD.nutscode):
    print(region)
    temp_df = d_TD[d_TD['nutscode'] == region]
    max_dispatch = p_TD[p_TD['nutscode'] == region]
    for year in list(p_inc_TD):
        print(year)
        temp_year = temp_df[['hour','TIME',year]]
        temp_year_final =pd.DataFrame()
        max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
        for month in set(temp_year['TIME']):
            #print(month)
            temp_month = temp_year[temp_year['TIME'] == month]
            if month in _31: #expansion of the data set to prevent issues from between days
                temp_month_exp = [temp_month]*31
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            elif month in _30:
                temp_month_exp = [temp_month]*30
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            else:
                temp_month_exp = [temp_month]*28
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
        temp_year_final = temp_year_final.sort_values(['TIME','day','hour'],ignore_index=True)
        for hour in range(0,temp_year_final.shape[0]):
            #print(hour)
            count = 0
            while (hour+count+1<8760) and (temp_year_final[year][hour]+temp_year_final[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
                #print(count)
                count = count +1
                temp_year_final[year][hour] = temp_year_final[year][hour]+temp_year_final[year][hour+count]
                #if hour+count >= temp_year_final.shape[0]-3 and hour != temp_year_final.shape[0]: # the last observation
                    #print('here')
                 #   break
        p_inc_TD[year][region] = temp_year_final[year][0:len(temp_year_final[year])-t_shift].mean()
p_inc_TD['country'] = ""

for  row in range(0,len(p_inc_TD.index)):
   p_inc_TD['country'][row] =  p_inc_TD.index[row][0:2]
p_inc_TD.to_csv(r'./P_inc/P_inc_TD.csv')                   
        

# calc pincrease for SH
columns = []
for i in range(2018,2051):
    columns.append(str(i))
p_inc_SH = pd.DataFrame(index = set(d_SH.nutscode), columns = columns)   

t_shift = int(df2['t.shift'][df2['Appliance']=='Storage Heater'])
for region in set(d_SH.nutscode):
    print(region)
    temp_df = d_SH[d_SH['nutscode'] == region]
    max_dispatch = p_SH[p_SH['nutscode'] == region]
    for year in list(p_inc_SH):
        print(year)
        temp_year = temp_df[['hour','TIME',year]]
        temp_year_final =pd.DataFrame()
        max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
        for month in set(temp_year['TIME']):
            #print(month)
            temp_month = temp_year[temp_year['TIME'] == month]
            if month in _31: #expansion of the data set to prevent issues from between days
                temp_month_exp = [temp_month]*31
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            elif month in _30:
                temp_month_exp = [temp_month]*30
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            else:
                temp_month_exp = [temp_month]*28
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
        temp_year_final = temp_year_final.sort_values(['TIME','day','hour'],ignore_index=True)
        for hour in range(0,temp_year_final.shape[0]):
            #print(hour)
            count = 0
            while (hour+count+1<8760) and (temp_year_final[year][hour]+temp_year_final[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
                #print(count)
                count = count +1
                temp_year_final[year][hour] = temp_year_final[year][hour]+temp_year_final[year][hour+count]
                #if hour+count >= temp_year_final.shape[0]-3 and hour != temp_year_final.shape[0]: # the last observation
                    #print('here')
                 #   break
        p_inc_SH[year][region] = temp_year_final[year][0:len(temp_year_final[year])-t_shift].mean()
p_inc_SH['country'] = ""

for  row in range(0,len(p_inc_SH.index)):
   p_inc_SH['country'][row] =  p_inc_SH.index[row][0:2]
p_inc_SH.to_csv(r'./P_inc/P_inc_SH.csv')                   

# calc pincrease for WH
columns = []
for i in range(2018,2051):
    columns.append(str(i))
p_inc_WH = pd.DataFrame(index = set(d_WH.nutscode), columns = columns)   

t_shift = int(df2['t.shift'][df2['Appliance']=='Water Heater'])
for region in set(d_WH.nutscode):
    print(region)
    temp_df = d_WH[d_WH['nutscode'] == region]
    max_dispatch = p_WH[p_WH['nutscode'] == region]
    for year in list(p_inc_WH):
        print(year)
        temp_year = temp_df[['hour','TIME',year]]
        temp_year_final =pd.DataFrame()
        max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
        for month in set(temp_year['TIME']):
            #print(month)
            temp_month = temp_year[temp_year['TIME'] == month]
            if month in _31: #expansion of the data set to prevent issues from between days
                temp_month_exp = [temp_month]*31
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            elif month in _30:
                temp_month_exp = [temp_month]*30
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            else:
                temp_month_exp = [temp_month]*28
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
        temp_year_final = temp_year_final.sort_values(['TIME','day','hour'],ignore_index=True)
        for hour in range(0,temp_year_final.shape[0]):
            #print(hour)
            count = 0
            while (hour+count+1<8760) and (temp_year_final[year][hour]+temp_year_final[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
                #print(count)
                count = count +1
                temp_year_final[year][hour] = temp_year_final[year][hour]+temp_year_final[year][hour+count]
                #if hour+count >= temp_year_final.shape[0]-3 and hour != temp_year_final.shape[0]: # the last observation
                    #print('here')
                 #   break
        p_inc_WH[year][region] = temp_year_final[year][0:len(temp_year_final[year])-t_shift].mean()
p_inc_WH['country'] = ""

for  row in range(0,len(p_inc_WH.index)):
   p_inc_WH['country'][row] =  p_inc_WH.index[row][0:2]
p_inc_WH.to_csv(r'./P_inc/P_inc_WH.csv')       

# calc pincrease for HP
columns = []
for i in range(2018,2051):
    columns.append(str(i))
p_inc_HP = pd.DataFrame(index = set(d_HP.nutscode), columns = columns)   

t_shift = 3
for region in set(d_HP.nutscode):
    print(region)
    temp_df = d_HP[d_HP['nutscode'] == region]
    max_dispatch = p_HP[p_HP['nutscode'] == region]
    for year in list(p_inc_HP):
        print(year)
        temp_year = temp_df[['hour','TIME',year]]
        temp_year_final =pd.DataFrame()
        max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
        for month in set(temp_year['TIME']):
            #print(month)
            temp_month = temp_year[temp_year['TIME'] == month]
            if month in _31: #expansion of the data set to prevent issues from between days
                temp_month_exp = [temp_month]*31
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            elif month in _30:
                temp_month_exp = [temp_month]*30
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
            else:
                temp_month_exp = [temp_month]*28
                for item in range(0,len(temp_month_exp)):
                    temp_month_exp[item]['day']=item
                    temp_year_final = temp_year_final.append(temp_month_exp[item],ignore_index=True)
        temp_year_final = temp_year_final.sort_values(['TIME','day','hour'],ignore_index=True)
        for hour in range(0,temp_year_final.shape[0]):
            #print(hour)
            count = 0
            while (hour+count+1<8760) and (temp_year_final[year][hour]+temp_year_final[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
                #print(count)
                count = count +1
                temp_year_final[year][hour] = temp_year_final[year][hour]+temp_year_final[year][hour+count]
                #if hour+count >= temp_year_final.shape[0]-3 and hour != temp_year_final.shape[0]: # the last observation
                    #print('here')
                 #   break
        p_inc_HP[year][region] = temp_year_final[year][0:len(temp_year_final[year])-t_shift].mean()
p_inc_HP['country'] = ""

for  row in range(0,len(p_inc_HP.index)):
   p_inc_HP['country'][row] =  p_inc_HP.index[row][0:2]
p_inc_HP.to_csv(r'./P_inc/P_inc_HP.csv')          

####################################
####################################
# whole sample
####################################
####################################

df_sample = pd.read_csv('./Full_potential.V9.country.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
df_sample['type'] = ""
df_sample['device'] = ""

df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dish Washer'] ="Max Red"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dryer'] ="Max Red"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Heat Pump'] ="Max Red"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Storage Heater'] ="Max Red"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Washing Machine'] ="Max Red"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Water Heater'] ="Max Red"

df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dish Washer'] ="DW"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dryer'] ="TD"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Heat Pump'] ="HP"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Storage Heater'] ="SH"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Washing Machine'] ="WM"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Water Heater'] ="WH"

df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dish Washer'] ="Max Dis"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dryer'] ="Max Dis"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Heat Pump'] ="Max Dis"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Storage Heater'] ="Max Dis"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Washing Machine'] ="Max Dis"
df_sample['type'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Water Heater'] ="Max Dis"

df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dish Washer'] ="DW"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dryer'] ="TD"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Heat Pump'] ="HP"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Storage Heater'] ="SH"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Washing Machine'] ="WM"
df_sample['device'][df_sample['variable'] == 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Water Heater'] ="WH"



DR_rates = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/participation_rates_country.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#  
#pip install country-converter

DR_rates['iso2'] = coco.convert(names=DR_rates['Unnamed: 0'], to='ISO2')
# adjust greece and great britain
DR_rates['iso2'][DR_rates['iso2']=="GR"] ='EL'
DR_rates['iso2'][DR_rates['iso2']=="GB"] ='UK'
DR_rates = DR_rates.loc[:,'Wash':'iso2']
DR_rates["id"] = DR_rates.index
DR_rates2 = pd.melt(DR_rates, id_vars="iso2", value_vars =DR_rates.columns[0:6])

df_sample['device2'] = df_sample['device']
df_sample['device2'][df_sample['device'] == 'DW'] ="Wash"
df_sample['device2'][df_sample['device'] == 'TD'] ="Wash"
df_sample['device2'][df_sample['device'] == 'WM'] ="Wash"
df_sample['device2'][df_sample['device'] == 'HP'] ="SH"

df_sample2 = pd.merge(df_sample,DR_rates2, left_on = ['region','device2'], right_on = ['iso2', 'variable' ])
for col in list(df_sample2)[6:39]:
    print(col)
    df_sample2[col] = df_sample2['value']/100 * df_sample2[col]

# remove devices that can not be shifted forward
keyRED = ['Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dish Washer',
 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Dryer',
 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Heat Pump',
 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Storage Heater',
 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Washing Machine',
 'Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Water Heater']

keyDIS = ['Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dish Washer',
 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Dryer',
 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Heat Pump',
 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Storage Heater',
 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Washing Machine',
 'Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Water Heater']

# sample realistic DR potentials and cooresponding installed capacities 
df_d_inc = df_sample2[df_sample2['variable_x'].isin(keyRED)] 
df_p_inc = df_sample2[df_sample2['variable_x'].isin(keyDIS)] 

# summarize to the sample level
# create whole sample data sets - hourly demand
SAMPLE_d_WM = df_d_inc[df_d_inc['device']=='WM'].groupby(['subannual'], as_index = False).sum()
SAMPLE_d_WH = df_d_inc[df_d_inc['device']=='WH'].groupby(['subannual'], as_index = False).sum()
SAMPLE_d_TD = df_d_inc[df_d_inc['device']=='TD'].groupby(['subannual'], as_index = False).sum()
SAMPLE_d_SH = df_d_inc[df_d_inc['device']=='SH'].groupby(['subannual'], as_index = False).sum()
SAMPLE_d_DW = df_d_inc[df_d_inc['device']=='DW'].groupby(['subannual'], as_index = False).sum()
SAMPLE_d_HP = df_d_inc[df_d_inc['device']=='HP'].groupby(['subannual'], as_index = False).sum()

# create whole sample data sets - installed capacity
SAMPLE_p_WM = df_p_inc[df_p_inc['device']=='WM'].groupby(['subannual'], as_index = False).sum()
SAMPLE_p_WH = df_p_inc[df_p_inc['device']=='WH'].groupby(['subannual'], as_index = False).sum()
SAMPLE_p_TD = df_p_inc[df_p_inc['device']=='TD'].groupby(['subannual'], as_index = False).sum()
SAMPLE_p_SH = df_p_inc[df_p_inc['device']=='SH'].groupby(['subannual'], as_index = False).sum()
SAMPLE_p_DW = df_p_inc[df_p_inc['device']=='DW'].groupby(['subannual'], as_index = False).sum()
SAMPLE_p_HP = df_p_inc[df_p_inc['device']=='HP'].groupby(['subannual'], as_index = False).sum()

# adjust p inc by adding demand back to the dataframe
SAMPLE_p_WM.iloc[:,1:34] = SAMPLE_p_WM.iloc[:,1:34] + SAMPLE_d_WM.iloc[:,1:34] 
SAMPLE_p_WH.iloc[:,1:34] = SAMPLE_p_WH.iloc[:,1:34] + SAMPLE_d_WH.iloc[:,1:34] 
SAMPLE_p_TD.iloc[:,1:34] = SAMPLE_p_TD.iloc[:,1:34] + SAMPLE_d_TD.iloc[:,1:34] 
SAMPLE_p_SH.iloc[:,1:34] = SAMPLE_p_SH.iloc[:,1:34] + SAMPLE_d_SH.iloc[:,1:34] 
SAMPLE_p_DW.iloc[:,1:34] = SAMPLE_p_DW.iloc[:,1:34] + SAMPLE_d_DW.iloc[:,1:34] 
SAMPLE_p_HP.iloc[:,1:34] = SAMPLE_p_HP.iloc[:,1:34] + SAMPLE_d_HP.iloc[:,1:34] 
##########################
# begin estimations for specific devices
##########################

# calc pincrease for WM
columns = []
for i in ['2022','2030','2040','2050']:
    columns.append(str(i))
SAMPLE_p_inc_WM = pd.DataFrame(index = SAMPLE_d_WM.index , columns = columns)   
SAMPLE_p_inc_WM['device'] = "WM"
SAMPLE_p_inc_WM['subannual'] = SAMPLE_d_WM.subannual
t_shift = int(df2['t.shift'][df2['Appliance']=='Washing Machine'])

max_dispatch = SAMPLE_p_WM
for year in ['2022','2030','2040','2050']:
    print(year)
    temp_year = SAMPLE_d_WM[['subannual',year]]
    max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
    for hour in range(0,temp_year.shape[0]):
        #print(hour)
        count = 0
        while (hour+count+1<288) and (temp_year[year][hour]+temp_year[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
            #print(count)
            count = count +1
            temp_year[year][hour] = temp_year[year][hour]+temp_year[year][hour+count]
    SAMPLE_p_inc_WM[year] = list(temp_year[year])
    
    
# calc pincrease for WH
columns = []
for i in ['2022','2030','2040','2050']:
    columns.append(str(i))
SAMPLE_p_inc_WH = pd.DataFrame(index = SAMPLE_d_WH.index , columns = columns)   
SAMPLE_p_inc_WH['device'] = "WH"
SAMPLE_p_inc_WH['subannual'] = SAMPLE_d_WH.subannual
t_shift = int(df2['t.shift'][df2['Appliance']=='Water Heater'])

max_dispatch = SAMPLE_p_WH
for year in ['2022','2030','2040','2050']:
    print(year)
    temp_year = SAMPLE_d_WH[['subannual',year]]
    max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
    for hour in range(0,temp_year.shape[0]):
        #print(hour)
        count = 0
        while (hour+count+1<288) and (temp_year[year][hour]+temp_year[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
            #print(count)
            count = count +1
            temp_year[year][hour] = temp_year[year][hour]+temp_year[year][hour+count]
    SAMPLE_p_inc_WH[year] = list(temp_year[year])
    
    
    
# calc pincrease for TD
columns = []
for i in ['2022','2030','2040','2050']:
    columns.append(str(i))
SAMPLE_p_inc_TD = pd.DataFrame(index = SAMPLE_d_TD.index , columns = columns)   
SAMPLE_p_inc_TD['device'] = "TD"
SAMPLE_p_inc_TD['subannual'] = SAMPLE_d_TD.subannual
t_shift = int(df2['t.shift'][df2['Appliance']=='Dryer'])

max_dispatch = SAMPLE_p_TD
for year in ['2022','2030','2040','2050']:
    print(year)
    temp_year = SAMPLE_d_TD[['subannual',year]]
    max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
    for hour in range(0,temp_year.shape[0]):
        #print(hour)
        count = 0
        while (hour+count+1<288) and (temp_year[year][hour]+temp_year[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
            #print(count)
            count = count +1
            temp_year[year][hour] = temp_year[year][hour]+temp_year[year][hour+count]
    SAMPLE_p_inc_TD[year] = list(temp_year[year])



# calc pincrease for DW
columns = []
for i in ['2022','2030','2040','2050']:
    columns.append(str(i))
SAMPLE_p_inc_DW = pd.DataFrame(index = SAMPLE_d_DW.index , columns = columns)   
SAMPLE_p_inc_DW['device'] = "DW"
SAMPLE_p_inc_DW['subannual'] = SAMPLE_d_DW['subannual']
t_shift = int(df2['t.shift'][df2['Appliance']=='Dish Washer'])

max_dispatch = SAMPLE_p_DW
for year in ['2022','2030','2040','2050']:
    print(year)
    temp_year = SAMPLE_d_DW[['subannual',year]]
    max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
    for hour in range(0,temp_year.shape[0]):
        #print(hour)
        count = 0
        while (hour+count+1<288) and (temp_year[year][hour]+temp_year[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
            #print(count)
            count = count +1
            temp_year[year][hour] = temp_year[year][hour]+temp_year[year][hour+count]
    SAMPLE_p_inc_DW[year] = list(temp_year[year])

    
    

# calc pincrease for SH
columns = []
for i in ['2022','2030','2040','2050']:
    columns.append(str(i))
SAMPLE_p_inc_SH = pd.DataFrame(index = SAMPLE_d_SH.index , columns = columns)   
SAMPLE_p_inc_SH['device'] = "SH"
SAMPLE_p_inc_SH['subannual'] = SAMPLE_d_SH['subannual']
t_shift = int(df2['t.shift'][df2['Appliance']=='Storage Heater'])


max_dispatch = SAMPLE_p_SH
for year in ['2022','2030','2040','2050']:
    print(year)
    temp_year = SAMPLE_d_SH[['subannual',year]]
    max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
    for hour in range(0,temp_year.shape[0]):
        #print(hour)
        count = 0
        while (hour+count+1<288) and (temp_year[year][hour]+temp_year[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
            #print(count)
            count = count +1
            temp_year[year][hour] = temp_year[year][hour]+temp_year[year][hour+count]
    SAMPLE_p_inc_SH[year] = list(temp_year[year])

    
    
    
# calc pincrease for HP
columns = []
for i in ['2022','2030','2040','2050']:
    columns.append(str(i))
SAMPLE_p_inc_HP = pd.DataFrame(index = SAMPLE_d_HP.index , columns = columns)   
SAMPLE_p_inc_HP['device'] = 'HP'
SAMPLE_p_inc_HP['subannual'] = SAMPLE_d_HP['subannual']
t_shift = 3

max_dispatch = SAMPLE_p_HP
for year in ['2022','2030','2040','2050']:
    print(year)
    temp_year = SAMPLE_d_HP[['subannual',year]]
    max_dispatch_year = max_dispatch[year].mean() # mean is arbitrary as value is constant throughout the year; this prevents indexing error 
    for hour in range(0,temp_year.shape[0]):
        #print(hour)
        count = 0
        while (hour+count+1<288) and (temp_year[year][hour]+temp_year[year][hour+count] < max_dispatch_year) and (count < t_shift+1):
            #print(count)
            count = count +1
            temp_year[year][hour] = temp_year[year][hour]+temp_year[year][hour+count]
    SAMPLE_p_inc_HP[year] = list(temp_year[year])


PINC_FINAL =pd.concat([SAMPLE_p_inc_DW,SAMPLE_p_inc_TD,SAMPLE_p_inc_WM,SAMPLE_p_inc_SH,SAMPLE_p_inc_WH,SAMPLE_p_inc_HP])

# remove hours at the end of each year for each device that due to the data structure could not increase the full amount
# since SH and WH have a tshift of 12 hours we will remove the last twelve observations fromthe data set
SH_WH_key = ['12-01 12:00+01:00',
 '12-01 13:00+01:00',
 '12-01 14:00+01:00',
 '12-01 15:00+01:00',
 '12-01 16:00+01:00',
 '12-01 17:00+01:00',
 '12-01 18:00+01:00',
 '12-01 19:00+01:00',
 '12-01 20:00+01:00',
 '12-01 21:00+01:00',
 '12-01 22:00+01:00',
 '12-01 23:00+01:00']

PINC_FINAL2 = PINC_FINAL[(~PINC_FINAL['subannual'].isin(SH_WH_key)) ]
PINC_FINAL3 = PINC_FINAL2.groupby(['subannual'], as_index = False).sum()
PINC_FINAL3[['2022','2030','2040','2050']].describe()
'''
SH_WH_key = ['12-01 12:00+01:00',
 '12-01 13:00+01:00',
 '12-01 14:00+01:00',
 '12-01 15:00+01:00',
 '12-01 16:00+01:00',
 '12-01 17:00+01:00',
 '12-01 18:00+01:00',
 '12-01 19:00+01:00',
 '12-01 20:00+01:00',
 '12-01 21:00+01:00',
 '12-01 22:00+01:00',
 '12-01 23:00+01:00']

WASH_key = [ '12-01 18:00+01:00',
 '12-01 19:00+01:00',
 '12-01 20:00+01:00',
 '12-01 21:00+01:00',
 '12-01 22:00+01:00',
 '12-01 23:00+01:00']

HP_key =[
 '12-01 21:00+01:00',
 '12-01 22:00+01:00',
 '12-01 23:00+01:00']

test_HP = SAMPLE_p_inc_HP
test_HP2 = test_HP[(~test_HP['subannual'].isin(HP_key)) & (test_HP['device'].isin(['HP']))]

test_SH = SAMPLE_p_inc_SH
test_SH2 = test_SH[(~test_SH['subannual'].isin(SH_WH_key)) & (test_SH['device'].isin(['SH']))]

# remove hours at the end of each year for each device that due to the data structure could not increase the full amount
#SH
PINC_FINAL2 = PINC_FINAL[(~PINC_FINAL['subannual'].isin(SH_WH_key)) | (~PINC_FINAL['device'].isin(['SH']))]
#WH
PINC_FINAL2 = PINC_FINAL2[(~PINC_FINAL2['subannual'].isin(SH_WH_key)) | (~PINC_FINAL2['device'].isin(['WH']))]
#TD
PINC_FINAL2 = PINC_FINAL2[(~PINC_FINAL2['subannual'].isin(WASH_key)) | (~PINC_FINAL2['device'].isin(['TD']))]
#WM
PINC_FINAL2 = PINC_FINAL2[(~PINC_FINAL2['subannual'].isin(WASH_key)) | (~PINC_FINAL2['device'].isin(['WM']))]
#HP
PINC_FINAL2 = PINC_FINAL2[(~PINC_FINAL2['subannual'].isin(HP_key)) | (~PINC_FINAL2['device'].isin(['HP']))]
#DW
PINC_FINAL2 = PINC_FINAL2[(~PINC_FINAL2['subannual'].isin(WASH_key)) | (~PINC_FINAL2['device'].isin(['DW']))]

'''

SAMPLE_HP = SAMPLE_p_inc_HP.T
SAMPLE_HP['device'] = 'HP'
SAMPLE_HP = SAMPLE_HP.reset_index()

SAMPLE_DW = SAMPLE_p_inc_DW.T
SAMPLE_DW['device'] = 'DW'
SAMPLE_DW = SAMPLE_DW.reset_index()

SAMPLE_SH = SAMPLE_p_inc_SH.T
SAMPLE_SH['device'] = 'SH'
SAMPLE_SH = SAMPLE_SH.reset_index()

SAMPLE_TD = SAMPLE_p_inc_TD.T
SAMPLE_TD['device'] = 'TD'
SAMPLE_TD = SAMPLE_TD.reset_index()

SAMPLE_WH = SAMPLE_p_inc_WH.T
SAMPLE_WH['device'] = 'WH'
SAMPLE_WH = SAMPLE_WH.reset_index()

SAMPLE_WM = SAMPLE_p_inc_WM.T
SAMPLE_WM['device'] = 'WM'
SAMPLE_WM = SAMPLE_WM.reset_index()

frames = [SAMPLE_HP,SAMPLE_DW,SAMPLE_SH,SAMPLE_TD,SAMPLE_WH,SAMPLE_WM]
SAMPLE_final = pd.concat(frames)

SAMPLE_final.to_csv(r'./P_inc/SAMPLE_PINC.csv')          
