"""
Language: Python 3

IDE: VS Code

HOW TO RUN: Navigate to where the python project and execute as python {projectname}.py, because python is an interpreted language, an external library is used to "compile" it for an executable.
    So you can either run the script or click on the executable. It was produced with a library called pyinstaller and ran with this command:
     python c:.users.rohan.appdata.local.packages.pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0.localcache.local-packages.python312.site-packages.pyinstaller. --onefile {projectA}.py
    Where the periods are forward slashes. (unicode parsing problem if leaving path in multi line comment)
Authors: Josh Brown, Rohan Keenoy

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
import glob
import os

#processes time and returns the difference
def get_time_difference_in_minutes(file_name, counter):
    df = pd.read_csv(file_name, header=None, na_filter=False)
    time_format = "%H:%M"
    start_time = df.iloc[counter, 1]  
    end_time = df.iloc[counter, 2]    

    dt1 = datetime.strptime(start_time, time_format)
    dt2 = datetime.strptime(end_time, time_format)


    if end_time == "0:00":
        dt2 = datetime.strptime("23:59", "%H:%M")
        difference = dt2 - dt1
        time_log_minutes = int(difference.total_seconds() / 60) + 1
    else:
        difference = dt2 - dt1
        time_log_minutes = int(difference.total_seconds() / 60)
    return time_log_minutes
#gets weekday from file name ad returns the day of week
def get_weekday(file_name, counter):
    df = pd.read_csv(file_name, header=None, na_filter=False)
    date = df.iloc[counter, 0]  # Date in column index 0
    try:
        date_object = datetime.strptime(date, "%m/%d/%Y")
        day_of_week = date_object.strftime("%A")
    except ValueError:
        print(f"Skipping invalid date '{date}' at row {counter} in file {file_name}")
        day_of_week = None

    return day_of_week

#returns num of rows in csv
def get_row_length(file_name):
    df = pd.read_csv(file_name, header=None, na_filter=False)
    row_count = len(df)
    return row_count


def report4Main(firstAndLastDict):

    files = glob.glob("*.csv")

    monday_min = 0
    tuesday_min = 0
    wednesday_min = 0
    thursday_min = 0
    friday_min = 0
    saturday_min = 0
    sunday_min = 0

    for file_name in files:
        i = 2  
        while i < get_row_length(file_name):
            weekday = get_weekday(file_name, i)
            if weekday:  
                time_difference = get_time_difference_in_minutes(file_name, i)

                if weekday == "Monday":
                    monday_min += time_difference
                elif weekday == "Tuesday":
                    tuesday_min += time_difference
                elif weekday == "Wednesday":
                    wednesday_min += time_difference
                elif weekday == "Thursday":
                    thursday_min += time_difference
                elif weekday == "Friday":
                    friday_min += time_difference
                elif weekday == "Saturday":
                    saturday_min += time_difference
                elif weekday == "Sunday":
                    sunday_min += time_difference

            i += 1

    
    report4 = {
        "Weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Total Minutes": [str(monday_min), str(tuesday_min), str(wednesday_min), str(thursday_min),
                         str(friday_min), str(saturday_min), str(sunday_min)]
    }

    report4_df = pd.DataFrame(report4)
    csv_file_path = "PhaseThreeReport4.txt"
    report4_df.to_csv(csv_file_path, index=False)


    report4_header = ["Weekday", "Total Minutes"]
    txt_file_path = "PhaseThreeReport4.txt"
    with open(txt_file_path, 'w') as file:
        file.write("Report 4 Generated.\n")
        file.write("CS 4500\n")
        file.write(f"Report contains information for {firstAndLastDict}\n")
        file.write("Report contains Minutes spent per day of the week in cs4500.\n")
        file.write("Group B\n")
        file.write("All members: Rohan Keenoy, Adrian Harter, Swati Shah, Josh brown, Andy Mai, Josiah Lyn\n")
        file.write(tabulate(report4, headers=report4_header, tablefmt="grid"))
    print("report 4 \n")
    print("Report 4 Generated.")
    print("CS 4500")
    print(f"Report contains information for {firstAndLastDict}")
    print("Report contains Minutes spent per day of the week in cs4500.")
    print("Group B")
    print("All members: Rohan Keenoy, Adrian Harter, Swati Shah, Josh Brown, Andy Mai, Josiah Lyn")
    print(tabulate(report4, headers=report4_header, tablefmt="grid"))
