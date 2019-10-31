from UnixConverter import unix_Converter
unix_Converter()
import sqlite3

con = sqlite3.connect('shc.db')
cursorObj = con.cursor()
def makeTimeStamps():
    max_time = cursorObj.execute("SELECT MAX([End Time]) FROM raw")
    min_time =  cursorObj.execute("SELECT MIN([Start Time]) FROM raw")
   # for i in max_time


    print(min_time)
    print(max_time)
