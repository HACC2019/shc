from datetime import datetime
import sqlite3

con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def sql_fetch_StartTimes(con):
    cursorObj.execute('SELECT "Start Time" FROM raw')
    StartTime = cursorObj.fetchall()
    for row in StartTime:
        print(row)

def sql_fetch_EndTimes(con):
    cursorObj.execute('SELECT "End Time" FROM raw')
    EndTime = cursorObj.fetchall()
    for row in EndTime:
        print(row)

print(sql_fetch_StartTimes(con))

def convertUNIX():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    print(timestamp)