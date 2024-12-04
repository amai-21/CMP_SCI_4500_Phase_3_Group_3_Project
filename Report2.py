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
    files to traverse. This is the structure called "L" in the specification.
    
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
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os
import re

#generates the report
def report2(diction):
    # Convert the dictionary into a DataFrame
    listOfItems = list(diction.items())
    newDf = pd.DataFrame(listOfItems, columns=['ActivityCode', 'MinutesSpent'])
    newDf = newDf.sort_values(by="ActivityCode")

    # Add header details
    title = "CS 4500 Development Team Activity Report"
    class_id = "Class ID: CS 4500"
    team_members = ["Adrian Harter", "Rohan Keenoy", "Andy Mai", "Swati Sah", "Josiah Lynn", "Josh Brown"]  
    description = (
        "This report contains details about the activities performed by the CS 4500 development "
        "team. It highlights the total time spent on each activity code."
    )

    # Prepare the header
    header = (
        f"{title}\n"
        f"{class_id}\n"
        f"Team Members: {', '.join(team_members)}\n"
        f"Description: {description}\n\n"
    )

    # Prepare the body of the report
    body = tabulate(newDf, headers="keys", tablefmt="grid", showindex=False)

    # Combine header and body
    report_content = header + body

    # Print the report to the console
    print(f"Report 2 Generated and Saved to File:\n{report_content}\n")

    # Save the report to a text file
    with open("PhaseThreeReport4.txt", "w") as file:
        file.write(report_content)

#reads a CSV as a dataframe
def returnDf(filepath):
    data = pd.read_csv(filepath, header=None, na_filter=False)
    df = pd.DataFrame(data)
    return df

#processes the time
def processTime(df):
    startMinutes = df.iloc[2:, 1].tolist()
    endMinutes = df.iloc[2:, 2].tolist()
    startTimes = [datetime.strptime(time, '%H:%M') for time in startMinutes]
    endTimes = [datetime.strptime(time, '%H:%M') for time in endMinutes]
    timeDifference = [(end - start).total_seconds() / 60 for start, end in zip(startTimes, endTimes)]
    return timeDifference

#returns a dictionary after processing the dataframe
def processDf(df):
    diction = {}
    activityCodeColumn = df.iloc[:, 4][df.iloc[:, 4] != ""].tolist()
    minutesSpendPerColumn = processTime(df)
    for key in range(len(activityCodeColumn)):
        ac = activityCodeColumn[key]
        minutes = minutesSpendPerColumn[key]
        if ac not in diction:
            diction[ac] = minutes
        else:
            diction[ac] += minutes
    return diction


#main driver
def report2Main():
    csvFiles = []
    dfs = []
    dictionaries = []
    names = []
    combined_dict = {}
    
    regPat = r"^[A-Za-z]+[lL][oO][gG]\.[cC][sS][vV]$"

    for file in os.listdir():
        if re.match(regPat, file):
            print(f"Processing file: {file}")
            csvFiles.append(file)
            validDf = returnDf(file)
            dfs.append(validDf)
            dict = processDf(validDf)
            dictionaries.append(dict)
            for key, value in dict.items():
                if key not in combined_dict:
                    combined_dict[key] = value
                else:
                    combined_dict[key] += value

    report2(combined_dict)




