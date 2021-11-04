# This script parses MLB data from retrosheet and creates a dataframe

# Importing required modules

import pandas as pd
import glob

# Defining username + directory

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/mlbozone/'

# Create a list of all files in the raw_data subfolder

files = []

for file in glob.glob(filepath + 'raw_data/*'):
    
    files.append(file)

# Declaring some data storage

attendance = []
dates = []
dblh = []
dow = []
stadia = []
dn = []
scorea = []
scoreh = []
team = [] # home team
gtype = [] # game type

# Main loop

for file in files:
    
    print('Extracting data from ' + file + '.......')
    
    data = pd.read_csv(file, header = None)
    attendance = attendance + data[[17]][17].to_list()
    dates = dates + data[[0]][0].to_list()
    dblh = dblh + data[[1]][1].to_list()
    dow = dow + data[[2]][2].to_list()
    stadia = stadia + data[[16]][16].to_list()
    dn = dn + data[[12]][12].to_list()
    team = team + data[[6]][6].to_list()
    gt = file[-8:-4]
    
    try:
        
        gt = int(gt)
        gt = 'REGS'
    
    except:
        
        pass
    
    
    gtype = gtype + [gt]*len(data)
    
    if file[-8:] == 'GLAS.TXT':
        
        scorea = scorea + [None]*len(data)
        scoreh = scoreh + [None]*len(data)
        
    else:
        
        scorea = scorea + data[[9]][9].to_list()
        scoreh = scoreh + data[[10]][10].to_list()
    
# Compute home winner in non all-star games

winner = [int(scoreh[i] - scorea[i] > 0) if scoreh[i] != None and scorea[i] != None else None for i in range(len(scoreh))]

# Updating FLO to MIA for consistency

team = ['MIA' if t == 'FLO' else t for t in team]

# Creating a dataframe

attendance = pd.Series(attendance, name = 'Attendance')
dates = pd.Series(dates, name = 'Date')
dblh = pd.Series(dblh, name = 'Doubleheader')
dow = pd.Series(dow, name = 'Day')
stadia = pd.Series(stadia, name = 'Stadium')
dn = pd.Series(dn, name = 'Time')
scorea = pd.Series(scorea, name = 'Score_Away')
scoreh = pd.Series(scoreh, name = 'Score_Home')
winner = pd.Series(winner, name = 'Winner')
team = pd.Series(team, name = 'Home_Team')
gtype = pd.Series(gtype, name = 'Type')
df = pd.concat([attendance, dates, dblh, dow, stadia, dn, scorea, scoreh, winner, team, gtype], axis = 1)

# Subset to remove non-season data (playoffs, etc.) that are outside of the window

df = df[df.Date > 20100000].reset_index(drop = True)
df = df[df.Date < 20200000].reset_index(drop = True)

# Create a 2010-2016 sample indicator and add to df

subsamp = [1 if d < 20170000 else 0 for d in df.Date]
df = pd.concat([df, pd.Series(subsamp, name = 'SAMPLE')], axis = 1)

# Subset to remove non-standard stadiums

parks = list(df.Stadium.unique())
counts = [len(df[df.Stadium == p]) for p in parks]
keeps = [p for p in parks if counts[parks.index(p)] > 100]
df = df[df.Stadium.isin(keeps)].reset_index(drop = True)

# Save df

df.to_csv(filepath + 'mlb_data.csv', index = False)

