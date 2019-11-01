from datetime import datetime
import sqlite3
global EndList
import MySQLdb

#con = sqlite3.connect('shc.db')

db = MySQLdb.connect(db= "hacc", host="pf.parsl.dev", user="hacc", passwd="hacc2019")
cursorObj = db.cursor()

def sql_fetch_StartTimes(db):
    StartTime = db.execute("""SELECT 'Start_Time' FROM raw""")
            #StartTime = cursorObj.execute('SELECT "Start Time" FROM raw')
    StartList=[]
    #for row in StartTime:
    #    StartList+=row
    print(StartTime)
sql_fetch_StartTimes(db)
'''
def sql_fetch_EndTimes(db):
    global EndList
    EndTime = cursorObj.execute('SELECT "End_Time" FROM raw')
    EndList=[]
    for row in EndTime:
        EndList+=row
    print(EndList)

#print(sql_fetch_EndTimes(con))

sql_fetch_StartTimes(db)
sql_fetch_EndTimes(db)

def convertUNIX():
    global EndList
    ConvertedList=[]
    for i in EndList:
        x=datetime(i)
        ConvertedList+=(x.strfTime(""))
    print(ConvertedList)

#convertUNIX()'''
