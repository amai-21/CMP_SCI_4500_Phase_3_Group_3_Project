"""Author: Josh Brown"""

import pandas as pd
from datetime import datetime
from tabulate import tabulate
import glob
# Only needed if creating a new directory
import os

# Calculates the time difference in minutes of the timelog csv
def get_time_difference_in_minutes(file_name, counter):

    column_names = ["Date", "StartTime", "EndTime", "HowManyPeople", "ActivityCode", "Notes"]
    df = pd.read_csv(file_name, na_filter=False, skiprows=2, names=column_names)
    time_format = "%H:%M"
    start_time = df.at[counter, "StartTime"]
    end_time = df.at[counter, "EndTime"]

    dt1 = datetime.strptime(start_time, time_format)
    dt2 = datetime.strptime(end_time, time_format)

# Calculates the time difference of start_time and end_time in minutes
    if end_time == "0:00":
        dt2 = datetime.strptime("23:59", "%H:%M")
        difference = dt2 - dt1
        time_log_minutes = int(difference.total_seconds() / 60) + 1
    else:
        difference = dt2 - dt1
        time_log_minutes = int(difference.total_seconds() / 60)
    return time_log_minutes

# Gets weekday from date
def get_weekday(file_name, counter):

    column_names = ["Date", "StartTime", "EndTime", "HowManyPeople", "ActivityCode", "Notes"]
    df = pd.read_csv(file_name, na_filter=False, skiprows=2, names=column_names)
    date = df.at[counter, "Date"]

    date_object = datetime.strptime(date, "%m/%d/%Y")
    day_of_week = date_object.strftime("%A")
    return day_of_week

# Gets row length of csv file
def get_row_length(file_name):
    df = pd.read_csv(file_name, na_filter=False, skiprows=2)
    row_count = len(df)
    return row_count

# Main
if __name__ == '__main__':

    # Gets all csv files from folder
    files = glob.glob("*.csv")

    # Weekday minutes
    monday_min= 0
    tuesday_min = 0
    wednesday_min = 0
    thursday_min = 0
    friday_min = 0
    saturday_min = 0
    sunday_min = 0

    for file_name in files:
        i = 0
        while i < get_row_length(file_name):
            if str(get_weekday(file_name, i)) == "Monday":
                monday_min = get_time_difference_in_minutes(file_name, i)
            if str(get_weekday(file_name, i)) == "Tuesday":
                tuesday_min = get_time_difference_in_minutes(file_name, i)
            if str(get_weekday(file_name, i)) == "Wednesday":
                wednesday_min = get_time_difference_in_minutes(file_name, i)
            if str(get_weekday(file_name, i)) == "Thursday":
                thursday_min = get_time_difference_in_minutes(file_name, i)
            if str(get_weekday(file_name, i)) == "Friday":
                friday_min = get_time_difference_in_minutes(file_name, i)
            if str(get_weekday(file_name, i)) == "Saturday":
                saturday_min += get_time_difference_in_minutes(file_name, i)
            if str(get_weekday(file_name, i)) == "Sunday":
                sunday_min += get_time_difference_in_minutes(file_name, i)
            i += 1

    # Report 4 csv headers and stuff
    report4 = {
        "Weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Total Minutes": [str(monday_min), str(tuesday_min), str(wednesday_min), str(thursday_min),
         str(friday_min), str(saturday_min), str(sunday_min)]
    }

    # This code might be obsolete
    '''
    # Creates a directory to save the csv
    make_dir = "report4"
    os.makedirs(make_dir, exist_ok=True)

    # Creates report4.csv
    report4_df = pd.DataFrame(report4)
    csv_file_path = "report4/report4.csv"
    report4_df.to_csv(csv_file_path, index=False)
    '''

    # Creates report4.txt
    report4_df = pd.DataFrame(report4)
    csv_file_path = "PhaseThreeReport4.txt"
    report4_df.to_csv(csv_file_path, index=False)

    # Displays report4 as a table in the console
    report4_header = ["Weekday", "Total Minutes"]
    print(tabulate(report4, headers=report4_header, tablefmt="grid"))