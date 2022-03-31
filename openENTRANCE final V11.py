"""
The objective of this script is to solve for European household energy demand from 2018-2050
Difference between version 7 and 8 are the file locations and version 8 uses the updated file for EV NUTS regions
Difference between version 8 and 9 is the adjustment to the circulation pump 
Differnence between version 9 and 10 is the inclusion of heat pumps
Difference between version 10 and 11 is the use of new EV data and fitfor55 EV scenario

"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
from datetime import date,timedelta,datetime # for getting today's date
import time
import json
import os
#from smtplib import SMTP_SSL ## for sending emails
#import pyam
#import nomenclature
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email.MIMEText import MIMEText
#import requests # for APIso
### Set options
#os.chdir('I:\Projekte\OpenEntrance - WV0173\Durchführungsphase\WP6\CS1\gitlab\datainputs') # set wd - change to server path - IMPORTANT
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data\openENTRANCE final data')
#os.chdir('/Users/ryanoreilly/Desktop/openENTRANCE-data/openENTRANCE final data/')
## TEST TEST COMMMENT
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

### END - global options
### Load in data

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

nflh_ac = pd.read_csv('./nflh_ac.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
nflh_cp = pd.read_csv('./nflh_cp.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
pcycle_wm = pd.read_csv('./Pcycle_wm.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
pcycle_td = pd.read_csv('./Pcycle_td.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
pcycle_dw = pd.read_csv('./Pcycle_dw.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
wunit_rf_fr = pd.read_csv('./Wunit_rf_fr.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
punit_ac = pd.read_csv('./Punit_ac.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
punit_cp = pd.read_csv('./Punit_cp.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

wunit_ev =  pd.read_excel('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/EV_parameters.xlsx')

#ownership rates; ev is in # of EVs
rcp = pd.read_csv('./rcp.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rdw = pd.read_csv('./rdw.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rwm = pd.read_csv('./rwm.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rtd = pd.read_csv('./rtd.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rfr = pd.read_csv('./rfr.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rrf = pd.read_csv('./rrf.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rsh = pd.read_csv('./rsh.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rwh = pd.read_csv('./rwh.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rac = pd.read_csv('./rac.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

rev = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/EV NUTS projectionsV5.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rev_fit55 = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/EV NUTS projectionsV5_fit55.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 


# add data for Electric Vehicles
# electric vehicle hour shares
# file created using R 'hourly share calculation.R'
s_ev=pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/openENTRANCE projection/EV Hourly Charging Shares/hourlyEVshares.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_ev=s_ev.drop(['Unnamed: 0'],axis=1)

# add shares for Tumble Dryer, Washing Machine and Dish Washer; from Stamminger
s_wash =pd.read_csv('./s_wash nuts.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_wash = s_wash[s_wash['nutscode']!= "NO0B"] # remove NO0B due to missing data in other categories
s_wash = s_wash[s_wash['nutscode']!= "MT00"] # remove MT00 due to missing data in other categories

# add shares for s_hdd & s_cdd
s_hdd =pd.read_csv('./s_hdd nutsV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_cdd=pd.read_csv('./s_cdd nutsV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
# add shares for CP, WH, SH, AC
s_allelse = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/stamminger_2009.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

# add share for hp
s_hp = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/heat_pump_hourly_share.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_hp.columns = ['hour',"S_HP"]

# add data for yr_hdd & yr_cdd
yr_hdd =pd.read_csv('./yr_hdd nutsV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
yr_cdd=pd.read_csv('./yr_cdd nutsV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

#thermal provision of energy from HP
Q_hp_thermal =pd.read_csv('./Qhp_thermal_MWh_projected.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

#thermal heat requirement by NTUS0 
Q_NUTS0_thermal =pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/NUTS0_thermal_heat_annum.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

# cop for hp by nuts 2 region
cop = pd.read_csv("I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/temperature/NUTS2_2011_2021_COPmean.csv",sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
cop.columns = ['nutscode', 'Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'August', 'Septmber', 'October', 'November', 'December']
# adjust excel autocorecting German NUTS2 region DEC0 to Dec-00
cop.nutscode[cop.nutscode=="Dec-00"] = 'DEC0'
cop.index = cop['nutscode']
cop = cop.drop('nutscode', axis=1)    
cop=cop[[ 'Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'August', 'Septmber', 'October', 'November', 'December']].apply(pd.to_numeric,errors='coerce').fillna(cop)



# expand datasets to represent nuts 2 regions
temp = nhh[['nutscode']]
temp['country']= ""
for row in range(0,len(temp)):
    temp['country'][row] = temp['nutscode'][row][0:2]
temp = temp.sort_values('nutscode')

# # full load hours
nflh_ac = nflh_ac.merge(temp)
nflh_ac = nflh_ac.drop('country', axis=1)
nflh_ac.index = nflh_ac['nutscode']
nflh_ac = nflh_ac.drop('nutscode', axis=1)    
    
nflh_cp = nflh_cp.merge(temp)
nflh_cp = nflh_cp.drop('country', axis=1)
nflh_cp.index = nflh_cp['nutscode']
nflh_cp = nflh_cp.drop('nutscode', axis=1)    

# power p cycle
pcycle_wm = pcycle_wm.merge(temp)
pcycle_wm = pcycle_wm.drop('country', axis=1)
pcycle_wm.index = pcycle_wm['nutscode']
pcycle_wm = pcycle_wm.drop('nutscode', axis=1)  

pcycle_td = pcycle_td.merge(temp)
pcycle_td = pcycle_td.drop('country', axis=1)
pcycle_td.index = pcycle_td['nutscode']
pcycle_td = pcycle_td.drop('nutscode', axis=1)  

pcycle_dw = pcycle_dw.merge(temp)
pcycle_dw = pcycle_dw.drop('country', axis=1)
pcycle_dw.index = pcycle_dw['nutscode']
pcycle_dw = pcycle_dw.drop('nutscode', axis=1)  

# unit capacity
wunit_rf_fr = wunit_rf_fr.merge(temp)
wunit_rf_fr = wunit_rf_fr.drop('country', axis=1)
wunit_rf_fr.index = wunit_rf_fr['nutscode']
wunit_rf_fr = wunit_rf_fr.drop('nutscode', axis=1)      


wunit_ev = wunit_ev.merge(temp)
wunit_ev = wunit_ev.drop(['country','evLIFE_150kkm','average age/# years assuming 150k life'], axis=1)
wunit_ev = wunit_ev.sort_values('nutscode')
wunit_ev.index = wunit_ev['nutscode']
wunit_ev = wunit_ev.drop('nutscode', axis=1)      

# hp thermal energy demand
Q_hp_thermal = Q_hp_thermal.merge(temp)
Q_hp_thermal = Q_hp_thermal.drop(['country'], axis=1)
Q_hp_thermal = Q_hp_thermal.sort_values('nutscode')
Q_hp_thermal.index = Q_hp_thermal['nutscode']
Q_hp_thermal = Q_hp_thermal.drop('nutscode', axis=1)  

# hp thermal energy demand
cop = cop.reset_index()
cop = cop.merge(temp)
cop = cop.drop(['country'], axis=1)
cop = cop.sort_values('nutscode')
cop.index = cop['nutscode']
cop = cop.drop('nutscode', axis=1)  


# rates of ownership
rcp = rcp.merge(temp)
rcp = rcp.drop('country', axis=1)
rcp.index = rcp['nutscode']
rcp = rcp.drop('nutscode', axis=1)

rdw = rdw.merge(temp)
rdw = rdw.drop('country', axis=1)
rdw.index = rdw['nutscode']
rdw = rdw.drop('nutscode', axis=1)

rwm = rwm.merge(temp)
rwm = rwm.drop('country', axis=1)
rwm.index = rwm['nutscode']
rwm = rwm.drop('nutscode', axis=1)

rfr = rfr.merge(temp)
rfr = rfr.drop('country', axis=1)
rfr.index = rfr['nutscode']
rfr = rfr.drop('nutscode', axis=1)

rrf = rrf.merge(temp)
rrf = rrf.drop('country', axis=1)
rrf.index = rrf['nutscode']
rrf = rrf.drop('nutscode', axis=1)

rsh = rsh.merge(temp)
rsh = rsh.drop('country', axis=1)
rsh.index = rsh['nutscode']
rsh = rsh.drop('nutscode', axis=1)

rtd = rtd.merge(temp)
rtd = rtd.drop('country', axis=1)
rtd.index = rtd['nutscode']
rtd = rtd.drop('nutscode', axis=1)

rwh = rwh.merge(temp)
rwh = rwh.drop('country', axis=1)
rwh.index = rwh['nutscode']
rwh = rwh.drop('nutscode', axis=1)

rac = rac.merge(temp)
rac = rac.drop('country', axis=1)
rac.index = rac['nutscode']
rac = rac.drop('nutscode', axis=1)

rev = rev.merge(temp,how = 'outer')
rev = rev.sort_values('nutscode')
rev = rev.drop('country', axis =1)
rev.index = rev['nutscode']
rev = rev.drop('nutscode', axis =1)
rev = rev.drop('Unnamed: 0', axis = 1)

rev_fit55 = rev_fit55.merge(temp,how = 'outer')
rev_fit55 = rev_fit55.sort_values('nutscode')
rev_fit55 = rev_fit55.drop('country', axis =1)
rev_fit55.index = rev_fit55['nutscode']
rev_fit55 = rev_fit55.drop('nutscode', axis =1)
rev_fit55 = rev_fit55.drop('Unnamed: 0', axis = 1)

# change nhh, punit_ac, punit_cp, s_hdd, and s_cdd to be in the same format as above
nhh.index = nhh['nutscode']
nhh = nhh.drop('nutscode',axis=1)

punit_ac.index = punit_ac['country']
punit_ac = punit_ac.drop('country',axis=1)

punit_cp.index = punit_cp['country']
punit_cp = punit_cp.drop('country',axis=1)

s_cdd.index = s_cdd['nutscode']
s_cdd = s_cdd.drop(['nutscode','month'],axis=1) #TIME is dropped from axis; order of months is maintained

s_hdd.index = s_hdd['nutscode']
s_hdd = s_hdd.drop(['nutscode','month'],axis=1) #TIME is dropped from axis; order of months is maintained

yr_cdd.index = yr_cdd['nutscode']
yr_cdd = yr_cdd.drop(['nutscode','month'],axis=1) #TIME is dropped from axis; order of months is maintained

yr_hdd.index = yr_hdd['nutscode']
yr_hdd = yr_hdd.drop(['nutscode','month'],axis=1) #TIME is dropped from axis; order of months is maintained


# create index for representative hours for each nuts 2 region
#!!!!!! adjust this
#time = pd.read_csv('/Users/ryanoreilly/Desktop/openENTRANCE-data/Clean_data.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
time = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/flexibilities file reference/Clean_data.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
time = time[time.nutscode == 'AT11'] # AT11 is chosen arbitrarily
time = pd.DataFrame(time[['time','hour']])

index = s_wash[['nutscode','country','hour']]
index = index.reset_index()   
index = index.drop('index', axis=1)

index = pd.merge(index,time)
del time
index = index.sort_values(by=['nutscode','time','hour'])
index = index.reset_index() #reset index 
index = index.drop('index', axis =1)

##########
# heat pumps

##################
# create expectations for the number of HP by NUTS2 - 
# 1) take thermal demand NUTS2 and divide by the average thermal requiremnt for HH in NUTS0
##################



"""
NUTS_num_HP = num_hp.groupby(['country']).sum()

