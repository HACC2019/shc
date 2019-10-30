from datetime import datetime
import sqlite3

con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def sql_fetch_StartTimes(con):
    cursorObj.execute('SELECT "Start Time" FROM raw')
    StartTime = cursorObj.fetchall()
    StartList=[]
    for row in StartTime:
        StartList+=row

def sql_fetch_EndTimes(con):
    cursorObj.execute('SELECT "End Time" FROM raw')
    EndTime = cursorObj.fetchall()
    EndList=[]
    for row in EndTime:
        EndList+=row


print(sql_fetch_EndTimes(con))

#StartTime_List = sql_fetch_StartTimes(con)

def convertUNIX():
    now = datetime.now()
    timestamp = datetime.timestamp(now)