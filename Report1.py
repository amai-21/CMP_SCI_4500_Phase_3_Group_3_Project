import pandas as pd
from datetime import datetime
from tabulate import tabulate

# Gets the last name and first name of the timelog csv
def get_name(csv):
    column_names = ["lastname", "firstname"]
    data_frame = pd.read_csv(csv, na_filter=False, nrows=1, names=column_names)
    name = data_frame.at[0, "lastname"] + data_frame.at[0, "firstname"]
    return  name

# Calculates the time difference in minutes of the timelog csv
def time_difference_in_minutes(start_time, end_time):
    time_format = "%H:%M"
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

# Main?
if __name__ == '__main__':

    #csv file to be used
    csv_file = "BrownJosh.csv"

    # Stores the start and end times of the timelog csv
    column_names = ["Date", "StartTime", "EndTime", "HowManyPeople", "ActivityCode", "Notes"]
    df = pd.read_csv(csv_file, na_filter=False, skiprows=2, names=column_names)
    row_count = len(df)
    column_start_time = df["StartTime"]
    column_end_time = df["EndTime"]

    # Converts the start and end times of the timelog csv into total minutes
    i = 0
    minutes = 0
    while i < row_count:
        start_time_value = column_start_time.values[i]
        end_time_value = column_end_time.values[i]
        minutes = time_difference_in_minutes(start_time_value, end_time_value)
        minutes += minutes
        i += 1

    # Creates report1.csv
    report1 = {
        "Name": [get_name(csv_file)],
        "Total minutes logged": str(minutes)
    }
    report1_df = pd.DataFrame(report1)

    # Creates report1.csv
    csv_file_path = "report1.csv"
    report1_df.to_csv(csv_file_path, index=False)
    print("CSV file " +  csv_file_path + " has been created successfully.")

    # Display report 1 table
    report1_header = ["Name", "Total minutes logged"]
    print(tabulate(report1_df,headers=report1_header,tablefmt="grid"))