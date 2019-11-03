from datetime import datetime
import backend
import MySQLdb

global StartList
global EndList
global StartListInt
global EndListInt

con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
# con = sqlite3.connect('shc.db')
import MySQLdb

#con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
#con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

global StartList
global EndList

def sql_fetch_StartTimes(con):
    con.query('SELECT Start_Time FROM raw')
    StartTimeResult = con.store_result()
    StartTime = StartTimeResult.fetch_row(maxrows=0)
    StartList = []
    for row in StartTime:
        StartList.append(str(row))

def sql_fetch_EndTimes(con):
    con.query('SELECT End_Time FROM raw')
    EndTimeResult = con.store_result()
    EndTime = EndTimeResult.fetch_row(maxrows=0)
    EndList = []
    for row in EndTime:
        EndList.append(str(row))
    return EndList

def unix_ConvertStart(con):
    StartListInt=[]
    StartList=sql_fetch_StartTimes(con)
    for date in StartList:
        try:
            utc = datetime.strptime(date, "('%m-%d-%y %H:%M:%S',)")
            # print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
        except ValueError:
            utc = datetime.strptime(date, "('%m/%d/%Y %H:%M:%S',)")
            # print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
        StartListInt.append(utcint)
    return StartListInt

def unix_ConvertEnd(con):
    EndListInt = []
    EndList=sql_fetch_EndTimes(con)
    for date in EndList:
        try:
            utc = datetime.strptime(date, "('%m-%d-%y %H:%M:%S',)")
            # print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
        except ValueError:
            utc = datetime.strptime(date, "('%m/%d/%Y %H:%M:%S',)")
            # print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            print(utcint)
        EndListInt.append(utcint)

"""(inputtime - starttime)/Unixdays"""
def FindDayIntervals():
    maxTime = backend.findMaxTime(con)
    minTime = backend.findMinTime(con)
    UnixDayValue = 86400
    indexes = int((maxTime - minTime) / UnixDayValue)
    TimeIndexes = []
    for i in range(indexes + 1):
        x = minTime + i * UnixDayValue
        TimeIndexes.append(x)
    TimeIndexes.append(maxTime)
    print(TimeIndexes)

unix_Converter()
print(StartListInt)
print(EndListInt)
FindDayIntervals()

            #print (utcint)
        EndListInt.append(utcint)
    return EndListInt

print(unix_ConvertStart())
print(unix_ConvertEnd())
