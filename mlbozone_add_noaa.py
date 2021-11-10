# This script parses noaa data for the mlbozone project

# Importing required modules

import pandas as pd
import glob
from geopy.distance import geodesic

# Defining username + filpeath

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/mlbozone/'

# Create a list of all files in the noaa_data subfolder

files = []

for file in glob.glob(filepath + 'noaa_data/*'):
    
    files.append(file)
    
# Initializing a dataframe

df = pd.DataFrame()

# Reading in the data and creating a single df

for file in files:
    
    print('Reading in raw data file ' + str(files.index(file)+1) + ' of ' + str(len(files)) + '.......')
    tmp = pd.read_csv(file)
    df = pd.concat([df, tmp], axis = 0)
    
# Reading in the baseball + stadium location data

data = pd.read_csv(filepath + 'mlb_data.csv')
slocs = pd.read_csv(filepath + 'stadium_locations.csv')

# Adding lats and lons to data

lats = []
lons = []

for i in range(len(data)):
    
    print('Getting coordinates for stadium ' + str(i+1) + ' of ' + str(len(data)) + '.......')
    s = data.Stadium[i]
    tmp = slocs[slocs.Stadium == s].reset_index(drop = True)
    lats.append(tmp.Lattitude[0])
    lons.append(tmp.Longitude[0])
    
lats = pd.Series(lats, name = 'Lattitude')
lons = pd.Series(lons, name = 'Longitude')
data = pd.concat([data, lats, lons], axis = 1)

# Create a small df of stations and their coordinates

codf = df[df.DATE == '2011-01-01'].reset_index(drop = True)

# Use geopy.distances.geodesic to find nearest stations for each stadium

stations = []
ll = list(data.Stadium.unique())

for s in ll:
    
    distances = []
    tmp = data[data.Stadium == s].reset_index(drop = True)
    coords1 = [tmp.Lattitude[0], -1*tmp.Longitude[0]]
    
    for i in range(len(codf)):
        
        coords2 = [codf.LATITUDE[i], codf.LONGITUDE[i]]
        distances.append(geodesic(coords1, coords2).mi)
        
    idx = distances.index(min(distances))
    stations.append(codf.STATION[idx])

# Adding NOAA stations to df and creating a full stations reference list

stats = []

for i in range(len(data)):
    
    stad = data.Stadium[i]
    idx = ll.index(stad)
    stats.append(stations[idx])

data = pd.concat([data, pd.Series(stats, name = 'NOAA_Station')], axis = 1)

# Creating main df

dates = []
lens = [31,28,31,30,31,30,31,31,30,31,30,31]

for i in range(2010,2020):
    
    for j in range(1,13):
        
        if j == 2 and i%4 == 0:
            
            for k in range(lens[j-1]+1):
                
                if k+1 > 9:
                    
                    x = str(k+1)
                    
                else:
                    
                    x = '0' + str(k+1)
                    
                dates.append(str(i) + '02' + x)
                
        else:
            
            if j > 9:
                
                y = str(j)
                
            else:
                
                y = '0' + str(j)
            
            for k in range(lens[j-1]):
                
                if k+1 > 9:
                    
                    x = str(k+1)
                    
                else:
                    
                    x = '0' + str(k+1)
                    
                dates.append(str(i) + y + x)
                
dates = dates*30

teams = []

for l in ll[:30]:
    
    tmpdf = data[data.Stadium == l].reset_index(drop = True)
    teams.append(tmpdf.Home_Team[0])

cities = []
latts = []
longs = []
stads = []

for t in teams:
    
    if t not in ['MIA', 'ATL']:
        
        tmpdf = data[data.Home_Team == t].reset_index(drop = True)
        tmp1 = [tmpdf.Home_Team[0]]*3652
        tmp2 = [tmpdf.Lattitude[0]]*3652
        tmp3 = [tmpdf.Longitude[0]]*3652
        tmp4 = [tmpdf.Stadium[0]]*3652
        cities = cities + tmp1
        latts = latts + tmp2
        longs = longs + tmp3
        stads = stads + tmp4
        
    elif t == 'MIA':
        
        tmpdf = data[data.Home_Team == t].reset_index(drop = True)
        tmp1 = [tmpdf.Home_Team[0]]*3652
        tmp2 = [tmpdf.Lattitude[0]]*730
        tmp22 = [tmpdf.Lattitude[len(tmpdf)-1]]*(3652-730)
        tmp3 = [tmpdf.Longitude[0]]*730
        tmp32 = [tmpdf.Longitude[len(tmpdf)-1]]*(3652-730)
        tmp4 = [tmpdf.Stadium[0]]*730
        tmp42 = [tmpdf.Stadium[len(tmpdf)-1]]*(3652-730)
        cities = cities + tmp1
        latts = latts + tmp2 + tmp22
        longs = longs + tmp3 + tmp32
        stads = stads + tmp4 + tmp42
        
    else:
        
        tmpdf = data[data.Home_Team == t].reset_index(drop = True)
        tmp1 = [tmpdf.Home_Team[0]]*3652
        tmp2 = [tmpdf.Lattitude[0]]*(7*365+2)
        tmp22 = [tmpdf.Lattitude[len(tmpdf)-1]]*(3652-(7*365+2))
        tmp3 = [tmpdf.Longitude[0]]*(7*365+2)
        tmp32 = [tmpdf.Longitude[len(tmpdf)-1]]*(3652-(7*365+2))
        tmp4 = [tmpdf.Stadium[0]]*(7*365+2)
        tmp42 = ['ATL03']*(3652-(7*365+2))
        cities = cities + tmp1
        latts = latts + tmp2 + tmp22
        longs = longs + tmp3 + tmp32
        stads = stads + tmp4 + tmp42
        
