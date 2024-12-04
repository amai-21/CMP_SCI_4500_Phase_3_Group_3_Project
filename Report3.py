"""
Language: Python 3

IDE: VS Code

HOW TO RUN: Navigate to where the python project and execute as python {projectname}.py, because python is an interpreted language, an external library is used to "compile" it for an executable.
    So you can either run the script or click on the executable. It was produced with a library called pyinstaller and ran with this command:
     python c:.users.rohan.appdata.local.packages.pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0.localcache.local-packages.python312.site-packages.pyinstaller. --onefile {projectA}.py
    Where the periods are forward slashes. (unicode parsing problem if leaving path in multi line comment)
Authors: Rohan Keenoy

Date: 10/24/2024

DATA STRUCTURES: A pandas dataframe is commonly used in scientific applications, it can be thought of as a N-d array,can have headers, and is structured as the csv is structured. 
    For this project using a dataframe is a no brainer. R has a similar structure. A dictionary is used to append to rows in a dataframe. This generated per row-entry.  An array called listOfDirectoryFiles is initalized as a class variable, this is a simple array that holds on to
    files to traverse. This is the structure called "L" in the specification. Uses several different dictionaries for mapping purposes.
    
General Flow: basically just opperates straight down the checks with a flag variable called "checkFailed" in the function OpenFilesAndCheck, if a check is failed , it calls a function to write to file that it failed, 
this does not happen on the exception of a warning though - it will just print a warning and set the flag back to 0, which is valid. It then continues. 

EXTERNAL files: Any file that is valid is used in the directory, generated a ValidityChecks.txt file.

External preperation: Because python is an interpreted language a software pyinstaller will be used to generate an executable. 
    
References:
    0.)Regex testing on : https://regex101.com/
    1.) Date checks: https://www.geeksforgeeks.org/python-validate-string-date-format/, 
    format reference https://pynative.com/python-datetime-format-strftime/
    2.) General Pandas referencing on documentation site: https://pandas.pydata.org/docs/getting_started/index.html
    
"""


import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os
import re

def report3(diction):
    flat = []

    for name, activities in diction.items():
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

def report3Main():
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
    masterDictionary = mapNamesToDictionaries(dictionaries, names)
    #print(masterDictionary)
    report3(masterDictionary)
    #validDf = returnDf()
    #dict = processDf(validDf)
    #report2(dict)