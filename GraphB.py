"""
Language: Python 3

IDE: VS Code

HOW TO RUN: Navigate to where the python project and execute as python {projectname}.py, because python is an interpreted language, an external library is used to "compile" it for an executable.
    So you can either run the script or click on the executable. It was produced with a library called pyinstaller and ran with this command:
     python c:.users.rohan.appdata.local.packages.pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0.localcache.local-packages.python312.site-packages.pyinstaller. --onefile {projectA}.py
    Where the periods are forward slashes. (unicode parsing problem if leaving path in multi line comment)
Authors: Rohan Keenoy

Date: 12/02/2024

DATA STRUCTURES: A pandas dataframe is commonly used in scientific applications, it can be thought of as a N-d array,can have headers, and is structured as the csv is structured. 
    For this project using a dataframe is a no brainer. R has a similar structure. A dictionary is used to append to rows in a dataframe. This generated per row-entry.  An array called listOfDirectoryFiles is initalized as a class variable, this is a simple array that holds on to
    files to traverse. 
    
General Flow: Processes data and then graphs it using a very common library called matplotlib. 

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
import matplotlib.pyplot as plt
import numpy as np

#Generates the report itself. had to do some dictionary processing 
def report3(diction):
    flat = []
    for name, activities in diction.items():
        for activity_code, amount in activities.items():
            flat.append([name, activity_code, amount])
    #print(flat)
    df = pd.DataFrame(flat, columns=['Name', 'Activity Code', 'Amount'])
    df = df.pivot(index='Name', columns='Activity Code', values='Amount')
    df = df.fillna(0)
    print(tabulate(df.values, headers='keys', tablefmt='grid', showindex=True))
    #https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
    axImg = plt.imshow(df, cmap='autumn')
    plt.colorbar(axImg)
    plt.xticks(ticks=range(len(df.columns)), labels=df.columns)
    plt.yticks(ticks=range(len(df.index)), labels=df.index)
    plt.title("Report 3 (GRAPH B) - Activity by Name heatmap")
    plt.xlabel("Activity Code")
    plt.ylabel("Name")
    plt.savefig("graphB_Report3")
    input("Press enter and the graph will display in a seperate window. To continue window must be exited.")
    plt.show()
    
        
    
#returns a df of files
def returnDf(file):
    data = pd.read_csv(file,header = None, na_filter=False)
    df = pd.DataFrame(data)
    return df

#https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
#returns the time
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
#returns dictionary with codes       
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
#gets name, returns the names
def getNames(df):
    firstName = df.iloc[0, 0]
    lastName = df.iloc[0,1]
    name = firstName + " " + lastName
    #print(name)
    return name
#maps the names to dictionaries   
def mapNamesToDictionaries(diction, names):
    #print("Names:", names)
    #print("Dictionaries:", diction)
    masterDiction = {}
    for name, dictionary in zip(names, diction):
        masterDiction[name] = dictionary 
    return masterDiction
#driver of this program
def graphBMain():
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