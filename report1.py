"""
Language: Python 3

IDE: VS Code

HOW TO RUN: Navigate to where the python project and execute as python {projectname}.py, because python is an interpreted language, an external library is used to "compile" it for an executable.
    So you can either run the script or click on the executable. It was produced with a library called pyinstaller and ran with this command:
     python c:.users.rohan.appdata.local.packages.pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0.localcache.local-packages.python312.site-packages.pyinstaller. --onefile {projectA}.py
    Where the periods are forward slashes. (unicode parsing problem if leaving path in multi line comment)
Authors: Josh Brown, Adrian Harter

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
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# set so that graphs update upon execution
plt.isinteractive()


# checks to see if names taken from dataframes are in need of spacing
def has_space(s):
    for char in s:
        if char == " ":
            return True
    return False


# for strings that don't have spaces, splits that string into two substrings and adds a space between them
def input_space(s):
    for char in range(len(s)):
        if s[char].isupper() and char > 0:
            mem_char = s[char]
            words = s.split(s[char])
            name = words[0] + " " + (mem_char + words[1])
        else:
            continue
        return name


# uses 'glob' to match all files in wd to .csv, and adds them to a list. List is vectorized, returns vector
def collect_csv_in_wd():
    temp_list = []
    for i in glob.glob(r'*.csv'):
        # only .csv files
        temp_list.append(i)
        temp_list.sort()
    return temp_list


# takes a list of .csv files and calculates total minutes worked per person, returning amounts as listed items
def get_minutes_worked(a_list):
    temp_list = []
    for csv in a_list:
        column_names = ["Date", "Time1", "Time2"]
        df = pd.read_csv(csv, usecols=[0, 1, 2], names=column_names)
        df = df.drop(df.index[[0, 1]], axis=0)
        accumulator = 0
        template = "%H:%M"
        for index in df.index:
            a = df.loc[index, "Time1"]
            b = df.loc[index, "Time2"]
            dt1 = datetime.strptime(a, template)
            dt2 = datetime.strptime(b, template)
            if b == "0:00":
                dt2 = datetime.strptime("23:59", template)
                difference = dt2 - dt1
                difference_int = int(difference.total_seconds() / 60) + 1
            else:
                difference = dt2 - dt1
                difference_int = int(difference.total_seconds() / 60) + 1
            accumulator += difference_int
        temp_list.append(accumulator)
    return temp_list


def create_dataframe(list_a, list_b):
    temp_dict = {'Name': pd.Series(list_a), 'Total Time Logged (Minutes)': pd.Series(list_b)}
    temp_df = pd.DataFrame(temp_dict)
    return temp_df


# gets a list of .csv files and combines first and last names, then returns them as listed items
def get_names(a_list):
    temp_list = []
    for csv in a_list:
        column_names = ["Last Name", "First Name"]
        df = pd.read_csv(csv, nrows=1, usecols=[0, 1], names=column_names)
        name = df.at[0, "First Name"] + df.at[0, "Last Name"]
        flag = has_space(name)
        if not flag:
            # in the event that the abstracted full name is not spaced
            name = input_space(name)
        temp_list.append(name)
    return temp_list


# generates report from collected dataframe info
def df_to_txt(df,firstAndLastDict):
    file = open("PhaseThreeReport1.txt", 'w')
    #file.write("sample header\n")
    file.write("Report 1 Generated.\n")
    file.write("CS 4500\n")
    file.write(f"Report contains information for {firstAndLastDict}\n")
    file.write("Report contains Minutes spent per person in cs4500.\n")
    file.write("Group B\n")
    file.write("All members: Rohan Keenoy, Adrian Harter, Swati Shah, Josh brown, Andy Mai, Josiah Lyn\n")
    print("Report 1 Generated.")
    print("CS 4500")
    print(f"Report contains information for {firstAndLastDict}")
    print("Report contains Minutes spent per person in cs4500.")
    print("Group B")
    print("All members: Rohan Keenoy, Adrian Harter, Swati Shah, Josh Brown, Andy Mai, Josiah Lyn")

    for index in df.index:
        file.write("-------------------------\n")
        a = df.loc[index, "Name"]
        b = df.loc[index, 'Total Time Logged (Minutes)']
        file.write(str(a) + " | " + str(b) + '\n')
        print(str(a) + " | " + str(b))


# primary method of this program
def df_to_txt_main(firstAndLastDict):
    csv_list = collect_csv_in_wd()
    minutes_list = get_minutes_worked(csv_list)
    names_list = get_names(csv_list)
    df1 = create_dataframe(names_list, minutes_list)
    df_to_txt(df1,firstAndLastDict)


if __name__ == "__main__":
    df_to_txt_main()




