# This script makes urls for NOAA data for the mlbozone project

# Importing required modules

import pandas as pd

# Define username + filepath

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/mlbozone/'

# Read in the file

data = pd.read_csv(filepath + 'stadium_locations.csv')

# Declaring lists for data storage

lats = []
lons = []

# Defining a parsing function

def parser(x):
    
    hn = int(x[0:2])
    mn = int(x[3:5].replace('?','').replace('�','')) / 60
    
    cut  = x.find('N')
    x = x[cut+2:]
    
    if x[2] == '�':
        
        hw = int(x[0:2])
        mw = int(x[3:5].replace('?','').replace('�','')) / 60
        
    else:
        
        hw = int(x[0:3])
        mw = int(x[4:6].replace('?','').replace('�','')) / 60
    
    n = hn + mn
    w = hw + mw
    
    out = [n, w]
    
    return out

# Parsing lats and lons

for x in data.Coords:
    
    out = parser(x)
    lats.append(round(out[0],3))
    lons.append(round(out[1],3))
    
# Making urls

base = 'https://www.ncei.noaa.gov/access/search/data-search/global-summary-of-the-day?bbox='
urls = []

for i in range(len(lats)):
    
    url = base + str(lats[i]) + ',-' + str(lons[i]) + ',' + str(lats[i]-.1) + ',-' + str(lons[i]-.1)
    urls.append(url + '&startDate=2010-01-01T00:00:00&endDate=2019-12-31T23:59:59')
    
# Write urls to file for convenience

urls = pd.Series(urls, name = 'urls')
urls.to_csv(filepath + 'NOAA_urls.txt', index = False, header = False)

# Update stadium_locations

lats = pd.Series(lats, name = 'Lattitude')
lons = pd.Series(lons, name = 'Longitude')
data = pd.concat([data, lats, lons], axis = 1)
data.to_csv(filepath + 'stadium_locations.csv', index = False)

