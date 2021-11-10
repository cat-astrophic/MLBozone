# This script parses epa data for the mlbozone project

# Importing required modules

import pandas as pd
import zipfile
import glob
from geopy.distance import geodesic

# Defining username + filpeath

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/mlbozone/'

# Create a list of all files in the noaa_data subfolder

files = []

for file in glob.glob(filepath + 'pollution_data/*'):
    
    files.append(file)
    
# Extract csv files from zip

for file in files:
    
    with zipfile.ZipFile(file, 'r') as zip_ref:
        
        zip_ref.extractall(filepath + 'pollution_data/extracted_pollution_data/')
        
# Create a list of all files in the noaa_data subfolder

files = []

for file in glob.glob(filepath + 'pollution_data/extracted_pollution_data/*'):
    
    files.append(file)
    
# Initializing a dataframe

df = pd.DataFrame()

# Reading in the data and creating a single df

for file in files:
    
    print('Reading in raw data file ' + str(files.index(file)+1) + ' of ' + str(len(files)) + '.......')
    tmp = pd.read_csv(file)
    df = pd.concat([df, tmp], axis = 0)

# Creating pollutant specific dfs

co = df[df['Parameter Code'] == 42101]
so2 = df[df['Parameter Code'] == 42401]
no2 = df[df['Parameter Code'] == 42602]
o3 = df[df['Parameter Code'] == 44201]
pm10 = df[df['Parameter Code'] == 81102]
pm25 = df[df['Parameter Code'] == 88101]

# Save RAM

del(df)

# Read in the mlb data

data = pd.read_csv(filepath + 'mlb_data_noaa.csv')

# Declaring some lists for data storage

dco = []
dso2 = []
dno2 = []
do3 = []
dpm10 = []
dpm25 = []

aqico = []
aqiso2 = []
aqino2 = []
aqio3 = []
aqipm10 = []
aqipm25 = []

sco = []
sso2 = []
sno2 = []
so3 = []
spm10 = []
spm25 = []

disco = []
disso2 = []
disno2 = []
diso3 = []
dispm10 = []
dispm25 = []

# Main loop

