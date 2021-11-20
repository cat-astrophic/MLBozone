# This script creates flows data for the MLBozone project

# Importing required modules

import pandas as pd

# Defining the username + filepath

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/mlbozone/'

# Reading in the data

data = pd.read_csv(filepath + 'final_data_set.csv')

# Cleaning pollution data

data['O3'].values[data['O3'].values < 0] = 0
data['CO'].values[data['CO'].values < 0] = 0
data['NO2'].values[data['NO2'].values < 0] = 0
data['SO2'].values[data['SO2'].values < 0] = 0
data['PM2.5'].values[data['PM2.5'].values < 0] = 0
data['PM10'].values[data['PM10'].values < 0] = 0

# Creating flows data

coflows = []
so2flows = []
no2flows = []
o3flows = []
pm10flows = []
pm25flows = []

costats = []
so2stats = []
no2stats = []
o3stats = []
pm10stats = []
pm25stats = []

for c in list(data.City.unique()):
    
    print(c)
    
    fco = [None]
    fso2 = [None]
    fno2 = [None]
    fo3 = [None]
    fpm10 = [None]
    fpm25 = [None]
    
    costatx = [None]
    so2statx = [None]
    no2statx = [None]
    o3statx = [None]
    pm10statx = [None]
    pm25statx = [None]
    
    tmp = data[data.City == c].reset_index(drop = True)
    
    for i in range(1,len(tmp)):
        
        fco.append(tmp.CO[i] - tmp.CO[i-1])
        fso2.append(tmp.SO2[i] - tmp.SO2[i-1])
        fno2 .append(tmp.NO2[i] - tmp.NO2[i-1])
        fo3.append(tmp.O3[i] - tmp.O3[i-1])
        fpm10.append(tmp.PM10[i] - tmp.PM10[i-1])
        fpm25.append(tmp['PM2.5'][i] - tmp['PM2.5'][i-1])
        
        costatx.append(str(tmp.CO_Station[i]) + str(tmp.CO_Station[i-1]))
        so2statx.append(str(tmp.SO2_Station[i]) + str(tmp.SO2_Station[i-1]))
        no2statx.append(str(tmp.NO2_Station[i]) + str(tmp.NO2_Station[i-1]))
        o3statx.append(str(tmp.O3_Station[i]) + str(tmp.O3_Station[i-1]))
        pm10statx.append(str(tmp.PM10_Station[i]) + str(tmp.PM10_Station[i-1]))
        pm25statx.append(str(tmp['PM2.5_Station'][i]) + str(tmp['PM2.5_Station'][i-1]))
        
    coflows = coflows + fco
    so2flows = so2flows + fso2
    no2flows = no2flows + fno2
    o3flows = o3flows + fo3
    pm10flows = pm10flows + fpm10
    pm25flows = pm25flows + fpm25
    
    costats = costats + costatx
    so2stats = so2stats + so2statx
    no2stats = no2stats + no2statx
    o3stats = o3stats + o3statx
    pm10stats = pm10stats + pm10statx
    pm25stats = pm25stats + pm25statx
        
coflows = pd.Series(coflows, name = 'CO_Flow')
so2flows = pd.Series(so2flows, name = 'SO2_Flow')
no2flows = pd.Series(no2flows, name = 'NO2_Flow')
o3flows = pd.Series(o3flows, name = 'O3_Flow')
pm10flows = pd.Series(pm10flows, name = 'PM10_Flow')
pm25flows = pd.Series(pm25flows, name = 'PM2.5_Flow')

costats = pd.Series(costats, name = 'CO_Flow_SFE')
so2stats = pd.Series(so2stats, name = 'SO2_Flow_SFE')
no2stats = pd.Series(no2stats, name = 'NO2_Flow_SFE')
o3stats = pd.Series(o3stats, name = 'O3_Flow_SFE')
pm10stats = pd.Series(pm10stats, name = 'PM10_Flow_SFE')
pm25stats = pd.Series(pm25stats, name = 'PM2.5_Flow_SFE')

data = pd.concat([data, coflows, so2flows, no2flows, o3flows, pm10flows, pm25flows,
                  costats, so2stats, no2stats, o3stats, pm10stats, pm25stats], axis = 1)
data.to_csv(filepath + 'maybe_final_data_set.csv', index = False)

