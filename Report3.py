import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os
import re

def report3(diction):
    flat = []

    for name, activities in masterDictionary.items():
        for activity_code, amount in activities.items():
            flat.append([name, activity_code, amount])
    #print(flat)
    df = pd.DataFrame(flat, columns=['Name', 'Activity Code', 'Amount'])
    df = df.pivot(index='Name', columns='Activity Code', values='Amount')
    df = df.fillna(0)
    output = tabulate(df, headers='keys', tablefmt='grid', showindex=True)
    print(f'Report 3 Generated and Saved: {output}')
    with open("Report3.txt", "w") as file:
        file.write(output)


def returnDf(file):
    data = pd.read_csv(file,header = None, na_filter=False)
    df = pd.DataFrame(data)
    return df

#https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
def processTime(df):
    startMinutes = df.iloc[2:,1].tolist()
    endMinutes = df.iloc[2:,2].tolist()
    #print(startMinutes, endMinutes)
    startTimes = []
    endTimes = []
    for time in range(len(startMinutes)):
        startTimes.append(datetime.strptime(startMinutes[time],'%H:%M'))
    for time in range(len(endMinutes)):
        endTimes.append(datetime.strptime(endMinutes[time],'%H:%M'))
    timeDifference = []
    for start, end in zip(startTimes, endTimes):
        totalTime = (end-start).total_seconds()/60
        timeDifference.append(totalTime)
    
    #print(timeDifference)
    return timeDifference
        
def processDf(df):
    diction = {}
    activityCodeColumn = df.iloc[:, 4][df.iloc[:, 4] != ""].tolist()
    minutesSpendPerColumn = processTime(df)
    for key in range(len(activityCodeColumn)):
        ac = activityCodeColumn[key]
        minutes = minutesSpendPerColumn[key]
        #print(ac,minutes)
        if ac not in diction:
            diction[ac] = minutes
        else:
            diction[ac] += minutes
    return diction

def getNames(df):
    firstName = df.iloc[0, 0]
    lastName = df.iloc[0,1]
    name = firstName + " " + lastName
    #print(name)
    return name
    
def mapNamesToDictionaries(diction, names):
    #print("Names:", names)
    #print("Dictionaries:", diction)
    masterDiction = {}
    for name, dictionary in zip(names, diction):
        masterDiction[name] = dictionary 
    return masterDiction

if __name__ == '__main__':
    #need to modify this to take in an array of csv files
    # but for now...
    csvFiles = []
    dfs = []
    dictionaries = []
    names = []
    regPat = r"^[A-Za-z]+[lL][oO][gG]\.[cC][sS][vV]$"
    for file in os.listdir():
        if re.match(regPat,file):
            #print(f"opening {file}")
            csvFiles.append(file)
            validDf = returnDf(file)
            names.append(getNames(validDf))
            dfs.append(validDf)
            dict = processDf(validDf)
            dictionaries.append(dict)
    
    #print(dictionaries)
    #print(names)
    masterDictionary = mapNamesToDictionaries(dictionaries, names)
    #print(masterDictionary)
    report3(masterDictionary)
    #validDf = returnDf()
    #dict = processDf(validDf)
    #report2(dict)