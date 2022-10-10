# -*- coding: utf-8 -*-
"""
Created on Fri May  6 09:02:04 2022

@author: AK194059
"""
### BEGIN - global options ###
## Import packages
import pandas as pd ## necessary data analysis package
import numpy as np ## necessary data analysis package
import os

### Set options
os.chdir('I:/Projekte/OpenEntrance - WV0173/Durchführungsphase/WP6/CS1/OE_data_analysis/openEntrance/data/theoretical potential/P_inc/')

# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
### END - global options
df_HP = pd.read_csv('./P_inc_HP.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
df_TD = pd.read_csv('./P_inc_TD.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
df_DW = pd.read_csv('./P_inc_DW.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
df_WM = pd.read_csv('./P_inc_WM.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
df_SH = pd.read_csv('./P_inc_SH.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)
df_WH = pd.read_csv('./P_inc_WH.csv',sep=",",encoding = "ISO-8859-1", header=0, index_col=False)



df_HP.rename(columns = {'Unnames: 0':'nutscode'},inplace = True)
df_yr_sum = df_HP.groupby(['country'], as_index = False).sum()
df_yr_sum.to_csv(r'./country_summary/NUTS0_p_incHP.csv')     


df_TD.rename(columns = {'Unnames: 0':'nutscode'},inplace = True)
df_yr_sum = df_TD.groupby(['country'], as_index = False).sum()
df_yr_sum.to_csv(r'./country_summary/NUTS0_p_incTD.csv')     


df_DW.rename(columns = {'Unnames: 0':'nutscode'},inplace = True)
df_yr_sum = df_DW.groupby(['country'], as_index = False).sum()
df_yr_sum.to_csv(r'./country_summary/NUTS0_p_incDW.csv')     


df_WM.rename(columns = {'Unnames: 0':'nutscode'},inplace = True)
df_yr_sum = df_WM.groupby(['country'], as_index = False).sum()
df_yr_sum.to_csv(r'./country_summary/NUTS0_p_incWM.csv')     


df_SH.rename(columns = {'Unnames: 0':'nutscode'},inplace = True)
df_yr_sum = df_SH.groupby(['country'], as_index = False).sum()
df_yr_sum.to_csv(r'./country_summary/NUTS0_p_incSH.csv')     


df_WH.rename(columns = {'Unnames: 0':'nutscode'},inplace = True)
df_yr_sum = df_WH.groupby(['country'], as_index = False).sum()
df_yr_sum.to_csv(r'./country_summary/NUTS0_p_incWH.csv')     
