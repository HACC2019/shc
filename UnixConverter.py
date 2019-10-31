from datetime import datetime
import sqlite3
global StartList
global EndList

con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def sql_fetch_StartTimes(con):
    cursorObj.execute('SELECT "Start Time" FROM raw')
    StartTime = cursorObj.fetchall()
    StartList=[]
    for row in StartTime:
        StartList+=row

def sql_fetch_EndTimes(con):
    global EndList
    cursorObj.execute('SELECT "End Time" FROM raw')
    EndTime = cursorObj.fetchall()
    EndList=[]
    for row in EndTime:
        EndList+=row

sql_fetch_StartTimes(con)
sql_fetch_EndTimes(con)

for date in EndList:
    try:
        utc = datetime.strptime(date, '%m-%d-%y %H:%M:%S')
        print(int(utc.timestamp()) - 36000)
    except ValueError:
        utc = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        print(int(utc.timestamp()) - 36000)

for date in StartList:
    try:
        utc = datetime.strptime(date, '%m-%d-%y %H:%M:%S')
        print(int(utc.timestamp()) - 36000)
    except ValueError:
        utc = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        print(int(utc.timestamp()) - 36000)