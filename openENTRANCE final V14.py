"""
The objective of this script is to solve for European household energy demand from 2018-2050
Difference between version 7 and 8 are the file locations and version 8 uses the updated file for EV NUTS regions
Difference between version 8 and 9 is the adjustment to the circulation pump 
Differnence between version 9 and 10 is the inclusion of heat pumps
Difference between version 10 and 11 is the use of new EV data and fitfor55 EV scenario
Difference between version 11 and 12 is that 12 refrences the correct shares for washing devices 
    and changes the reference/file location of all file so that every data set that is referenced in this script is in ./openENTRANCE final data
    Air conditioning has a new method to correct for demand exceeding installed capacity. It reduces the number of NFLH until no hours during the
    year exceed capacity instead of the previous method which distributes the excess energy throughout the day
Difference between 12 and 13 is that 13 references new files for COP and HDD and CDD that were created using long run averages from EOBS Copernicus database
additionally while statements were added following the same method in version 12 for air conditioning, however, using the new temperature data from EOBS fixed the problem
and thus the while statements were not activated and are not neccessary.
Difference between 13 and 14 is that 14 references Qhp_thermal_MWh_projectedV2 not V1
"""

import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os

os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/openENTRANCE final data')

# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

### END - global options
### Load in data

# parameters
nhh = pd.read_csv('./nhhV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
#nhh = nhh.dropna()
nhh.index = nhh['nutscode']
# drop unnecessary NUTS regions and Islands
nhh = nhh.drop(['MT00','IS00', 'LI00', 'UKI1', 'UKI2', 'UKM2', 'UKM3', 'ES64','PT20','FRY1','FRY2','FRY3','FRY4','FRY5'], axis = 0)
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

wunit_ev =  pd.read_excel('./EV_parameters.xlsx')

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

rev = pd.read_csv('./EV NUTS projectionsV5.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
rev_fit55 = pd.read_csv('./EV NUTS projectionsV5_fit55.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 


# add data for Electric Vehicles
# electric vehicle hour shares
# file created using R 'hourly share calculation.R'
s_ev=pd.read_csv('./hourlyEVshares.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_ev=s_ev.drop(['Unnamed: 0'],axis=1)

# add shares for Tumble Dryer, Washing Machine and Dish Washer; from Stamminger
s_wash =pd.read_csv('./s_wash nuts_V2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_wash = s_wash[s_wash['nutscode']!= "NO0B"] # remove NO0B due to missing data in other categories
s_wash = s_wash[s_wash['nutscode']!= "MT00"] # remove MT00 due to missing data in other categories

# add shares for s_hdd & s_cdd
s_hdd =pd.read_csv('./s_hdd nutsV3.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_cdd=pd.read_csv('./s_cdd nutsV3.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
# add shares for CP, WH, SH, AC
s_allelse = pd.read_csv('./stamminger_2009.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

# add share for hp
s_hp = pd.read_csv('./heat_pump_hourly_share.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
s_hp.columns = ['hour',"S_HP"]

# add data for yr_hdd & yr_cdd
yr_hdd =pd.read_csv('./yr_hdd nutsV3.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
yr_cdd=pd.read_csv('./yr_cdd nutsV3.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

#thermal provision of energy from HP
Q_hp_thermal =pd.read_csv('./Qhp_thermal_MWh_projectedV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

#thermal heat requirement by NTUS0 
Q_NUTS0_thermal =pd.read_csv('./NUTS0_thermal_heat_annum.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

# cop for hp by nuts 2 region
cop = pd.read_csv("./COP_.1deg_11-21_V1.csv",sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 
cop = cop.drop(['Unnamed: 0','yr_CCOP'], axis=1)
cop.columns = ['nutscode', 'Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'August', 'Septmber', 'October', 'November', 'December']

#thermal provision of energy from HP by nuts 2 region
num_hp =pd.read_csv('./Qhp_thermal_MWh_projectedV2.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 


# expand datasets to represent nuts 2 regions
temp = nhh[['nutscode']]
temp['country']= ""
for row in range(0,len(temp)):
    temp['country'][row] = temp['nutscode'][row][0:2]
temp = temp.sort_values('nutscode')


# # full load hours
nflh_ac = nflh_ac.merge(temp,sort=True)
nflh_ac = nflh_ac.drop('country', axis=1)
nflh_ac.index = nflh_ac['nutscode']
nflh_ac = nflh_ac.drop('nutscode', axis=1)    
    
nflh_cp = nflh_cp.merge(temp,sort=True)
nflh_cp = nflh_cp.drop('country', axis=1)
nflh_cp.index = nflh_cp['nutscode']
nflh_cp = nflh_cp.drop('nutscode', axis=1)    

# power p cycle
pcycle_wm = pcycle_wm.merge(temp,sort=True)
pcycle_wm = pcycle_wm.drop('country', axis=1)
pcycle_wm.index = pcycle_wm['nutscode']
pcycle_wm = pcycle_wm.drop('nutscode', axis=1)  

pcycle_td = pcycle_td.merge(temp,sort=True)
pcycle_td = pcycle_td.drop('country', axis=1)
pcycle_td.index = pcycle_td['nutscode']
pcycle_td = pcycle_td.drop('nutscode', axis=1)  

pcycle_dw = pcycle_dw.merge(temp,sort=True)
pcycle_dw = pcycle_dw.drop('country', axis=1)
pcycle_dw.index = pcycle_dw['nutscode']
pcycle_dw = pcycle_dw.drop('nutscode', axis=1)  

# unit capacity
wunit_rf_fr = wunit_rf_fr.merge(temp,sort=True)
wunit_rf_fr = wunit_rf_fr.drop('country', axis=1)
wunit_rf_fr.index = wunit_rf_fr['nutscode']
wunit_rf_fr = wunit_rf_fr.drop('nutscode', axis=1)      


wunit_ev = wunit_ev.merge(temp,sort=True)
wunit_ev = wunit_ev.drop(['country','evLIFE_150kkm','average age/# years assuming 150k life'], axis=1)
wunit_ev = wunit_ev.sort_values('nutscode')
wunit_ev.index = wunit_ev['nutscode']
wunit_ev = wunit_ev.drop('nutscode', axis=1)      

# hp thermal energy demand
Q_hp_thermal = Q_hp_thermal.merge(temp,sort=True)
Q_hp_thermal = Q_hp_thermal.drop(['country'], axis=1)
Q_hp_thermal = Q_hp_thermal.sort_values('nutscode')
Q_hp_thermal.index = Q_hp_thermal['nutscode']
Q_hp_thermal = Q_hp_thermal.drop('nutscode', axis=1)  

# hp thermal energy demand
cop = cop.reset_index()
cop = cop.merge(temp,sort=True)
cop = cop.drop(['country','index'], axis=1)
#cop = cop.sort_values('nutscode')
cop.index = cop['nutscode']
cop = cop.drop('nutscode', axis=1)  

num_hp = num_hp.merge(temp,sort=True)
num_hp.index = num_hp['nutscode']
num_hp = num_hp.drop(['nutscode','country'], axis=1)


# rates of ownership
rcp = rcp.merge(temp,sort=True)
rcp = rcp.drop('country', axis=1)
rcp.index = rcp['nutscode']
rcp = rcp.drop('nutscode', axis=1)

rdw = rdw.merge(temp,sort=True)
rdw = rdw.drop('country', axis=1)
rdw.index = rdw['nutscode']
rdw = rdw.drop('nutscode', axis=1)

rwm = rwm.merge(temp,sort=True)
rwm = rwm.drop('country', axis=1)
rwm.index = rwm['nutscode']
rwm = rwm.drop('nutscode', axis=1)

rfr = rfr.merge(temp,sort=True)
rfr = rfr.drop('country', axis=1)
rfr.index = rfr['nutscode']
rfr = rfr.drop('nutscode', axis=1)

rrf = rrf.merge(temp,sort=True)
rrf = rrf.drop('country', axis=1)
rrf.index = rrf['nutscode']
rrf = rrf.drop('nutscode', axis=1)

rsh = rsh.merge(temp,sort=True)
rsh = rsh.drop('country', axis=1)
rsh.index = rsh['nutscode']
rsh = rsh.drop('nutscode', axis=1)

rtd = rtd.merge(temp,sort=True)
rtd = rtd.drop('country', axis=1)
rtd.index = rtd['nutscode']
rtd = rtd.drop('nutscode', axis=1)

rwh = rwh.merge(temp,sort=True)
rwh = rwh.drop('country', axis=1)
rwh.index = rwh['nutscode']
rwh = rwh.drop('nutscode', axis=1)

rac = rac.merge(temp,sort=True)
rac = rac.drop('country', axis=1)
rac.index = rac['nutscode']
rac = rac.drop('nutscode', axis=1)

rev = rev.merge(temp,how = 'outer',sort=True)
rev = rev.drop('country', axis =1)
rev.index = rev['nutscode']
rev = rev.drop('nutscode', axis =1)
rev = rev.drop('Unnamed: 0', axis = 1)

rev_fit55 = rev_fit55.merge(temp,how = 'outer',sort=True)
rev_fit55 = rev_fit55.drop('country', axis =1)
rev_fit55.index = rev_fit55['nutscode']
rev_fit55 = rev_fit55.drop('nutscode', axis =1)
rev_fit55 = rev_fit55.drop('Unnamed: 0', axis = 1)

s_cdd = s_cdd.merge(temp,sort=True)
s_cdd.index = s_cdd['nutscode']
s_cdd = s_cdd.drop(['nutscode','month','country'],axis=1) #TIME is dropped from axis; order of months is maintained

s_hdd = s_hdd.merge(temp,sort=True)
s_hdd.index = s_hdd['nutscode']
s_hdd = s_hdd.drop(['nutscode','month','country'],axis=1) #TIME is dropped from axis; order of months is maintained

yr_cdd = yr_cdd.merge(temp,sort=True)
yr_cdd.index = yr_cdd['nutscode']
yr_cdd = yr_cdd.drop(['nutscode','month','country'],axis=1) #TIME is dropped from axis; order of months is maintained


yr_hdd = yr_hdd.merge(temp,sort=True)
yr_hdd.index = yr_hdd['nutscode']
yr_hdd = yr_hdd.drop(['nutscode','month','country'],axis=1) #TIME is dropped from axis; order of months is maintained



# change nhh, punit_ac, punit_cp to be in the same format as above
nhh.index = nhh['nutscode']
nhh = nhh.drop('nutscode',axis=1)

punit_ac.index = punit_ac['country']
punit_ac = punit_ac.drop('country',axis=1)

punit_cp.index = punit_cp['country']
punit_cp = punit_cp.drop('country',axis=1)

s_wash = s_wash.merge(temp,sort=True)

# create index for representative hours for each nuts 2 region
time = pd.read_csv('./time_index.csv', sep=",",encoding = "ISO-8859-1", header=0, index_col=False) 

# s_wash is arbitrarily chosen to create index
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
       
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_HP = pd.DataFrame(index = index, columns = columns)   
p_HP = pd.DataFrame(index = index, columns = columns)  
 

s_hp2 =s_hp.S_HP # hour share of daily demand

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
            temp_qyear.iloc[count,0:33] = temp_qmonth.iloc[month,0:33]*s_hp2[hour]/30 # divide by # days in the month ~30
            if count == 287:
                low = (row-1)*288
                high = row*288
                for year in range(2018-2018,2050+1-2018):
                    data = list(temp_qyear.iloc[0:288,year])
                    d_HP.iloc[low:high,year] = data               
                    
# solve for P_HP assuming HP installed cap = 12kWh
# p_cap_hp can never be greater than #hh*0.012


Q_NUTS0_thermal.index = Q_NUTS0_thermal['file_country_path']
Q_NUTS0_thermal = Q_NUTS0_thermal.drop(['file_country_path'],axis=1)

num_hp['country'] = ""

for row in range(0, num_hp.shape[0]):
        print(row)
        num_hp['country'][row] = num_hp.index[row][0:2]
        
for row in range(0, num_hp.shape[0]):
    print(row)
    NUTS0 = num_hp.index[row][0:2]
    for year in range(0, num_hp.shape[1]-1):
            num_hp.iloc[row,year] =     num_hp.iloc[row,year]/(Q_NUTS0_thermal.loc[NUTS0]['them_cap']/1000)


num_hp = num_hp.drop(['country'], axis =1)

# set limit for installed capacity
for row in range(0, num_hp.shape[0]):
    print(num_hp.index[row])
    for year in range(0, num_hp.shape[1]):
        if num_hp.iloc[row,year] / nhh.iloc[row,year] > 1:
            print(year)
            num_hp.iloc[row,year] = nhh.iloc[row,year]

p_inst_hp = num_hp*0.012 # 0.012 = the installed capacity of hp in mWh
p_inst_hp.index = num_hp.index
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
    
d_HP.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_HPV4.csv')  
   
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
    
p_HP.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_HPV4.csv')  


##########
# Air conditioning
    
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_AC = pd.DataFrame(index = index, columns = columns)   
p_AC = pd.DataFrame(index = index, columns = columns)  

s_ac =s_allelse.S_AC # hour share of daily demand
s_ac2 = s_ac
s_ac = s_ac.append([s_ac]*11,ignore_index=True)

for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_AC.index[(row-1)*288][0]
    NHH = nhh.loc[region]
    PUNIT_AC = punit_ac.loc[region[0:2]]
    NFLH_AC = nflh_ac.loc[region]
    RAC = rac.loc[region]
    S_CDD = s_cdd.loc[region] 
    # set constraint that NFLH_AC*PUNIT_AC*NHH*RAC*S_CDD <= .75*(NFLH_AC*PUNIT_AC*NHH*RAC/1000   *S_CDD)
    #FOR HOURLY DEMAND
    temp = NFLH_AC*PUNIT_AC*NHH*RAC*S_CDD/1/30/1000 # daily
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for yr in range(0,temp.shape[1]): # convert from daily to hourly
        temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_ac    
    # check and see if limit has been violated    
    check_limit = {'max_NUTS2':list(PUNIT_AC*NHH*RAC/1000),'observed_max':list(temp.max())}
    adj_nflh = pd.DataFrame(data = check_limit)
    adj_nflh['gt'] = adj_nflh['max_NUTS2'] <= adj_nflh['observed_max']
    adj_nflh['NFLH_AC'] = list(NFLH_AC)
    count = 0
    adj_nflh['adj_nflh'] = list(NFLH_AC)
    while True in list(adj_nflh['gt']): # while the constraint is violated adjust the number of FLH such that no day can have more than 1 FLH per hour
        count +=1
        print("Iteration", count)
        adj_nflh['nflh_change'] = 0
        adj_nflh['nflh_change'][adj_nflh['gt']== True] = 1
        adj_nflh['adj_nflh'] = adj_nflh['adj_nflh'] - adj_nflh['nflh_change']
        NFLH_AC2 = adj_nflh['adj_nflh']
        NFLH_AC2.index = NFLH_AC.index
        #FOR HOURLY DEMAND
        temp = NFLH_AC2*PUNIT_AC*NHH*RAC*S_CDD/1/30/1000 # daily
        temp['month']= range(1,13)
        temp = temp.append([temp]*23,ignore_index=True)
        temp = temp.sort_values(by='month')
        temp = temp.reset_index()
        temp = temp.drop(['index','month'],axis=1)
        for yr in range(0,temp.shape[1]): # convert from daily to hourly
            temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_ac    
        # check and see if limit has been violated    
        adj_nflh['observed_max'] = list(temp.max())
        adj_nflh['gt'] = adj_nflh['max_NUTS2'] <= adj_nflh['observed_max']
    nflh_ac.loc[region] =   list(adj_nflh['adj_nflh'])  
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
    
p_AC.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_ACV8.csv')       
d_AC.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_ACV8.csv')     
#write out put of the nflh algorithm to file
nflh_ac.to_csv(r'./nflh_ac_adjV2.csv')    

del NFLH_AC
del PUNIT_AC
del RAC
del S_CDD 

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
                #print("here")                                                 # less than 15% peak
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

     
d_CPadj.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_CPV6.csv')   


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


p_CP.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_CPV6.csv')       
 

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

#creat df with nflh_wh
nflh_WH_before = pd.DataFrame(index = set(index['nutscode']), columns = columns) 
nflh_WH_after = pd.DataFrame(index = set(index['nutscode']), columns = columns)   

for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_WH.index[(row-1)*288][0]
    NHH = nhh.loc[region]           # number of households
    YR_HDD = yr_hdd.loc[region]     # annual HDD
    RWH = rwh.loc[region]           # rate of ownership of WH
    NFLH_WH = (YR_HDD.iloc[0]/1000)*25+175  # number of full load hours of WH
    PUNIT_WH = 2                    # unit installed capacity; assumed constant across years kW
    WUNIT_WH = NFLH_WH*PUNIT_WH     # annual electricity demand per unit of WH; kWh
    W_WH = WUNIT_WH*NHH*RWH         # national annual electricity demand for WH; kWh
    S_HDD = pd.DataFrame(1/12/30,index = YR_HDD.index, columns = columns)   # every hour has the same energy demand 
    #FOR HOURLY DEMAND
    temp = NFLH_WH*PUNIT_WH*NHH*RWH*S_HDD/1/1000 #daily; MWh
    temp['month']= range(1,13)
    temp = temp.append([temp]*23,ignore_index=True)
    temp = temp.sort_values(by='month')
    temp = temp.reset_index()
    temp = temp.drop(['index','month'],axis=1)
    for yr in range(0,temp.shape[1]): # convert from daily to hourly
        temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_wh    
# check and see if limit has been violated    
    check_limit = {'max_NUTS2':list(PUNIT_WH*NHH*RWH/1000),'observed_max':list(temp.max())}
    adj_nflh = pd.DataFrame(data = check_limit)
    adj_nflh['gt'] = adj_nflh['max_NUTS2'] <= adj_nflh['observed_max']
    adj_nflh['NFLH_WH'] = list(NFLH_WH)
    count = 0
    adj_nflh['adj_nflh'] = list(NFLH_WH)
    nflh_WH_before.loc[region] =   list(NFLH_WH)
    while True in list(adj_nflh['gt']):
        count +=1
        print("Iteration", count)
        adj_nflh['nflh_change'] = 0
        adj_nflh['nflh_change'][adj_nflh['gt']== True] = 1
        adj_nflh['adj_nflh'] = adj_nflh['adj_nflh'] - adj_nflh['nflh_change']
        NFLH_WH2 = adj_nflh['adj_nflh']
        NFLH_WH2.index = NFLH_WH.index
        #FOR HOURLY DEMAND
        temp = NFLH_WH2*PUNIT_WH*NHH*RWH*S_HDD/1/30/1000 # daily
        temp['month']= range(1,13)
        temp = temp.append([temp]*23,ignore_index=True)
        temp = temp.sort_values(by='month')
        temp = temp.reset_index()
        temp = temp.drop(['index','month'],axis=1)
        for yr in range(0,temp.shape[1]): # convert from daily to hourly
            temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_wh    
        # check and see if limit has been violated    
        adj_nflh['observed_max'] = list(temp.max())
        adj_nflh['gt'] = adj_nflh['max_NUTS2'] <= adj_nflh['observed_max']
    nflh_WH_after.loc[region] =   list(adj_nflh['adj_nflh'])     
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
    
p_WH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_WHV7.csv')       
d_WH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_WHV7.csv') 


########################################
del p_WH
del d_WH
########
# sh - storage heater
# the calculation of storage heater will use Gils 2014 method using number of full load hours as a function of HDD and assume that there is no change in the efficiency of the appliance
columns = []
for i in range(2018,2051):
    columns.append(str(i))
d_SH = pd.DataFrame(index = index, columns = columns)   
p_SH = pd.DataFrame(index = index, columns = columns)   

s_sh =s_allelse.S_SH # hour share of daily demand
s_sh2 =s_sh # hour share of daily demand
s_sh = s_sh.append([s_sh]*11,ignore_index=True)


#creat df with nflh_wh
nflh_SH_before = pd.DataFrame(index = set(index['nutscode']), columns = columns) 
nflh_SH_after = pd.DataFrame(index = set(index['nutscode']), columns = columns)   

for row in range(1,len(set(index['nutscode']))+1):
    print(row)
    region = d_SH.index[(row-1)*288][0]
    NHH = nhh.loc[region]           # number of households
    YR_HDD = yr_hdd.loc[region]     # annual HDD
    RSH = rsh.loc[region]           # rate of ownership of SH
    NFLH_SH = (YR_HDD.iloc[0]/1000)*150+200  # number of full load hours of SH
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
# check and see if limit has been violated    
    check_limit = {'max_NUTS2':list(PUNIT_SH*NHH*RSH/1000),'observed_max':list(temp.max())}
    adj_nflh = pd.DataFrame(data = check_limit)
    adj_nflh['gt'] = adj_nflh['max_NUTS2'] < adj_nflh['observed_max']
    adj_nflh['NFLH_SH'] = list(NFLH_SH)
    count = 0
    adj_nflh['adj_nflh'] = list(NFLH_SH)
    nflh_SH_before.loc[region] =   list(NFLH_SH)
    while True in list(adj_nflh['gt']):
        count +=1
        print("Iteration", count)
        adj_nflh['nflh_change'] = 0
        adj_nflh['nflh_change'][adj_nflh['gt']== True] = 1
        adj_nflh['adj_nflh'] = adj_nflh['adj_nflh'] - adj_nflh['nflh_change']
        NFLH_SH2 = adj_nflh['adj_nflh']
        NFLH_SH2.index = NFLH_SH.index
        #FOR HOURLY DEMAND
        temp = NFLH_SH2*PUNIT_SH*NHH*RSH*S_HDD/1/30/1000 # daily
        temp['month']= range(1,13)
        temp = temp.append([temp]*23,ignore_index=True)
        temp = temp.sort_values(by='month')
        temp = temp.reset_index()
        temp = temp.drop(['index','month'],axis=1)
        for yr in range(0,temp.shape[1]): # convert from daily to hourly
            temp.iloc[0:288,yr] = temp.iloc[0:288,yr]*s_sh    
        # check and see if limit has been violated    
        adj_nflh['observed_max'] = list(temp.max())
        adj_nflh['gt'] = adj_nflh['max_NUTS2'] <= adj_nflh['observed_max']
    nflh_SH_after.loc[region] =   list(adj_nflh['adj_nflh'])             
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


p_SH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_SHV7.csv')       
d_SH.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_SHV7.csv')   


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

p_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_EVV7.csv')       
d_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_EVV7.csv')   

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

p_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_EVV6_fit55V2.csv')       
d_EV.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_EVV6_fit55V2.csv')   

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
d_RF.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_RFV5.csv')
p_RF.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_RFV5.csv')   
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

d_FR.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_FRV5.csv')
p_FR.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_FRV5.csv')
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




d_WM.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_WMV6.csv')
d_TD.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_TDV6.csv')
d_DW.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/d_DWV6.csv')
del d_WM
del d_TD
del d_DW

p_WM.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_WMV6.csv')
p_TD.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_TDV6.csv')
p_DW.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/p_DWV6.csv')
del p_WM
del p_TD
del p_DW
    