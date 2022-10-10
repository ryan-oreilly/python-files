# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import country_converter as coco
pd.read_csv()

df = pd.read_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/Full_potential.V9.country.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)#
set(df.variable)
tmp = ['Demand Response|Maximum Reduction|Load Shifting|Electricity|Residential|Electric Vehicle_55','Demand Response|Maximum Dispatch|Load Shifting|Electricity|Residential|Electric Vehicle_55']

df2 = df[df.variable != tmp[0]]
df2 = df2[df2.variable != tmp[1]]

iso2 = set(df2.region)
name = coco.convert(iso2, to ='name')
temp = {'region':list(iso2), 'name':name}

dftemp = pd.DataFrame(temp)
dftemp.name[dftemp.region=='UK']= 'United Kingdom'
dftemp.name[dftemp.region=='EL']= 'Greece'
dftemp.name[dftemp.region=='NL']= 'The Netherlands'

df3 = pd.merge(df2,dftemp)
df3.head()
set(df3.name)
df3 = df3.drop('region',axis =1)
df3.rename(columns ={'name':'region'}, inplace = True)
set(df3.region)
df3.write_csv('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/Full_potential.V10.country.csv')


df3.to_csv(r'I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/Full_potential.V10.country.csv')   
df3.to_excel('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/Full_potential.V10.country.xlsx', index=False)
