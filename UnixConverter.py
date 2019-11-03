from datetime import datetime
import MySQLdb

#con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
#con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def sql_fetch_StartTimes(con):
    con.query('SELECT Start_Time FROM raw')
    StartTimeResult=con.store_result()
    StartTime=StartTimeResult.fetch_row(maxrows=0)
    StartList=[]
    for row in StartTime:
        StartList.append(str(row))
    return StartList

def sql_fetch_EndTimes(con):
    #EndTime = cursorObj.execute('SELECT End_Time FROM raw')
    con.query('SELECT End_Time FROM raw')
    EndTimeResult = con.store_result()
    EndTime=EndTimeResult.fetch_row(maxrows=0)
    EndList=[]
    for row in EndTime:
        EndList.append(str(row))
    return EndList


def unix_ConvertStart(con):
    StartListInt=[]
    StartList=sql_fetch_StartTimes(con)
    for date in StartList:
        try:
            utc = datetime.strptime(date, "('%m-%d-%y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        except ValueError:
            utc = datetime.strptime(date, "('%m/%d/%Y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        StartListInt.append(utcint)
    return StartListInt

def unix_ConvertEnd(con):
    EndListInt = []
    EndList=sql_fetch_EndTimes(con)
    for date in EndList:
        try:
            utc = datetime.strptime(date, "('%m-%d-%y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        except ValueError:
            utc = datetime.strptime(date,"('%m/%d/%Y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        EndListInt.append(utcint)
    return EndListInt

print(unix_ConvertStart())
print(unix_ConvertEnd())