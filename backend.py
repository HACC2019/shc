#from UnixConverter import unix_Converter
#unix_Converter()
import MySQLdb
#import sqlite3

con = MySQLdb.connect(db="hacc",host="pf.parsl.dev", user="hacc", passwd="hacc2019")
#con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def findMaxTime(con):
    con.query("SELECT MIN([Start_Time]) FROM raw")
    maxTimeResult = con.store_result()
    maxTime = maxTimeResult.fetch_row(maxrows=0)
    return(maxTime)

def findMinTime(con):
    con.query("SELECT MAX([End_Time]) FROM raw")
    minTimeResult = con.store_result()
    minTime = minTimeResult.fetch_row(maxrows=0)
    return(minTime)

    '''max_time = cursorObj.execute("SELECT MAX([End_Time]) FROM raw")
    min_time =  cursorObj.execute("SELECT MIN([Start_Time]) FROM raw")'''
    print(minTime)
    print(maxTime)