dow = [5] # M-W == 1-5; S-S == 6-0

for i in range(1,len(dates)):
    
    dow.append((5+i)%7)
    
wend = [int(x%6 == 0) for x in dow]
wkday = [int(x%6 != 0) for x in dow]

temp = []
wind = []
prcp = []

for i in range(len(dates)):
    
    d = dates[i]
    dx = str(d[:4]) + '-' + str(d[4:6]) + '-' + str(d[6:])
    tmpx = data[data.Home_Team == cities[i]].reset_index(drop = True)
    sx = tmpx.NOAA_Station[0]
    tmp = df[df.DATE == dx]
    tmp = tmp[tmp.STATION == sx].reset_index(drop = True)
    
    try:
        
        temp.append(tmp.TEMP[0])
        wind.append(tmp.WDSP[0])
        prcp.append(tmp.PRCP[0])
        
    except:
        
        temp.append(None)
        wind.append(None)
        prcp.append(None)
        
attend = []
home = []

for i in range(len(dates)):
    
    d = int(dates[i])
    tmp = data[data.Date == d]
    tmp = tmp[tmp.Home_Team == cities[i]].reset_index(drop = True)
    
    try:
        
        attend.append(tmp.Attendance[0])
        home.append(1)
        
    except:
        
        attend.append(0)
        home.append(0)
        
away = []

for i in range(len(dates)):
    
    d = int(dates[i])
    tmp = data[data.Date == d]
    tmp = tmp[tmp.Away_Team == cities[i]].reset_index(drop = True)
    
    if len(tmp) > 0:
        
        away.append(1)
        
    else:
        
        away.append(0)
        
dhd = []
time = []
typ = []

for i in range(len(dates)):
    
    if home[i] > 0:
        
        d = int(dates[i])
        tmp = data[data.Home_Team == cities[i]]
        tmp = tmp[tmp.Date == d].reset_index(drop = True)
        
    elif away[i] > 0:
        
        d = int(dates[i])
        tmp = data[data.Away_Team == cities[i]]
        tmp = tmp[tmp.Date == d].reset_index(drop = True)
        
    else:
        
        tmp = data[data.Date == 4]
        
    try:
        
        dhd.append(int(tmp.Doubleheader[0] != 0))
        time.append(tmp.Time[0])
        typ.append(tmp.Type[0])
        
    except:
        
        dhd.append(0)
        time.append(None)
        typ.append(None)
        
# Assembling dataframe and writing to file

dates = pd.Series(dates, name = 'Date')
cities = pd.Series(cities, name = 'City')
latts = pd.Series(latts, name = 'Latitude')
longs = pd.Series(longs, name = 'Longitude')
stads = pd.Series(stads, name = 'Stadium')
dow = pd.Series(dow, name = 'Day_of_the_Week')
wend = pd.Series(wend, name = 'Weekend')
wkday = pd.Series(wkday, name = 'Weekday')
temp = pd.Series(temp, name = 'Temperature')
wind = pd.Series(wind, name = 'Wind_Speed')
prcp = pd.Series(prcp, name = 'Precipitation')
attend = pd.Series(attend, name = 'Attendance')
home = pd.Series(home, name = 'Home')
away = pd.Series(away, name = 'Away')
dhd = pd.Series(dhd, name = 'Doubleheader')
time = pd.Series(time, name = 'Time')
typ = pd.Series(typ, name = 'Type')
new_df = pd.concat([dates, cities, latts, longs, stads, dow, wend, wkday,
                    temp, wind, prcp, attend, home, away, dhd, time, typ], axis = 1)
new_df.to_csv(filepath + 'mlb_data_noaa.csv', index = False)

