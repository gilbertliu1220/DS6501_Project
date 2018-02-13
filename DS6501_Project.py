# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:05:45 2018

@author: GilbertLiu
"""

import pandas as pd
import numpy as np
#define a variable for the directory of target excel file, read the file data 
#into a dataframe. 
file = 'C:/Users/GilbertLiu/Desktop/python/SOWC-Statistical-Tables-2017.xlsx'
x1=pd.ExcelFile(file)
# print out all the sheet names, and selecte the target sheet and skip rows 
# which are either empty or contain irrelevant words.
print(x1.sheet_names)
df1=x1.parse('Health',skiprows=[0,1,2,3,4,5,6])
#select the subset of rows for the columns of interest: 'Unnamed: 2' is for
#the use of basic water drinking service, and 'Unnamed: 5' is for the use of 
#basic sanitation services. 
ser1=df1.loc[0:201, 'Unnamed: 2']
ser2=df1.loc[0:201, 'Unnamed: 5']
# if any row from the selected column contains string "-", replace it with 0; 
# otherwise this row stays unchanged
ser1=ser1.replace("–",0)
ser2=ser2.replace("–",0)
# create an array to store average use of basic service, if either drinking 
#service or sanitation service in the same row for a country/area is equal 0
# the average value is equal to the other non-zero value; otherwise average 
# (basic drinking service+basic sanitation service).
newarray=np.zeros(len(ser1));
for i in range(0,len(ser1)):
    if (ser1[i]==0 or ser2[i]==0):
        newarray[i]=ser1[i]+ser2[i]
    else: 
        newarray[i]=0.5*(ser1[i]+ser2[i])
# convert the array into a series   
newser=pd.Series(newarray)
#read population infomration from another spreadsheet, and create a new series
# for it
df2=x1.parse('Demographic Indicators', skiprows=[0,1,2,3,4,5])
ser3=df2.loc[0:201, 'Unnamed: 2']
# creat a series for the list of countries and areas
ser4=df2.loc[0:201, 'Unnamed: 1']
# define a country to continent dictionary which is imported from a spreadsheet
file2 = 'C:/Users/GilbertLiu/Desktop/python/test.xlsx'
x1=pd.ExcelFile(file2)
df3=x1.parse(x1.sheet_names[0])
ser5=df3.loc[0:201,'Continent ']
# create a dataframe containg continent, population and percentage of the average use of 
# basic services for each country/area
dataframe_new=pd.concat([ser5,ser3,newser],axis=1)
dataframe_new.columns=['Continent','Population','Percentage of Average Basic Service Usage']
#assign the list of countries and areas as new index for datafram_new
dataframe_new.index=ser4
#define six sub-dataframes grouped by continents: AS stands for Asia, AF stands for Africa
# EU stands for Europe, NAM stands for North America, OC stands for Oceania and
# LC stands for Latin America and the Caribbean
conti_AS=dataframe_new[dataframe_new['Continent']=='AS']
conti_AF=dataframe_new[dataframe_new['Continent']=='AF']
conti_EU=dataframe_new[dataframe_new['Continent']=='EU']
conti_NAM=dataframe_new[dataframe_new['Continent']=='NAM']
conti_OC=dataframe_new[dataframe_new['Continent']=='OC']
conti_LC=dataframe_new[dataframe_new['Continent']=='LC']
# obtain weighted mean of average basic service usage (%) for each continent
MW_AS=(conti_AS['Population']*conti_AS['Percentage of Average Basic Service Usage']/conti_AS['Population'].sum()).sum()
MW_AF=(conti_AF['Population']*conti_AF['Percentage of Average Basic Service Usage']/conti_AF['Population'].sum()).sum()
MW_EU=(conti_EU['Population']*conti_EU['Percentage of Average Basic Service Usage']/conti_EU['Population'].sum()).sum()
MW_NAM=(conti_NAM['Population']*conti_NAM['Percentage of Average Basic Service Usage']/conti_NAM['Population'].sum()).sum()
MW_OC=(conti_OC['Population']*conti_OC['Percentage of Average Basic Service Usage']/conti_OC['Population'].sum()).sum()
MW_LC=(conti_LC['Population']*conti_LC['Percentage of Average Basic Service Usage']/conti_LC['Population'].sum()).sum()
# create an array to store weighted mean for these continents
arr1=[MW_AS,MW_AF,MW_EU,MW_NAM,MW_OC,MW_LC]
import matplotlib.pyplot as plt
objects = ('Asia','Africa','Europe','N.America','Oceania','L.America')
y_pos=np.arange(len(objects))
plt.bar(y_pos, arr1, align='center', alpha=1)
plt.xticks(y_pos, objects)
plt.ylabel('Percentage of Average Use of Basic Servics')
plt.title('Comparison of Average Use of Basic Services(%) Among Continents')