nhh['country'] = ""

for row in range(0, nhh.shape[0]):
        print(row)
        nhh['country'][row] = nhh.index[row][0:2]
        
nhh = nhh.groupby(['country']).sum()
 
test = NUTS_num_HP.merge(nhh, left_on = NUTS_num_HP.index, right_on = nhh.index)

columns = []
for i in range(2018,2051):
    columns.append(str(i))
    
numhp_as_shareHH = pd.DataFrame(index = test.key_0, columns = columns)  

for row in range(0, numhp_as_shareHH.shape[0]):
    print(row)
    for year in range(1, numhp_as_shareHH.shape[1]+1):
        numhp_as_shareHH.iloc[row,year-1] = round(test.iloc[row,year]/test.iloc[row,year + 33],2)
        """


       
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_HP = pd.DataFrame(index = index, columns = columns)   
p_HP = pd.DataFrame(index = index, columns = columns)  
 

s_hp =s_hp.S_HP # hour share of daily demand

'''
#create sequence for hours in representative year
hour = pd.Series(range(0,24))
hour = hour.append([pd.Series(range(0,24))]*((11)),ignore_index=True)
test['houryr'] = list(temp2)
#create sequence for months in representative year
month = list(pd.Series(range(1,13)))*24
month.sort()
'''
for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_HP.index[(row-1)*288][0]
    S_HDD = pd.DataFrame(s_hdd.loc[region])
    temp_cop = cop.loc[region]
    temp_qhp = pd.DataFrame(Q_hp_thermal.loc[region]).transpose()
    yr_S_HDD = pd.DataFrame(S_HDD['2018'])
    temp_qmonth = pd.DataFrame(np.dot(yr_S_HDD, temp_qhp))
    for year in range(0,temp_qmonth.shape[1]):
        for month in range(0,12):
            temp_qmonth.iloc[month,year] =  temp_qmonth.iloc[month,year]/temp_cop[month]
    temp_qyear = pd.DataFrame(index = range(0,288), columns = columns)
    count = -1
    for month in range(0,12):
        for hour in range(0,24):
            count +=1
            temp_qyear.iloc[count,0:33] = temp_qmonth.iloc[month,0:33]*s_hp[hour]/30 # divide by # days in the month ~30
            if count == 287:
                low = (row-1)*288
                high = row*288
                for year in range(2018-2018,2050+1-2018):
                    data = list(temp_qyear.iloc[0:288,year])
                    d_HP.iloc[low:high,year] = data               
                    
# solve for P_HP assuming HP installed cap = 12kWh
# p_cap_hp can never be greater than #hh*0.012

#thermal provision of energy from HP
num_hp =pd.read_csv('./Qhp_thermal_MWh_projected.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 


Q_NUTS0_thermal.index = Q_NUTS0_thermal['file_country_path']
Q_NUTS0_thermal = Q_NUTS0_thermal.drop(['file_country_path'],axis=1)


num_hp['country'] = ""

for row in range(0, num_hp.shape[0]):
        print(row)
        num_hp['country'][row] = num_hp.nutscode[row][0:2]
        
for row in range(0, num_hp.shape[0]):
    print(row)
    NUTS0 = num_hp.nutscode[row][0:2]
    for year in range(1, num_hp.shape[1]-1):
            num_hp.iloc[row,year] =     num_hp.iloc[row,year]/(Q_NUTS0_thermal.loc[NUTS0]['them_cap']/1000)

num_hp= num_hp.sort_values('nutscode')
num_hp.index = num_hp.nutscode
num_hp = num_hp.drop(['MT00'], axis =0)
num_hp = num_hp.drop(['nutscode','country'], axis =1)

# set limit for installed capacity
for row in range(0, num_hp.shape[0]):
    print(row)
    for year in range(0, num_hp.shape[1]):
        print(year)
        if num_hp.iloc[row,year] / nhh.iloc[row,year] > 1:
            num_hp.iloc[row,year] = nhh.iloc[row,year]

p_inst_hp = num_hp*0.012 # 0.012 = the installed capacity of hp in mWh

for hour in range(0, p_HP.shape[0]):
    print(hour)
    p_HP.iloc[hour,0:33] = list(p_inst_hp.loc[p_HP.index[hour][0],])

d_HP =d_HP.apply(pd.to_numeric)
d_HP['country'] = ""
d_HP['hour'] = ""
d_HP['TIME'] = ""
d_HP['nutscode'] = ""
for i in range(0, d_HP.shape[0]):
    print(i)
    d_HP['country'][i] = d_HP.index[i][1]
    d_HP['hour'][i] = int(d_HP.index[i][2])
    d_HP['nutscode'][i] = d_HP.index[i][0]
    d_HP['TIME'][i] = d_HP.index[i][3]
    
d_HP.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_HPV2.csv')  
   
p_HP =p_HP.apply(pd.to_numeric)
p_HP['country'] = ""
p_HP['hour'] = ""
p_HP['TIME'] = ""
p_HP['nutscode'] = ""
for i in range(0, p_HP.shape[0]):
    print(i)
    p_HP['country'][i] = p_HP.index[i][1]
    p_HP['hour'][i] = int(p_HP.index[i][2])
    p_HP['nutscode'][i] = p_HP.index[i][0]
    p_HP['TIME'][i] = p_HP.index[i][3]      
    
p_HP.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_HP.csv')  

# check for error
p_HP = p_HP.reset_index()
p_HP = p_HP.drop(['index'],axis=1)

d_HP = pd.read_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_HPV2.csv') 
d_HP = d_HP.drop(['Unnamed: 0'],axis=1)
# identify error
p_star = p_HP.iloc[0:p_HP.shape[0],0:33]#

d_excess = d_HP.iloc[0:d_HP.shape[0],0:33] -p_star

##########
# Air conditioning
    
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_AC = pd.DataFrame(index = index, columns = columns)   
p_AC = pd.DataFrame(index = index, columns = columns)  
 
#!!!!!!!!!!!!!!!!!!! change 
#s_allelse = pd.read_csv('./stamminger_2009.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

s_ac =s_allelse.S_AC # hour share of daily demand
s_ac2 = s_ac
s_ac = s_ac.append([s_ac]*11,ignore_index=True)
'''
#create sequence for hours in representative year
hour = pd.Series(range(0,24))
hour = hour.append([pd.Series(range(0,24))]*((11)),ignore_index=True)
test['houryr'] = list(temp2)
#create sequence for months in representative year
month = list(pd.Series(range(1,13)))*24
month.sort()
'''
for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_AC.index[(row-1)*288][0]
    NHH = nhh.loc[region]
    PUNIT_AC = punit_ac.loc[region[0:2]]
    NFLH_AC = nflh_ac.loc[region]
    RAC = rac.loc[region]
    S_CDD = s_cdd.loc[region] 
    #FOR HOURLY DEMAND
    temp = NFLH_AC*PUNIT_AC*NHH*RAC*S_CDD/1/30/1000 # daily
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for yr in range(0,temp.shape[1]): # convert from daily to hourly
        temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_ac    
    low = (row-1)*288
    high = row*288
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        d_AC.iloc[low:high,year] = data
    #for pinst - installed capacity NUTS2 level
    temp = pd.DataFrame(NHH*RAC*PUNIT_AC/1000).T
    temp = temp.append([temp]*11,ignore_index=True)
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        p_AC.iloc[low:high,year] = data



d_AC =d_AC.apply(pd.to_numeric)
d_AC['country'] = ""
d_AC['hour'] = ""
d_AC['TIME'] = ""
d_AC['nutscode'] = ""
for i in range(0, d_AC.shape[0]):
    print(i)
    d_AC['country'][i] = d_AC.index[i][1]
    d_AC['hour'][i] = int(d_AC.index[i][2])
    d_AC['nutscode'][i] = d_AC.index[i][0]
    d_AC['TIME'][i] = d_AC.index[i][3]
    
p_AC =p_AC.apply(pd.to_numeric)
p_AC['country'] = ""
p_AC['hour'] = ""
p_AC['TIME'] = ""
p_AC['nutscode'] = ""
for i in range(0, p_AC.shape[0]):
    print(i)
    p_AC['country'][i] = p_AC.index[i][1]
    p_AC['hour'][i] = int(p_AC.index[i][2])
    p_AC['nutscode'][i] = p_AC.index[i][0]
    p_AC['TIME'][i] = p_AC.index[i][3]   
    
#p_AC.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_ACV6.csv')       
#d_AC.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_ACV6.csv')     
  
#p_AC = pd.read_csv(r'/Users/ryanoreilly/Desktop/openENTRANCE-data/temp_ac/p_ACV6.csv')       
#d_AC = pd.read_csv(r'/Users/ryanoreilly/Desktop/openENTRANCE-data/temp_ac/d_ACV6.csv') 
#d_AC = d_AC.drop(['Unnamed: 0'],axis=1)
#p_AC = p_AC.drop(['Unnamed: 0'],axis=1)

# identify error
p_star = p_AC.iloc[0:p_AC.shape[0],0:33]#*.75

d_excess = d_AC.iloc[0:d_AC.shape[0],0:33] - p_star

d_excess['nutscode'] = d_AC['nutscode']
d_excess['hour'] = d_AC['hour']
d_excess['TIME'] = d_AC['TIME']

d_excess = d_excess.reset_index()
d_excess = d_excess.drop(['index'],axis=1)
look_excess = []
two_iter = []
for year in range(2018-2018,2050+1-2018):
    yr = d_excess.columns[year]
    d_neg = d_excess[d_excess[yr]>0]
    #print(yr,len(set(d_neg.nutscode)))
    reg_change = set(d_neg['nutscode'])    
    print(reg_change)
    reg_look = []
    reg_look2 = []
    for i in reg_change:
        #print(i)
        temp2 = d_neg[d_neg['nutscode']==i]
        months = set(temp2['TIME'])
        for mon in months:
            #print(mon)
            temp3 = temp2[temp2['TIME']==mon]
            dist_amt = sum(temp3[yr])
            #distribution of energy
            hour_rem = list(temp3['hour'])
            s_ac_temp = list(s_ac2[0:min(hour_rem)])
            s_ac_temp.extend(len(hour_rem)*[0])
            s_ac_temp.extend(list(s_ac2[max(hour_rem)+1:len(s_ac2)]))
            #normalize shares
            sum_s_ac = sum(s_ac_temp)
            for share in range(0, len(s_ac_temp)):
                s_ac_temp[share] = s_ac_temp[share]/sum_s_ac
            s_ac_temp = pd.DataFrame(s_ac_temp)
            #create df with final values to add or subtract from d_AC
            amt_ac_hour = s_ac_temp*dist_amt
            data = pd.DataFrame(temp3[yr].iloc[0:temp3.shape[0]])*-1 # values to subtract
            amt_ac_hour.iloc[temp3['hour'].iloc[0]:temp3['hour'].iloc[-1]+1] = data
            #edit d_AC
            #day  that violated peak assumption
            vio_hour = d_AC.iloc[temp3.index[0]]['hour'] # first row that vilated peak assumption
            vio_day = pd.DataFrame(d_AC.iloc[temp3.index[0]-vio_hour:temp3.index[0]+24-vio_hour][yr]) # day that violated peak assumption
            vio_day['adjust'] = ""
            for row in range(0,vio_day.shape[0]):
                vio_day['adjust'].iloc[row] = vio_day[yr].iloc[row] +amt_ac_hour[0].iloc[row]
            count = 0
            #print("region:  ", i,"month:  ", mon)
            reg_look2.append(i)
            while max(vio_day['adjust']) >vio_day['adjust'].iloc[vio_hour]: 
                count+=1
                #print("region:  ", i,"month:  ", mon, "count:  ", count)
          # if redistribution of the energy caused other hours to exceed p_star
                dist_amt2 =[]
                hour_surplus = []
                for row in range(0,vio_day.shape[0]): 
                    if vio_day['adjust'].iloc[row] > vio_day['adjust'].iloc[vio_hour]:
                        reg_look.append(i)
                        #print(row)
                        dist_amt2.append(vio_day['adjust'].iloc[row]-vio_day['adjust'].iloc[vio_hour])
                        hour_surplus.append(row)
                        vio_day['adjust'].iloc[row] = vio_day['adjust'].iloc[row] - (vio_day['adjust'].iloc[row]-vio_day['adjust'].iloc[vio_hour])
                hour_rem.extend(hour_surplus)
                if min(hour_rem) == 0:
                    s_ac_temp = [0]
                    s_ac_temp.extend(s_ac2[1:list(set(hour_rem))[1]])
                    s_ac_temp.extend((len(hour_rem)-1)*[0])
                    #s_ac_temp.extend(list(s_ac2[max(hour_rem)+1:len(s_ac2)]))
                else:
                    s_ac_temp = list(s_ac2[0:min(hour_rem)])
                    s_ac_temp.extend(len(hour_rem)*[0])
                    s_ac_temp.extend(list(s_ac2[max(hour_rem)+1:len(s_ac2)]))
                dist_amt2 = sum(dist_amt2)
                #normalize shares
                sum_s_ac = sum(s_ac_temp)
                for share in range(0, len(s_ac_temp)):
                    s_ac_temp[share] = s_ac_temp[share]/sum_s_ac
                s_ac_temp = pd.DataFrame(s_ac_temp)
                #create df with final values to add or subtract from d_AC
                amt_ac_hour = s_ac_temp*dist_amt2
                #adjust2 is the final values to replace respective values in d_AC
                vio_day['adjust2'] = ""
                for row in range(0,vio_day.shape[0]):
                    vio_day['adjust2'].iloc[row] = vio_day['adjust'].iloc[row] +amt_ac_hour[0].iloc[row]
                vio_day['adjust'] = vio_day['adjust2']
            data = list(vio_day['adjust'])
            # set d_AC with new data
            print('region:  ', i )
            d_AC.loc[min(vio_day.index):max(vio_day.index),yr] =  data 
    look_excess.append([yr,reg_look2])
    two_iter.append([yr,reg_look])
            


#Check results

# identify error
p_star = p_AC.iloc[0:p_AC.shape[0],0:33]#*.75

d_excess = d_AC.iloc[0:d_AC.shape[0],0:33] -p_star

d_excess['nutscode'] = d_AC['nutscode']
d_excess['hour'] = d_AC['hour']
d_excess['TIME'] = d_AC['TIME']

for year in range(2018-2018,2050+1-2018):
    yr = d_excess.columns[year]
    d_neg = d_excess[d_excess[yr]>0]
    print(yr,"amt",len(set(d_neg['nutscode'])),"nutscode",set(d_neg['nutscode'])  )
    reg_change = set(d_neg['nutscode'])  
    print(len(reg_change))
    
temp = d_AC[d_AC['nutscode']=='TR82']


del NFLH_AC
del PUNIT_AC
del RAC
del S_CDD

p_AC.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_ACV6.csv')       
d_AC.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_ACV6.csv')   

#p_AC.to_csv(r'/Users/ryanoreilly/Desktop/openENTRANCE-data/theoretical potential/p_ACV7.csv')       
#d_AC.to_csv(r'/Users/ryanoreilly/Desktop/openENTRANCE-data/theoretical potential/d_ACV7.csv')   

del p_AC
del d_AC

########
# heat cirulation pump
# punit is is watts, hence divide by 1000 to converto kw for consistency with other algorithms
# hourly demand for CP is higher than installed capacity. 
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_CP = pd.DataFrame(index = index, columns = columns)   
d_CPadj = pd.DataFrame(index = index, columns = columns)   
p_CP = pd.DataFrame(index = index, columns = columns)   

s_cp =s_allelse.S_CP # hour share of daily demand
s_cp = s_cp.append([s_cp]*11,ignore_index=True)

for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_CP.index[(row-1)*288][0]
    NHH = nhh.loc[region]
    PUNIT_CP = punit_cp.loc[region[0:2]]/1000 #kW
    NFLH_CP = nflh_cp.loc[region]
    RCP = rcp.loc[region]
    S_HDD = s_hdd.loc[region]/30 #daily share
    #FOR HOURLY DEMAND
    temp = NFLH_CP*NHH*RCP*PUNIT_CP*S_HDD/1/1000 #hourly in MW
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for yr in range(0,temp.shape[1]): # convert from daily to hourly
        temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_cp
    low = (row-1)*288
    high = row*288
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        d_CP.iloc[low:high,year] = data
    #make adjustment for circulation pumps that are not turned off in summer
    for yr in range(0,temp.shape[1]):
        maxyr = temp.iloc[0:288,yr].max()
#        print("Year:  ", yr)
#        print("Max:  ", maxyr)
        for hour in range(0,temp.shape[0]):
            if round(temp.iloc[hour,yr],2) < maxyr*.15: 
                print("here")                                                 # less than 15% peak
                temp.iloc[hour,yr] = PUNIT_CP[yr]*NHH[yr]*RCP[yr]/1000*.25
            elif round(temp.iloc[hour,yr],2) >= maxyr*.15 and round(temp.iloc[hour,yr],2) <= maxyr*.6:              #between 15% and 60% peak
                temp.iloc[hour,yr] =  1.67*(temp.iloc[hour,yr]/maxyr)*PUNIT_CP[yr]*NHH[yr]*RCP[yr]/1000
            elif round(temp.iloc[hour,yr],2) > maxyr*.6:                                                 # greater than 60%
                temp.iloc[hour,yr] =  PUNIT_CP[yr]*NHH[yr]*RCP[yr]/1000       
            else:
                print("Hour:  ", hour)
                print("Year:  ", yr)
                print("Year:  ", yr)
    low = (row-1)*288
    high = row*288
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        d_CPadj.iloc[low:high,year] = data
    #for pinst - installed capacity NUTS2 level
    temp = pd.DataFrame(NHH*RCP*100/1000/1000).T # unit installed capacity assumed to be 100 watts
    temp = temp.append([temp]*11,ignore_index=True)
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        p_CP.iloc[low:high,year] = data
        
d_CPadj =d_CPadj.apply(pd.to_numeric)


d_CPadj['country'] = ""
d_CPadj['hour'] = ""
d_CPadj['TIME'] = ""
d_CPadj['nutscode'] = ""
for i in range(0, d_CPadj.shape[0]):
    print(i)
    d_CPadj['country'][i] = d_CPadj.index[i][1]
    d_CPadj['hour'][i] = int(d_CPadj.index[i][2])
    d_CPadj['nutscode'][i] = d_CPadj.index[i][0]
    d_CPadj['TIME'][i] = d_CPadj.index[i][3]

     
d_CPadj.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_CPV5.csv')   


p_CP =p_CP.apply(pd.to_numeric)
p_CP['country'] = ""
p_CP['hour'] = ""
p_CP['TIME'] = ""
p_CP['nutscode'] = ""
for i in range(0, p_CP.shape[0]):
    print(i)
    p_CP['country'][i] = p_CP.index[i][1]
    p_CP['hour'][i] = int(p_CP.index[i][2])
    p_CP['nutscode'][i] = p_CP.index[i][0]
    p_CP['TIME'][i] = p_CP.index[i][3]    
    
del NFLH_CP
del PUNIT_CP
del RCP
del S_HDD


p_CP.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_CPV5.csv')       
 

########
# wh - water heater
# the calculation of water heater will use Gils 2014 method and assume that there is no change in the efficiency of the appliance
# assumed that water heater energy is constant for all days in year 
# WH and SH cant be Delayed only advanced (Gils 2014)



columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_WH = pd.DataFrame(index = index, columns = columns)   
p_WH = pd.DataFrame(index = index, columns = columns)   

s_wh =s_allelse.S_WH # hour share of daily demand
s_wh2 = s_wh
s_wh = s_wh.append([s_wh]*11,ignore_index=True)

for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_WH.index[(row-1)*288][0]
    NHH = nhh.loc[region]           # number of households
    YR_HDD = yr_hdd.loc[region]     # annual HDD
    RWH = rwh.loc[region]           # rate of ownership of WH
    NFLH_WH = (YR_HDD/1000)*25+175  # number of full load hours of WH
    PUNIT_WH = 2                    # unit installed capacity; assumed constant across years kW
    WUNIT_WH = NFLH_WH*PUNIT_WH     # annual electricity demand per unit of WH; kWh
    W_WH = WUNIT_WH*NHH*RWH         # national annual electricity demand for WH; kWh
    S_HDD = 1/12/30                 # every hour has the same energy demand 
    #FOR HOURLY DEMAND
    temp = NFLH_WH*PUNIT_WH*NHH*RWH*S_HDD/1/1000 #daily; MWh
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for yr in range(0,temp.shape[1]): # convert from daily to hourly
        temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_wh    
    low = (row-1)*288
    high = row*288
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        d_WH.iloc[low:high,year] = data
    #for pinst - installed capacity NUTS2 level
    temp = pd.DataFrame(NHH*RWH*PUNIT_WH/1000).T
    temp = temp.append([temp]*11,ignore_index=True)
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        p_WH.iloc[low:high,year] = data
d_WH =d_WH.apply(pd.to_numeric)

d_WH['country'] = ""
d_WH['hour'] = ""
d_WH['TIME'] = ""
d_WH['nutscode'] = ""
for i in range(0, d_WH.shape[0]):
    d_WH['country'][i] = d_WH.index[i][1]
    d_WH['hour'][i] = int(d_WH.index[i][2])
    d_WH['nutscode'][i] = d_WH.index[i][0]
    d_WH['TIME'][i] = d_WH.index[i][3]


p_WH =p_WH.apply(pd.to_numeric)

p_WH['country'] = ""
p_WH['hour'] = ""
p_WH['TIME'] = ""
p_WH['nutscode'] = ""
for i in range(0, p_WH.shape[0]):
    p_WH['country'][i] = p_WH.index[i][1]
    p_WH['hour'][i] = int(p_WH.index[i][2])
    p_WH['nutscode'][i] = p_WH.index[i][0]
    p_WH['TIME'][i] = p_WH.index[i][3]


########################################
# identify error
p_star = p_WH.iloc[0:p_WH.shape[0],0:33]#*.75

d_excess = d_WH.iloc[0:d_WH.shape[0],0:33] -p_star

d_excess['nutscode'] = d_WH['nutscode']
d_excess['hour'] = d_WH['hour']
d_excess['TIME'] = d_WH['TIME']


for year in range(2018-2018,2050+1-2018):
    yr = d_excess.columns[year]
    d_neg = d_excess[d_excess[yr]>0]
    print(yr)
    reg_change = set(d_neg['nutscode'])    
    reg_look = []
    for i in reg_change:
        print(i)
        temp2 = d_neg[d_neg['nutscode']==i]
        months = set(temp2['TIME'])
        for mon in months:
            print(mon)
            temp3 = temp2[temp2['TIME']==mon]
            dist_amt = sum(temp3[yr])
            #distribution of energy
            hour_rem = list(temp3['hour'])
            s_wh_temp = list(s_wh2[0:min(hour_rem)])
            s_wh_temp.extend(len(hour_rem)*[0])
            s_wh_temp.extend(list(s_wh2[max(hour_rem)+1:len(s_wh2)]))
            #normalize shares
            sum_s_wh = sum(s_wh_temp)
            for share in range(0, len(s_wh_temp)):
                s_wh_temp[share] = s_wh_temp[share]/sum_s_wh
            s_wh_temp = pd.DataFrame(s_wh_temp)
            #create df with final values to add or subtract from d_WH
            amt_ac_hour = s_wh_temp*dist_amt
            data = pd.DataFrame(temp3[yr].iloc[0:temp3.shape[0]])*-1 # values to subtract
            amt_ac_hour.iloc[temp3['hour'].iloc[0]:temp3['hour'].iloc[-1]+1] = data
            #edit d_WH
            #day  that violated peak assumption
            vio_hour = d_WH.iloc[temp3.index[0]]['hour'] # first row that vilated peak assumption
            vio_day = pd.DataFrame(d_WH.iloc[temp3.index[0]-vio_hour:temp3.index[0]+24-vio_hour][yr]) # day that violated peak assumption
            vio_day['adjust'] = ""
            for row in range(0,vio_day.shape[0]):
                vio_day['adjust'].iloc[row] = vio_day[yr].iloc[row] +amt_ac_hour[0].iloc[row]
            # if redistribution of the energy caused other hours to exceed p_star
            dist_amt2 =[]
            hour_surplus = []
            for row in range(0,vio_day.shape[0]): 
                if vio_day['adjust'].iloc[row] > vio_day['adjust'].iloc[vio_hour]:
                    reg_look.append(i)
                    print(row)
                    dist_amt2.append(vio_day['adjust'].iloc[row]-vio_day['adjust'].iloc[vio_hour])
                    hour_surplus.append(row)
                    vio_day['adjust'].iloc[row] = vio_day['adjust'].iloc[row] - (vio_day['adjust'].iloc[row]-vio_day['adjust'].iloc[vio_hour])
            hour_rem.extend(hour_surplus)
            if min(hour_rem) == 0:
                s_wh_temp = [0]
                s_wh_temp.extend(s_wh2[1:list(set(hour_rem))[1]])
                s_wh_temp.extend((len(hour_rem)-1)*[0])
                #s_wh_temp.extend(list(s_wh2[max(hour_rem)+1:len(s_wh2)]))
            else:
                s_wh_temp = list(s_wh2[0:min(hour_rem)])
                s_wh_temp.extend(len(hour_rem)*[0])
                s_wh_temp.extend(list(s_wh2[max(hour_rem)+1:len(s_wh2)]))
            dist_amt2 = sum(dist_amt2)
            #normalize shares
            sum_s_wh = sum(s_wh_temp)
            for share in range(0, len(s_wh_temp)):
                s_wh_temp[share] = s_wh_temp[share]/sum_s_wh
            s_wh_temp = pd.DataFrame(s_wh_temp)
            #create df with final values to add or subtract from d_AC
            amt_ac_hour = s_wh_temp*dist_amt2
            #adjust2 is the final values to replace respective values in d_AC
            vio_day['adjust2'] = ""
            for row in range(0,vio_day.shape[0]):
                vio_day['adjust2'].iloc[row] = vio_day['adjust'].iloc[row] +amt_ac_hour[0].iloc[row]
            #replace values in d_AC
            data = list(vio_day['adjust2'])
            # set d_WH with new data
            d_WH.loc[min(vio_day.index):max(vio_day.index),yr] =  data

#Check results

# identify error
p_star = p_WH.iloc[0:p_WH.shape[0],0:33]#*.75

d_excess = d_WH.iloc[0:d_WH.shape[0],0:33] -p_star

d_excess['nutscode'] = d_WH['nutscode']
d_excess['hour'] = d_WH['hour']
d_excess['TIME'] = d_WH['TIME']

for year in range(2018-2018,2050+1-2018):
    yr = d_excess.columns[year]
    d_neg = d_excess[d_excess[yr]>0]
    print(yr)
    reg_change = set(d_neg['nutscode'])  
    print(len(reg_change))
    
    
p_WH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_WHV6.csv')       
d_WH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_WHV6.csv') 

########################################
del p_WH
del d_WH
########
# sh - storage heater
# the calculation of water heater will use Gils 2014 method using number of full load hours as a function of HDD and assume that there is no change in the efficiency of the appliance
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_SH = pd.DataFrame(index = index, columns = columns)   
p_SH = pd.DataFrame(index = index, columns = columns)   

s_sh =s_allelse.S_SH # hour share of daily demand
s_sh2 =s_sh # hour share of daily demand
s_sh = s_sh.append([s_sh]*11,ignore_index=True)

for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_SH.index[(row-1)*288][0]
    NHH = nhh.loc[region]           # number of households
    YR_HDD = yr_hdd.loc[region]     # annual HDD
    RSH = rsh.loc[region]           # rate of ownership of SH
    NFLH_SH = (YR_HDD/1000)*150+200  # number of full load hours of SH
    PUNIT_SH = 14                    # unit installed capacity; assumed constant across years kW
    WUNIT_SH = NFLH_SH*PUNIT_SH     # annual electricity demand per unit of SH; kWh
    W_SH = WUNIT_SH*NHH*RSH         # national annual electricity demand for SH; kWh
    S_HDD = s_hdd.loc[region]/30
    #FOR HOURLY DEMAND
    temp = NFLH_SH*PUNIT_SH*NHH*RSH*S_HDD/1/1000 #hourly; MWh
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for yr in range(0,temp.shape[1]): # convert from daily to hourly
        temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_sh      
    low = (row-1)*288
    high = row*288
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        d_SH.iloc[low:high,year] = data
    #for pinst - installed capacity NUTS2 level
    temp = pd.DataFrame(NHH*RSH*PUNIT_SH/1000).T
    temp = temp.append([temp]*11,ignore_index=True)
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for year in range(2018-2018,2050+1-2018):
        data = list(temp.iloc[0:288,year])
        p_SH.iloc[low:high,year] = data
        
d_SH =d_SH.apply(pd.to_numeric)  

d_SH['country'] = ""
d_SH['hour'] = ""
d_SH['TIME'] = ""
d_SH['nutscode'] = ""
for i in range(0, d_SH.shape[0]):
    d_SH['country'][i] = d_SH.index[i][1]
    d_SH['hour'][i] = int(d_SH.index[i][2])
    d_SH['nutscode'][i] = d_SH.index[i][0]
    d_SH['TIME'][i] = d_SH.index[i][3]



p_SH =p_SH.apply(pd.to_numeric)

p_SH['country'] = ""
p_SH['hour'] = ""
p_SH['TIME'] = ""
p_SH['nutscode'] = ""
for i in range(0, p_SH.shape[0]):
    p_SH['country'][i] = p_SH.index[i][1]
    p_SH['hour'][i] = int(p_SH.index[i][2])
    p_SH['nutscode'][i] = p_SH.index[i][0]
    p_SH['TIME'][i] = p_SH.index[i][3]

########################################
# identify error
p_star = p_SH.iloc[0:p_SH.shape[0],0:33]#*.75

d_excess = d_SH.iloc[0:d_SH.shape[0],0:33] -p_star

d_excess['nutscode'] = d_SH['nutscode']
d_excess['hour'] = d_SH['hour']
d_excess['TIME'] = d_SH['TIME']


for year in range(2018-2018,2050+1-2018):
    yr = d_excess.columns[year]
    d_neg = d_excess[d_excess[yr]>0]
    print(yr)
    reg_change = set(d_neg['nutscode'])    
    reg_look = []
    for i in reg_change:
        print(i)
        temp2 = d_neg[d_neg['nutscode']==i]
        months = set(temp2['TIME'])
        for mon in months:
            print(mon)
            temp3 = temp2[temp2['TIME']==mon]
            dist_amt = sum(temp3[yr])
            #distribution of energy
            hour_rem = list(temp3['hour'])
            s_sh_temp = list(s_sh2[0:min(hour_rem)])
            s_sh_temp.extend(len(hour_rem)*[0])
            s_sh_temp.extend(list(s_sh2[max(hour_rem)+1:len(s_sh2)]))
            #normalize shares
            sum_s_sh = sum(s_sh_temp)
            for share in range(0, len(s_sh_temp)):
                s_sh_temp[share] = s_sh_temp[share]/sum_s_sh
            s_sh_temp = pd.DataFrame(s_sh_temp)
            #create df with final values to add or subtract from d_sh
            amt_ac_hour = s_sh_temp*dist_amt
            data = pd.DataFrame(temp3[yr].iloc[0:temp3.shape[0]])*-1 # values to subtract
            amt_ac_hour.iloc[temp3['hour'].iloc[0]:temp3['hour'].iloc[-1]+1] = data
            #edit d_SH
            #day  that violated peak assumption
            vio_hour = d_SH.iloc[temp3.index[0]]['hour'] # first row that vilated peak assumption
            vio_day = pd.DataFrame(d_SH.iloc[temp3.index[0]-vio_hour:temp3.index[0]+24-vio_hour][yr]) # day that violated peak assumption
            vio_day['adjust'] = ""
            for row in range(0,vio_day.shape[0]):
                vio_day['adjust'].iloc[row] = vio_day[yr].iloc[row] +amt_ac_hour[0].iloc[row]
            # if redistribution of the energy caused other hours to exceed p_star
            dist_amt2 =[]
            hour_surplus = []
            for row in range(0,vio_day.shape[0]): 
                if vio_day['adjust'].iloc[row] > vio_day['adjust'].iloc[vio_hour]:
                    reg_look.append(i)
                    print(row)
                    dist_amt2.append(vio_day['adjust'].iloc[row]-vio_day['adjust'].iloc[vio_hour])
                    hour_surplus.append(row)
                    vio_day['adjust'].iloc[row] = vio_day['adjust'].iloc[row] - (vio_day['adjust'].iloc[row]-vio_day['adjust'].iloc[vio_hour])
            hour_rem.extend(hour_surplus)
            if min(hour_rem) == 0:
                s_sh_temp = [0]
                s_sh_temp.extend(s_sh2[1:list(set(hour_rem))[1]])
                s_sh_temp.extend((len(hour_rem)-1)*[0])
                #s_sh_temp.extend(list(s_sh2[max(hour_rem)+1:len(s_sh2)]))
            else:
                s_sh_temp = list(s_sh2[0:min(hour_rem)])
                s_sh_temp.extend(len(hour_rem)*[0])
                s_sh_temp.extend(list(s_sh2[max(hour_rem)+1:len(s_sh2)]))
            dist_amt2 = sum(dist_amt2)
            #normalize shares
            sum_s_sh = sum(s_sh_temp)
            for share in range(0, len(s_sh_temp)):
                s_sh_temp[share] = s_sh_temp[share]/sum_s_sh
            s_sh_temp = pd.DataFrame(s_sh_temp)
            #create df with final values to add or subtract from d_AC
            amt_ac_hour = s_sh_temp*dist_amt2
            #adjust2 is the final values to replace respective values in d_AC
            vio_day['adjust2'] = ""
            for row in range(0,vio_day.shape[0]):
                vio_day['adjust2'].iloc[row] = vio_day['adjust'].iloc[row] +amt_ac_hour[0].iloc[row]
            #replace values in d_AC
            data = list(vio_day['adjust2'])
            # set d_SH with new data
            d_SH.loc[min(vio_day.index):max(vio_day.index),yr] =  data

#Check results

# identify error
p_star = p_SH.iloc[0:p_SH.shape[0],0:33]#*.75

d_excess = d_SH.iloc[0:d_SH.shape[0],0:33] -p_star

d_excess['nutscode'] = d_SH['nutscode']
d_excess['hour'] = d_SH['hour']
d_excess['TIME'] = d_SH['TIME']

for year in range(2018-2018,2050+1-2018):
    yr = d_excess.columns[year]
    d_neg = d_excess[d_excess[yr]>0]
    print(yr)
    reg_change = set(d_neg['nutscode'])  
    print(len(reg_change))
##############################################

p_SH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_SHV6.csv')       
d_SH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_SHV6.csv')   


del S_HDD
del PUNIT_SH
del PUNIT_WH
del NFLH_SH
del NFLH_WH
del WUNIT_SH
del WUNIT_WH
del RSH
del RWH
del YR_HDD
del d_SH
del p_SH
del temp
###########
## EV - Electric vehicle
## assumes charging characteristic is the same between countries (i.e. timing of chage, charger capacities, and EV battery characteristics)
## assumes every EV plugs into the grid every day
## assumes average charging outlets charge at 3.6 kW, used to determine installed capacity
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_EV = pd.DataFrame(index = index, columns = columns)   
p_EV = pd.DataFrame(index = index, columns = columns)   

s_ev = pd.DataFrame(s_ev.S_EV) # hourly shares of annual energy demand
WUNIT_EV = wunit_ev/1000      # annual energy consumed by 1 Electric Vehicle MWh
PINST_EV    = rev*3.6/1000
for row in range(0,wunit_ev.shape[0]):#
    print(row)
    region  = wunit_ev.index[row]
    W_EV =  pd.DataFrame(rev.loc[region]*int(WUNIT_EV.loc[region]))
    temp    = pd.DataFrame(W_EV).T     # annual energy consumption for all EVs in region for '18-'50
    temp1   = pd.DataFrame(np.dot(s_ev/12/30,temp)) #  hourly energy consumption for EVs in region for '18-'50
    temp2   = pd.DataFrame(np.dot(s_ev/12/30,temp)) 
    for i in range(0,12-1): # expand for representative hours in year y
        temp1 = temp1.append(temp2, sort=True)
    temp1 = temp1.reset_index()
    temp1 = temp1.drop(['index'],axis=1)
    low =  (row)*288
    high = (row+1)*288   
    for year in range(2018-2018,2050+1-2018):
        print(year)
        data = list(temp1.iloc[0:288,year])
        d_EV.iloc[low:high,year] = data
    # p_EV
    ptemp    = pd.DataFrame(PINST_EV.loc[region]).T
    ptemp2   = pd.DataFrame(PINST_EV.loc[region]).T
    for i in range(0,12*24-1): # expand for representative hours in year y
        ptemp = ptemp.append(ptemp2, sort=True)
    ptemp = ptemp.reset_index()
    ptemp = ptemp.drop(['index'],axis=1)
    for year in range(2018-2018,2050+1-2018):
        data = list(ptemp.iloc[0:288,year])
        p_EV.iloc[low:high,year] = data    
    
d_EV =d_EV.apply(pd.to_numeric)  

d_EV['country'] = ""
d_EV['hour'] = ""
d_EV['TIME'] = ""
d_EV['nutscode'] = ""
for i in range(0, d_EV.shape[0]):
    d_EV['country'][i] = d_EV.index[i][1]
    d_EV['hour'][i] = int(d_EV.index[i][2])
    d_EV['nutscode'][i] = d_EV.index[i][0]
    d_EV['TIME'][i] = d_EV.index[i][3]



p_EV =p_EV.apply(pd.to_numeric)

p_EV['country'] = ""
p_EV['hour'] = ""
p_EV['TIME'] = ""
p_EV['nutscode'] = ""
for i in range(0, p_EV.shape[0]):
    p_EV['country'][i] = p_EV.index[i][1]
    p_EV['hour'][i] = int(p_EV.index[i][2])
    p_EV['nutscode'][i] = p_EV.index[i][0]
    p_EV['TIME'][i] = p_EV.index[i][3]    

p_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_EVV6.csv')       
d_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_EVV6.csv')   

del p_EV
del d_EV 
        
        

###########
# FIT FOR 55
###########
## EV - Electric vehicle
## assumes charging characteristic is the same between countries (i.e. timing of chage, charger capacities, and EV battery characteristics)
## assumes every EV plugs into the grid every day
## assumes average charging outlets charge at 3.6 kW, used to determine installed capacity
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_EV = pd.DataFrame(index = index, columns = columns)   
p_EV = pd.DataFrame(index = index, columns = columns)   

s_ev = pd.DataFrame(s_ev.S_EV) # hourly shares of annual energy demand
WUNIT_EV = wunit_ev/1000      # annual energy consumed by 1 Electric Vehicle MWh
PINST_EV    = rev*3.6/1000
for row in range(0,wunit_ev.shape[0]):#
    print(row)
    region  = wunit_ev.index[row]
    W_EV =  pd.DataFrame(rev_fit55.loc[region]*int(WUNIT_EV.loc[region]))
    temp    = pd.DataFrame(W_EV).T     # annual energy consumption for all EVs in region for '18-'50
    temp1   = pd.DataFrame(np.dot(s_ev/12/30,temp)) #  hourly energy consumption for EVs in region for '18-'50
    temp2   = pd.DataFrame(np.dot(s_ev/12/30,temp)) 
    for i in range(0,12-1): # expand for representative hours in year y
        temp1 = temp1.append(temp2, sort=True)
    temp1 = temp1.reset_index()
    temp1 = temp1.drop(['index'],axis=1)
    low =  (row)*288
    high = (row+1)*288   
    for year in range(2018-2018,2050+1-2018):
        print(year)
        data = list(temp1.iloc[0:288,year])
        d_EV.iloc[low:high,year] = data
    # p_EV
    ptemp    = pd.DataFrame(PINST_EV.loc[region]).T
    ptemp2   = pd.DataFrame(PINST_EV.loc[region]).T
    for i in range(0,12*24-1): # expand for representative hours in year y
        ptemp = ptemp.append(ptemp2, sort=True)
    ptemp = ptemp.reset_index()
    ptemp = ptemp.drop(['index'],axis=1)
    for year in range(2018-2018,2050+1-2018):
        data = list(ptemp.iloc[0:288,year])
        p_EV.iloc[low:high,year] = data    
    
d_EV =d_EV.apply(pd.to_numeric)  

d_EV['country'] = ""
d_EV['hour'] = ""
d_EV['TIME'] = ""
d_EV['nutscode'] = ""
for i in range(0, d_EV.shape[0]):
    d_EV['country'][i] = d_EV.index[i][1]
    d_EV['hour'][i] = int(d_EV.index[i][2])
    d_EV['nutscode'][i] = d_EV.index[i][0]
    d_EV['TIME'][i] = d_EV.index[i][3]



p_EV =p_EV.apply(pd.to_numeric)

p_EV['country'] = ""
p_EV['hour'] = ""
p_EV['TIME'] = ""
p_EV['nutscode'] = ""
for i in range(0, p_EV.shape[0]):
    p_EV['country'][i] = p_EV.index[i][1]
    p_EV['hour'][i] = int(p_EV.index[i][2])
    p_EV['nutscode'][i] = p_EV.index[i][0]
    p_EV['TIME'][i] = p_EV.index[i][3]    

p_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_EVV6_fit55.csv')       
d_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_EVV6_fit55.csv')   

del p_EV
del d_EV 
        


##########
# refridgerator
NHH = nhh             # number of households
WUNIT_RF = wunit_rf_fr#.loc[region]  # energy requirements of one year
RRF = rrf#.loc[region]               # rate of ownership
#FOR HOURLY DEMAND
temp = pd.DataFrame(WUNIT_RF*NHH*RRF/1/12/30/24/1000) # hourly
temp= temp.reset_index()
temp2 = pd.DataFrame(WUNIT_RF*NHH*RRF/1/12/30/24/1000)
temp2= temp2.reset_index()
for i in range(0,12*24-1): # expand for representative hours in year y
    temp = temp.append(temp2, sort=True)
temp =temp.sort_values(by = "nutscode")
temp = temp.drop('nutscode',axis = 1)
temp = temp.apply(pd.to_numeric)
temp = temp.reset_index()
temp = temp.drop('index', axis = 1)
d_RF = temp    
d_RF['hour'] = index['hour']
d_RF['TIME'] = index['time']
d_RF['nutscode'] = index['nutscode']
d_RF['country'] = index['country']
    # power from ref can only be delayed of reduced
# installed capacity
temp = pd.DataFrame(WUNIT_RF*NHH*RRF/1/12/30/8/1000) # average RF runs for 8 hours perday; see Stamminger 2008
temp= temp.reset_index()
temp2 = pd.DataFrame(WUNIT_RF*NHH*RRF/1/12/30/8/1000)
temp2= temp2.reset_index()
for i in range(0,12*24-1): # expand for representative hours in year y
    temp = temp.append(temp2, sort=True)
temp =temp.sort_values(by = "nutscode")
temp = temp.drop('nutscode',axis = 1)
temp = temp.apply(pd.to_numeric)
temp = temp.reset_index()
temp = temp.drop('index', axis = 1)
p_RF = temp    
p_RF['hour'] = index['hour']
p_RF['TIME'] = index['time']
p_RF['nutscode'] = index['nutscode']
p_RF['country'] = index['country']
    
del temp
del temp2
d_RF.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_RFV4.csv')
p_RF.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_RFV4.csv')   
del d_RF
del p_RF

##########
# freezer
NHH = nhh               # number of households
WUNIT_FR = wunit_rf_fr  # energy requirements of one year
RFR = rfr               # rate of ownership
#FOR HOURLY DEMAND
temp = pd.DataFrame(WUNIT_FR*NHH*RFR/1/12/30/24/1000) # hourly
temp= temp.reset_index()
temp2 = pd.DataFrame(WUNIT_FR*NHH*RFR/1/12/30/24/1000)
temp2= temp2.reset_index()
for i in range(0,12*24-1): # expand for representative hours in year y
    temp = temp.append(temp2, sort=True)
temp =temp.sort_values(by = "nutscode")
temp = temp.drop('nutscode',axis = 1)
temp = temp.apply(pd.to_numeric)
temp = temp.reset_index()
temp = temp.drop('index', axis = 1)
d_FR = temp    
d_FR['hour'] = index['hour']
d_FR['TIME'] = index['time']
d_FR['nutscode'] = index['nutscode']
d_FR['country'] = index['country']
    # power from ref can only be delayed of reduced
# installed capacity
temp = pd.DataFrame(WUNIT_FR*NHH*RFR/1/12/30/8/1000) # average RF runs for 8 hours perday; see Stamminger 2008
temp= temp.reset_index()
temp2 = pd.DataFrame(WUNIT_FR*NHH*RFR/1/12/30/8/1000)
temp2= temp2.reset_index()
for i in range(0,12*24-1): # expand for representative hours in year y
    temp = temp.append(temp2, sort=True)
temp =temp.sort_values(by = "nutscode")
temp = temp.drop('nutscode',axis = 1)
temp = temp.apply(pd.to_numeric)
temp = temp.reset_index()
temp = temp.drop('index', axis = 1)
p_FR = temp    
p_FR['hour'] = index['hour']
p_FR['TIME'] = index['time']
p_FR['nutscode'] = index['nutscode']
p_FR['country'] = index['country']
del temp
del temp2

d_FR.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_FRV4.csv')
p_FR.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_FRV4.csv')
del d_FR
del p_FR


#############
# appliances with hourly variation
s_wash = s_wash.sort_values(by=['nutscode','hour'])
s_wash = s_wash.reset_index()
s_wash =  s_wash.drop('index',axis = 1)
index_h = s_wash[['nutscode', 'hour']]
# NHH_H can be used for all washing appliances
NHH_h   = pd.merge(NHH,index_h, left_on = NHH.index, right_on = 'nutscode')                   # number of households
NHH_h = NHH_h.drop(['nutscode','hour'], axis =1)

## WM - washing machine

RWM_h   = pd.merge(rwm,index_h, left_on = rwm.index, right_on = 'nutscode')                   # energy requirements of one cycle
PCYCLE_WM   = pd.merge(pcycle_wm,index_h, left_on = pcycle_wm.index, right_on = 'nutscode') # rate of ownership
# order of nutscode and hour is preserved, drop to allow matrix multiplication
RWM_h = RWM_h.drop(['nutscode','hour'], axis =1)
PCYCLE_WM = PCYCLE_WM.drop(['nutscode','hour'], axis =1)

# PCYCLE_WM*duration* # cycles per year; duration and cycles per year are expected to remain constant GILS '14 table 8 and pg 22 Gils dissertation
PCYCLE_WM_A = PCYCLE_WM*2*146 #annual energy required for one WM

S_WM = s_wash['S_WM']
S_WM2 = s_wash['S_WM']
for year in range(0,2050-2018):
    S_WM = pd.concat([S_WM, S_WM2], axis=1, join="inner")
S_WM=S_WM.apply(pd.to_numeric)
S_WM.columns = NHH_h.columns
#FOR HOURLY DEMAND
d_WM = pd.DataFrame(NHH_h*RWM_h*PCYCLE_WM_A*S_WM/1/30/12/1000) # hourly; PC
p_WM = pd.DataFrame(NHH_h*RWM_h*PCYCLE_WM/1000) # hourly


d_WM['hour'] = index_h['hour']
d_WM['nutscode'] = index_h['nutscode']
p_WM['hour'] = index_h['hour']
p_WM['nutscode'] = index_h['nutscode']

p_WM2 = pd.DataFrame(NHH_h*RWM_h*PCYCLE_WM/1000) # hourly
p_WM2['hour'] = index_h['hour']
p_WM2['nutscode'] = index_h['nutscode']
for i in range(0,12-1): # expand for representative hours in year y; currently no monthly variation
    p_WM = p_WM.append(p_WM2, sort=True)
    

d_WM2 = pd.DataFrame(NHH_h*RWM_h*PCYCLE_WM_A*S_WM/1/30/12/1000) # hourly
d_WM2['hour'] = index_h['hour']
d_WM2['nutscode'] = index_h['nutscode']
for i in range(0,12-1): # expand for representative hours in year y; currently no monthly variation
    d_WM = d_WM.append(d_WM2, sort=True)
    
del RWM_h
del PCYCLE_WM
del d_WM2
del p_WM2

## TD - tumble drier

RTD_h   = pd.merge(rtd,index_h, left_on = rtd.index, right_on = 'nutscode')                   # energy requirements of one cycle
PCYCLE_TD   = pd.merge(pcycle_td,index_h, left_on = pcycle_td.index, right_on = 'nutscode') # rate of ownership
# order of nutscode and hour is preserved, drop to allow matrix multiplication
RTD_h = RTD_h.drop(['nutscode','hour'], axis =1)
PCYCLE_TD = PCYCLE_TD.drop(['nutscode','hour'], axis =1)

# PCYCLE_TD*duration* # cycles per year; duration and cycles per year are expected to remain constant GILS '14 table 8 and pg 22 Gils dissertation
PCYCLE_TD_A = PCYCLE_TD*2*102

S_TD = s_wash['S_TD']
S_TD2 = s_wash['S_TD']
for year in range(0,2050-2018):
    S_TD = pd.concat([S_TD, S_TD2], axis=1, join="inner")
S_TD=S_TD.apply(pd.to_numeric)
S_TD.columns = NHH_h.columns
#FOR HOURLY DEMAND
d_TD = pd.DataFrame(NHH_h*RTD_h*PCYCLE_TD_A*S_TD/1/30/12/1000) # hourly, uses annnual PCYCLE
p_TD = pd.DataFrame(NHH_h*RTD_h*PCYCLE_TD/1000) # hourly


d_TD['hour'] = index_h['hour']
d_TD['nutscode'] = index_h['nutscode']
p_TD['hour'] = index_h['hour']
p_TD['nutscode'] = index_h['nutscode']

p_TD2 = pd.DataFrame(NHH_h*RTD_h*PCYCLE_TD/1000) # hourly
p_TD2['hour'] = index_h['hour']
p_TD2['nutscode'] = index_h['nutscode']
for i in range(0,12-1): # expand for representative hours in year y; currently no monthly variation
    p_TD = p_TD.append(p_TD2, sort=True)
    

d_TD2 = pd.DataFrame(NHH_h*RTD_h*PCYCLE_TD_A*S_TD/1/30/12/1000) # hourly
d_TD2['hour'] = index_h['hour']
d_TD2['nutscode'] = index_h['nutscode']
for i in range(0,12-1): # expand for representative hours in year y; currently no monthly variation
    d_TD = d_TD.append(d_TD2, sort=True)    
    
del RTD_h
del PCYCLE_TD
del d_TD2
del p_TD2

## DW - dish washer

RDW_h   = pd.merge(rdw,index_h, left_on = rdw.index, right_on = 'nutscode')                   # energy requirements of one cycle
PCYCLE_DW   = pd.merge(pcycle_dw,index_h, left_on = pcycle_dw.index, right_on = 'nutscode') # rate of ownership
# order of nutscode and hour is preserved, drop to allow matrix multiplication
RDW_h = RDW_h.drop(['nutscode','hour'], axis =1)
PCYCLE_DW = PCYCLE_DW.drop(['nutscode','hour'], axis =1)

# PCYCLE_DW*duration* # cycles per year; duration and cycles per year are expected to remain constant GILS '14 table 8 and pg 22 Gils dissertation
PCYCLE_DW_A = PCYCLE_DW*2*208

S_DW = s_wash['S_DW']
S_DW2 = s_wash['S_DW']
for year in range(0,2050-2018):
    S_DW = pd.concat([S_DW, S_DW2], axis=1, join="inner")
S_DW=S_DW.apply(pd.to_numeric)
S_DW.columns = NHH_h.columns
#FOR HOURLY DEMAND
d_DW = pd.DataFrame(NHH_h*RDW_h*PCYCLE_DW_A*S_DW/1/30/12/1000) # hourly
p_DW = pd.DataFrame(NHH_h*RDW_h*PCYCLE_DW/1000) # hourly


d_DW['hour'] = index_h['hour']
d_DW['nutscode'] = index_h['nutscode']
p_DW['hour'] = index_h['hour']
p_DW['nutscode'] = index_h['nutscode']

p_DW2 = pd.DataFrame(NHH_h*RDW_h*PCYCLE_DW/1000) # hourly
p_DW2['hour'] = index_h['hour']
p_DW2['nutscode'] = index_h['nutscode']
for i in range(0,12-1): # expand for representative hours in year y; currently no monthly variation
    p_DW = p_DW.append(p_DW2, sort=True)
    

d_DW2 = pd.DataFrame(NHH_h*RDW_h*PCYCLE_DW_A*S_DW/1/30/12/1000) # hourly
d_DW2['hour'] = index_h['hour']
d_DW2['nutscode'] = index_h['nutscode']
for i in range(0,12-1): # expand for representative hours in year y; currently no monthly variation
    d_DW = d_DW.append(d_DW2, sort=True)    
    
del RDW_h
del PCYCLE_DW
del d_DW2
del p_DW2    

# sort dataframes by nutscode and hour
#WM
d_WM = d_WM.sort_values(by = ['nutscode','hour'])
d_WM = d_WM.reset_index()
d_WM = d_WM.drop('index',axis=1)
p_WM = p_WM.sort_values(by = ['nutscode','hour'])
p_WM = p_WM.reset_index()
p_WM = p_WM.drop('index',axis=1)
#TD
d_TD = d_TD.sort_values(by = ['nutscode','hour'])
d_TD = d_TD.reset_index()
d_TD = d_TD.drop('index',axis=1)
p_TD = p_TD.sort_values(by = ['nutscode','hour'])
p_TD = p_TD.reset_index()
p_TD = p_TD.drop('index',axis=1)
#DW
d_DW = d_DW.sort_values(by = ['nutscode','hour'])
d_DW = d_DW.reset_index()
d_DW = d_DW.drop('index',axis=1)
p_DW = p_DW.sort_values(by = ['nutscode','hour'])
p_DW = p_DW.reset_index()
p_DW = p_DW.drop('index',axis=1)

# creat an index that coincides with the washing appliance dfs
index_h = pd.DataFrame(index[['time','country','hour','nutscode']]).sort_values(by = ['nutscode','hour'])
index_h = index_h.reset_index()

# add TIME and country to washing appliances
d_WM['TIME'] = index_h['time']
p_WM['TIME']= index_h['time']
d_TD['TIME']= index_h['time']
p_TD['TIME']= index_h['time']
d_DW['TIME']= index_h['time']
p_DW['TIME']= index_h['time']
    
d_WM['country']= index_h['country']
p_WM['country']= index_h['country']
d_TD['country']= index_h['country']
p_TD['country']= index_h['country']
d_DW['country']= index_h['country']
p_DW['country']= index_h['country']




d_WM.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_WMV4.csv')
d_TD.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_TDV4.csv')
d_DW.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_DWV4.csv')
del d_WM
del d_TD
del d_DW

p_WM.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_WMV4.csv')
p_TD.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_TDV4.csv')
p_DW.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_DWV4.csv')
del p_WM
del p_TD
del p_DW
    