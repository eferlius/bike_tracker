import fitparse
import pandas as pd
import numpy as np
import basic
import os
import matplotlib.pyplot as plt

def get_data(fitfile, names = []):
    if names == []:
        names = get_dataNames(fitfile)
    # timestamp is actually a datetime object
    allRecords = []
    for record in fitfile.get_messages("record"):
        thisRecord = []
        for name in names:
            for data in record:
                value = np.nan
                if data.name == name:
                    value=data.value
                    break
            thisRecord.append(value)
        allRecords.append(thisRecord)
                  
    df = pd.DataFrame(allRecords, columns = names)
    
    df['time'] = (df['timestamp'].values-df['timestamp'].values[0])/np.timedelta64(1, 's')
    return df

def get_dataNames(fitfile):
    names = []
    for record in fitfile.get_messages("record"):
        for data in record:
            name = data.name
            if name not in names:
                names.append(name)
    return names

def print_content(fitfile):
    for record in fitfile.get_messages("record"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:
            # Print the name and value of the data (and the units if it has any)
            if data.units:
                print(" * {}: {} ({})".format(data.name, data.value, data.units))
            else:
                print(" * {}: {}".format(data.name, data.value))
        print("---")

# Load the FIT file
filePartialName = "2023-01-01"
filePartialName = "2023-01-05"
filePartialName = "2023-01-30"
# filePartialName = "2022-12-27"
# filePartialName = "2022-12-14"
# files, dirs = basic.utils.find_files_and_dirs_in_dir(r'G:\My Drive\python projects\bike tracker\Tests',
# listDepth = [2],listExt='.fit',listPartialName = filePartialName)
files, dirs = basic.utils.find_files_and_dirs_in_dir(r'G:\My Drive\FILE\activites garmin',
listExt='.fit',listPartialName = filePartialName)

fileCompleteName = files[0]
fileName = os.path.split(fileCompleteName)[1]
fitfile = fitparse.FitFile("{}".format(fileCompleteName))

names = ['timestamp', 'speed', 'heart_rate', 'cadence']
df = get_data(fitfile, names)
df = get_data(fitfile)
print(df.columns)


t = df['time'].values

sp = df['speed'].values*3.6
hr = df['heart_rate'].values
cad = df['cadence'].values
alt = df['altitude'].values
dst = df['distance'].values




basic.plots.plts([t]*4,[sp,hr,cad, alt], sharex = True, ncols = 1,
                 mainTitle = fileName,
                 listTitles=['speed', 'heart_rate', 'cadence', 'altitude'], 
                 listXlabels=['','','','time [s]'],
                 listYlabels=['[km/h]','[bpm]','[rpm]'],
                 listOfkwargs=[{},{'color':'C3'},{'color':'C1'}], 
                 common_kwargs={'marker':'None'})

basic.plots.plts([t]*5,[sp,hr,cad, alt, dst], sharex = True, ncols = 1,
                 mainTitle = fileName,
                 listTitles=['speed', 'heart_rate', 'cadence', 'altitude','distance'], 
                 listXlabels=['','','','time [s]'],
                 listYlabels=['[km/h]','[bpm]','[rpm]'],
                 listOfkwargs=[{'color':'C{}'.format(i)} for i in range(5)], 
                 common_kwargs={'marker':'None'})

plt.tight_layout()

plt.figure()
plt.plot(df['position_long'].values,df['position_lat'].values)

plt.draw()
# plt.show(block = False)
plt.pause(0.01)

plt.show()

 
    

    
    