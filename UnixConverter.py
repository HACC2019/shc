from datetime import datetime
import sqlite3

con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

global StartList
global EndList

def sql_fetch_StartTimes(con):
    global StartList
    cursorObj.execute('SELECT "Start Time" FROM raw')
    StartTime = cursorObj.fetchall()
    StartList = []
    for row in StartTime:
        StartList += row




def sql_fetch_EndTimes(con):
    global EndList
    cursorObj.execute('SELECT "End Time" FROM raw')
    EndTime = cursorObj.fetchall()
    EndList = []
    for row in EndTime:
        EndList += row


#sql_fetch_StartTimes(con)
#sql_fetch_EndTimes(con)
print(StartList)
print(EndList)
#print(sql_fetch_EndTimes(con))
#print(sql_fetch_StartTimes(con))

def convertStartTime():
    global StartList
    for i in StartList:
        ConvertedStart_List = []
        UnixStartTime = datetime.strptime(i, '%m-%d-%Y" "%I:%M:%S')
        UnixStartTime += ConvertedStart_List
        # return int(UnixStartTime.timestamp())
        print(ConvertedStart_List)




