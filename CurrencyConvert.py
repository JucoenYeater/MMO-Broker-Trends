# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 01:53:16 2022

@author: jucoe
"""

import re, csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd



def drop_outliers_IQR(df):
   q1=df.quantile(0.10)
   q3=df.quantile(0.90)
   IQR=q3-q1
   outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
   not_outliers = df[~((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
   outliers_dropped = not_outliers.dropna().reset_index()
   return outliers_dropped


mats = ['tin cluster','tuber strand','carbonite cluster','belladonna root','feyiron cluster',
        'tussah root','fulginate cluster','ashen root','indium cluster','succulent root',
        'severed sandalwood']

mats_rare = ['ireheart radish','lambent material','scaled leather pelt','rough pearl',
             'vanadium cluster','cobalt cluster']

item_hv = ['krono']

search_list = item_hv + mats_rare + mats





# Currency
csl = [] # Currency String List
css = [] # Currency String Split - List of List of Elements
cssf = [] # css but with '' removed
cssl = []

# Currency Conversion Ratios
ccr = [100, 1, 0.01, 0.0001]


# File path to master_price.txt
mp_path = r"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\master_price.txt"

# File path to master_price_list.txt
mp_path_sp = r"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\master_price_sp.txt"


# Dump master_price to list of strings
with open(mp_path) as file:
    lines = file.readlines()
    file.close()
# Dump master_price_sp to list of strings   
with open(mp_path_sp) as file:
    lines_sp = file.readlines()
    file.close()

# Split strings to get a list of lists split at the comma
ll = [v.rstrip().split(", ") for v in lines]
# Split strings to get a list of lists split at the comma
ll_sp = [v.rstrip().split(", ") for v in lines_sp]

# Append the sp dataset to the desktop, may be more effecient to go the other way
# since the sp will have more data
for x in range(len(ll_sp)):   
    ll.append(ll_sp[x])
    
# Need to use increment since there is some bad data that is dropped
#i = 0

# Want to pull the price string out of each embedded list
for x in range(len(ll)):
    # Price can only come in a specific format, so the else drops most bad data
    if re.match(r"^(?:\d+p)?(?:\d\d?g)?(?:\d\d?s)?(?:\d\d?c)?$",ll[x][2]):
        
        # Grab currency strings to be placed in respective elements in the list
        css = list(re.findall(r"^(?:(\d+)p)?(?:(\d\d?)g)?(?:(\d\d?)s)?(?:(\d\d?)c)?$",ll[x][2])[0])
        
        # Need to reset pgl each loop
        pgl = []
        
        # Converts currency for each sale per loop for the currency types to gold
        for y in range(len(css)):
            if css[y] == '':
                css[y] = 0
            else:
                css[y] = int(css[y])
                pgl.append(css[y] * ccr[y])
        
        # Sum the gold conversions to get the total item amount in gold
        pg = round(sum(pgl),2) # Total Price of item in gold

        # Append gold price to list
        cssl.append(pg)
        
        # Replace original price string with converted gold float data types
        ll[x][2] = pg
        
        # Increment so the correct list is grabbed
        # i += 1
        
    # Bad data, currently just dropped from dataset
    else:
        continue

# Define empty lists to append data to
mpg = []
a = []
b = []

# The amount of bad data points to be summed in next for loop
z = 0

# Keep only item listings where price was converted to int/float
for x in range(len(ll)):
    if type(ll[x][2]) == str or (ll[x][2] >= 5000 and (ll[x][1] != 'krono' and ll[x][1] != 'ireheart radish')) or (ll[x][2] <= 3000 and ll[x][1] == 'krono'):
        z += 1
    else:
        mpg.append(ll[x])
    
# Convert datetime string back to datetime date type
for x in range(len(mpg)):
    #mpg[x][3] = datetime.strptime(mpg[x][3], '%Y-%m-%d %H:%M:%S')
    mpg[x][3] = pd.to_datetime(mpg[x][3])
    
# Write item listings to text file
with open(r"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\master_price_master_gold2.txt",'w',newline="") as file:
    csv.writer(file,delimiter=" ").writerows(mpg)

# Create empty lists to be appended to
summary_with_outliers = []
summary_without_outliers = []
dfl = []
xfl = []

# Dataframe column names
column1 = 'Item'
column2 = 'Date'
column3 = 'PriceGold'

# Pull out the datetime and price for each listing
for y in range(len(search_list)):
    for x in range(len(mpg)):
        if mpg[x][1] == search_list[y]:
            a.append(mpg[x][3])
            b.append(mpg[x][2])
    
    ab = []
    for z in range(len(a)):
        ab.append([search_list[y],a[z],b[z]])
    # Plot each item on its own graph
    plt.scatter(a,b)
    plt.xlabel(search_list[y])
    plt.ylim(ymin=0)
    plt.show()
    # plt.pause(2)
    # Reset plot x=a and y=b to append new item price points
    a = []
    b = []
    #a.extend(b)
    # for z in range(len(a)):
    #     ab.append(a[z])
    
    # Each item's respective dataframe
    df = pd.DataFrame(ab)
    
    # Rename columns
    df = df.rename({0: column1, 1: column2, 2: column3}, axis=1)
    
    # Append each item's respective dataframe so we don't lose the data on the loop
    dfl.append(df)
    
    # Lower and upper outlier threshold
    qa = df[column3].quantile(0.025)
    qb = df[column3].quantile(0.975)
    
    # Remove outliers
    xf = df[(df[column3] >= qa) & (df[column3] <= qb)]
    
    # Append each item's respective outliers removed dataframe so we don't lose the data on the loop
    xfl.append(xf)
    
    summary_with_outliers.append(dfl[y].describe())
    summary_without_outliers.append(xfl[y].describe())
    
    # Plot each graph
    plt.scatter(xf[column2],xf[column3])
    plt.xlabel(f"{search_list[y]} | Outliers Removed")
    plt.ylim(ymin=0,ymax=max(xf[column3])+(0.5*(sum(xf[column3])/len(xf[column3]))))
    plt.show()
    # plt.pause(120)
    
    
    # plt.plot(df2[y][0],df2[y][1])
    # plt.xlabel(search_list[y])
    # plt.show()

    # for m in range(len(df[y])):
    #     if df[y].iloc[m,0] == df2[y][m]:
    #         del df[y][2]
    #         df[y][m].append(df2[y][0])
    #         df3 = df[y][m]
    #     else:
    #         continue
    
    # plt.scatter(df[y].iloc[:,1],df2[y].iloc[:,1])
    

    # print(df.describe(a,b))