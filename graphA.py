import glob
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


# graph formatting
def graph_df(df):
    temp_df = df['Total Time Logged (Minutes)']
    plt.style.use("ggplot")
    plt.rcParams["figure.figsize"] = (12, 10)
    df1.plot.barh(x="Name", y="Total Time Logged (Minutes)", title="Graph A: Total Minutes Worked By Member", color="red")
    plt.xlim(0, (temp_df.max() + 500))
    plt.gca().set_xticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000])
    plt.show()


csv_list = collect_csv_in_wd()
minutes_list = get_minutes_worked(csv_list)
names_list = get_names(csv_list)
df1 = create_dataframe(names_list, minutes_list)
graph_df(df1)

