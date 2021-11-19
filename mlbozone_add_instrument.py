# This script creates an instrument for the MLBozone project

# Importing required modules

import pandas as pd
import numpy as np
import os

# Define username + filepath

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/MLBozone/raw_data2/'

# Reading in the data

data = pd.read_csv(filepath[:-10] + 'maybe_final_data_set.csv')
files = os.listdir(filepath)
df = pd.DataFrame()

for f in files:
    
    tmp = pd.read_csv(filepath + f, header = None)
    df = pd.concat([df, tmp], axis = 0)
    
# Sort by date

df = df.sort_values([0])

# Remove games before 2009

df = df[df[0] > 20090000].reset_index(drop = True)

# Convert FLO to MIA so same team is identified

df[[3,6]] = df[[3,6]].replace(['FLO'], ['MIA'])

# Create a list of teams

teams = list(df[3].unique())

# Main loop creating the instrument

iv10 = []
iv20 = []
iv50 = []
iv100 = []
dates10 = []
dates20 = []
dates50 = []
dates100 = []
ts10 = []
ts20 = []
ts50 = []
ts100 = []

for t in teams:
    
    print(t)
    
    tmpa = df[df[3] == t]
    tmph = df[df[6] == t]
    tmp = pd.concat([tmpa, tmph], axis = 0)
    tmp = tmp.sort_values([0]).reset_index(drop = True)
    a = [int(tmp[3][x] == t) for x in range(len(tmp))]
    h = [int(tmp[6][x] == t) for x in range(len(tmp))]
    aw = [1 if tmp[9][i] > tmp[10][i] else 0 for i in range(len(tmp))]
    hw = [1 if tmp[10][i] > tmp[9][i] else 0 for i in range(len(tmp))]
    w = [a[i]*aw[i] + h[i]*hw[i] for i in range(len(a))]
    
    iv10x = [np.mean(w[x-10:x]) for x in range(10,len(w))]
    iv20x = [np.mean(w[x-20:x]) for x in range(20,len(w))]
    iv50x = [np.mean(w[x-50:x]) for x in range(50,len(w))]
    iv100x = [np.mean(w[x-100:x]) for x in range(100,len(w))]
    
    dates10x = [tmp[0][x] for x in range(10,len(tmp))]
    dates20x = [tmp[0][x] for x in range(20,len(tmp))]
    dates50x = [tmp[0][x] for x in range(50,len(tmp))]
    dates100x = [tmp[0][x] for x in range(100,len(tmp))]
    
    ts10x = [t]*len(dates10x)
    ts20x = [t]*len(dates20x)
    ts50x = [t]*len(dates50x)
    ts100x = [t]*len(dates100x)
    
    iv10 = iv10 + iv10x
    iv20 = iv20 + iv20x
    iv50 = iv50 + iv50x
    iv100 = iv100 + iv100x
    dates10 = dates10 + dates10x
    dates20 = dates20 + dates20x
    dates50 = dates50 + dates50x
    dates100 = dates100 + dates100x
    ts10 = ts10 + ts10x
    ts20 = ts20 + ts20x
    ts50 = ts50 + ts50x
    ts100 = ts100 + ts100x
    
# Create some dataframes

iv10 = pd.Series(iv10, name = 'IV10')
iv20 = pd.Series(iv20, name = 'IV20')
iv50 = pd.Series(iv50, name = 'IV50')
iv100 = pd.Series(iv100, name = 'IV100')
dates10 = pd.Series(dates10, name = 'Date')
dates20 = pd.Series(dates20, name = 'Date')
dates50 = pd.Series(dates50, name = 'Date')
dates100 = pd.Series(dates100, name = 'Date')
ts10 = pd.Series(ts10, name = 'Team')
ts20 = pd.Series(ts20, name = 'Team')
ts50 = pd.Series(ts50, name = 'Team')
ts100 = pd.Series(ts100, name = 'Team')

