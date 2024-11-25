import pandas as pd
from datetime import datetime
from tabulate import tabulate

def report2(diction):
    listOfItems = list(diction.items())
    newDf = pd.DataFrame(listOfItems,columns=['ActivityCode', 'MinutesSpent'])
    newDf = newDf.sort_values(by="ActivityCode")
    print(newDf.to_string(index=False))
    print(tabulate(newDf, headers="keys", tablefmt="grid", showindex=False))


def returnDf():
    data = pd.read_csv("KeenoyRohanLog.csv",header = None, na_filter=False)
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

if __name__ == '__main__':
    validDf = returnDf()
    dict = processDf(validDf)
    report2(dict)
    
    