for i in range(len(data)):
    
    # Visualize progress
    
    print('Collecting pollution data for entry ' + str(1+i) + ' of 109560.......')
    
    # Subset the pollution dataframes    
    
    dt = str(data.Date[i])
    d = dt[:4] + '-' + dt[4:6] + '-' + dt[6:8]
    cotmp = co[co['Date Local'] == d].reset_index(drop = True)
    so2tmp = so2[so2['Date Local'] == d].reset_index(drop = True)
    no2tmp = no2[no2['Date Local'] == d].reset_index(drop = True)
    o3tmp = o3[o3['Date Local'] == d].reset_index(drop = True)
    pm10tmp = pm10[pm10['Date Local'] == d].reset_index(drop = True)
    pm25tmp = pm25[pm25['Date Local'] == d].reset_index(drop = True)
    
    # Compute distances to all sites
    
    codis = [geodesic([data.Latitude[i],-1*data.Longitude[i]],[cotmp.Latitude[j],cotmp.Longitude[j]]).mi for j in range(len(cotmp))]
    so2dis = [geodesic([data.Latitude[i],-1*data.Longitude[i]],[so2tmp.Latitude[j],so2tmp.Longitude[j]]).mi for j in range(len(so2tmp))]
    no2dis = [geodesic([data.Latitude[i],-1*data.Longitude[i]],[no2tmp.Latitude[j],no2tmp.Longitude[j]]).mi for j in range(len(no2tmp))]
    o3dis = [geodesic([data.Latitude[i],-1*data.Longitude[i]],[o3tmp.Latitude[j],o3tmp.Longitude[j]]).mi for j in range(len(o3tmp))]
    pm10dis = [geodesic([data.Latitude[i],-1*data.Longitude[i]],[pm10tmp.Latitude[j],pm10tmp.Longitude[j]]).mi for j in range(len(pm10tmp))]
    pm25dis = [geodesic([data.Latitude[i],-1*data.Longitude[i]],[pm25tmp.Latitude[j],pm25tmp.Longitude[j]]).mi for j in range(len(pm25tmp))]
    
    # Find nearest sites
    
    idxco = codis.index(min(codis))
    idxso2 = so2dis.index(min(so2dis))
    idxno2 = no2dis.index(min(no2dis))
    idxo3 = o3dis.index(min(o3dis))
    idxpm10 = pm10dis.index(min(pm10dis))
    idxpm25 = pm25dis.index(min(pm25dis))
    
    # Recording pollution levels and AQI values at nearest site
    
    dco.append(cotmp['Arithmetic Mean'][idxco])
    dso2.append(so2tmp['Arithmetic Mean'][idxso2])
    dno2.append(no2tmp['Arithmetic Mean'][idxno2])
    do3.append(o3tmp['Arithmetic Mean'][idxo3])
    dpm10.append(pm10tmp['Arithmetic Mean'][idxpm10])
    dpm25.append(pm25tmp['Arithmetic Mean'][idxpm25])
    
    aqico.append(cotmp['AQI'][idxco])
    aqiso2.append(so2tmp['AQI'][idxso2])
    aqino2.append(no2tmp['AQI'][idxno2])
    aqio3.append(o3tmp['AQI'][idxo3])
    aqipm10.append(pm10tmp['AQI'][idxpm10])
    aqipm25.append(pm25tmp['AQI'][idxpm25])
    
    # Recording sites
    
    sco.append(cotmp['Site Num'][idxco])
    sso2.append(so2tmp['Site Num'][idxso2])
    sno2.append(no2tmp['Site Num'][idxno2])
    so3.append(o3tmp['Site Num'][idxo3])
    spm10.append(pm10tmp['Site Num'][idxpm10])
    spm25.append(pm25tmp['Site Num'][idxpm25])
    
    # Recording distances
    
    disco.append(codis[idxco])
    disso2.append(so2dis[idxso2])
    disno2.append(no2dis[idxno2])
    diso3.append(o3dis[idxo3])
    dispm10.append(pm10dis[idxpm10])
    dispm25.append(pm25dis[idxpm25])
    
# Making the final dataframe and writing to file

dco = pd.Series(dco, name = 'CO')
dso2 = pd.Series(dso2, name = 'SO2')
dno2 = pd.Series(dno2, name = 'NO2')
do3 = pd.Series(do3, name = 'O3')
dpm10 = pd.Series(dpm10, name = 'PM10')
dpm25 = pd.Series(dpm25, name = 'PM2.5')

aqico = pd.Series(aqico, name = 'CO_AQI')
aqiso2 = pd.Series(aqiso2, name = 'SO2_AQI')
aqino2 = pd.Series(aqino2, name = 'NO2_AQI')
aqio3 = pd.Series(aqio3, name = 'O3_AQI')
aqipm10 = pd.Series(aqipm10, name = 'PM10_AQI')
aqipm25 = pd.Series(aqipm25, name = 'PM2.5_AQI')

sco = pd.Series(sco, name = 'CO_Station')
sso2 = pd.Series(sso2, name = 'SO2_Station')
sno2 = pd.Series(sno2, name = 'NO2_Station')
so3 = pd.Series(so3, name = 'O3_Station')
spm10 = pd.Series(spm10, name = 'PM10_Station')
spm25 = pd.Series(spm25, name = 'PM2.5_Station')

disco = pd.Series(disco, name = 'CO_Distance')
disso2 = pd.Series(disso2, name = 'SO2_Distance')
disno2 = pd.Series(disno2, name = 'NO2_Distance')
diso3 = pd.Series(diso3, name = 'O3_Distance')
dispm10 = pd.Series(dispm10, name = 'PM10_Distance')
dispm25 = pd.Series(dispm25, name = 'PM2.5_Distance')

data = pd.concat([data, dco, dso2, dno2, do3, dpm10, dpm25, aqico, aqiso2, aqino2,
                  aqio3, aqipm10, aqipm25, sco, sso2, sno2, so3, spm10, spm25,
                  disco, disso2, disno2, diso3, dispm10, dispm25], axis = 1)

data.to_csv(filepath + 'final_data_set.csv', index = False)