newdf10 = pd.concat([iv10,dates10,ts10], axis = 1)
newdf20 = pd.concat([iv20,dates20,ts20], axis = 1)
newdf50 = pd.concat([iv50,dates50,ts50], axis = 1)
newdf100 = pd.concat([iv100,dates100,ts100], axis = 1)

x10 = [str(dates10[x]) + str(ts10[x]) for x in range(len(dates10))]
x20 = [str(dates20[x]) + str(ts20[x]) for x in range(len(dates20))]
x50 = [str(dates50[x]) + str(ts50[x]) for x in range(len(dates50))]
x100 = [str(dates100[x]) + str(ts100[x]) for x in range(len(dates100))]

x10 = pd.Series(x10, name = 'x')
x20 = pd.Series(x20, name = 'x')
x50 = pd.Series(x50, name = 'x')
x100 = pd.Series(x100, name = 'x')

newdf10 = pd.concat([newdf10, x10], axis = 1).reset_index(drop = True)
newdf20 = pd.concat([newdf20, x20], axis = 1).reset_index(drop = True)
newdf50 = pd.concat([newdf50, x50], axis = 1).reset_index(drop = True)
newdf100 = pd.concat([newdf100, x100], axis = 1).reset_index(drop = True)

# Create final instruments data

i10 = []
i20 = []
i50 = []
i100 = []
obs = [str(data.Date[i]) + str(data.City[i]) for i in range(len(data))]
prev_t = ''

for o in obs:
    
    print(o)
    t = o[-3:]
    
    if t == prev_t:
        
        tmp10 = newdf10[newdf10.x == o].reset_index(drop = True)
        tmp20 = newdf20[newdf20.x == o].reset_index(drop = True)
        tmp50 = newdf50[newdf50.x == o].reset_index(drop = True)
        tmp100 = newdf100[newdf100.x == o].reset_index(drop = True)
        
        try:
            
            i10.append(tmp10.IV10[0])
            i20.append(tmp20.IV20[0])
            i50.append(tmp50.IV50[0])
            i100.append(tmp100.IV100[0])
            
        except:
            
            i10.append(None)
            i20.append(None)
            i50.append(None)
            i100.append(None)
            
    else:
        
        tmp10 = newdf10[newdf10.Team == t]
        tmp10 = tmp10[tmp10.Date < 20100000].reset_index(drop = True)
        i10.append(tmp10.IV10[len(tmp10)-1])
        
        tmp20 = newdf20[newdf20.Team == t]
        tmp20 = tmp20[tmp20.Date < 20100000].reset_index(drop = True)
        i20.append(tmp20.IV20[len(tmp20)-1])
        
        tmp50 = newdf50[newdf50.Team == t]
        tmp50 = tmp50[tmp50.Date < 20100000].reset_index(drop = True)
        i50.append(tmp50.IV50[len(tmp50)-1])
        
        tmp100 = newdf100[newdf100.Team == t]
        tmp100 = tmp100[tmp100.Date < 20100000].reset_index(drop = True)
        i100.append(tmp100.IV100[len(tmp100)-1])
        
# Removing Nones

for i in range(len(i10)):
    
    if i10[i] == None:
        
        i10[i] = i10[i-1]
        
for i in range(len(i20)):
    
    if i20[i] == None:
        
        i20[i] = i20[i-1]
        
for i in range(len(i50)):
    
    if i50[i] == None:
        
        i50[i] = i50[i-1]
        
for i in range(len(i100)):
    
    if i100[i] == None:
        
        i100[i] = i100[i-1]
        
# Add instruments to dataframe

i10 = pd.Series(i10, name = 'IV10')
i20 = pd.Series(i20, name = 'IV20')
i50 = pd.Series(i50, name = 'IV50')
i100 = pd.Series(i100, name = 'IV100')
data = pd.concat([data, i10, i20, i50, i100], axis = 1)

# Write data to file

data.to_csv(filepath[:-10] + 'mlbozone_data.csv', index = False)

# This works as an instrument because better team performance can
# bring people to the stadium who otherwise wouldn't have been out

