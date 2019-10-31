from UnixConverter import unix_Converter
unix_Converter()
import MySQLdb

con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019")
cursorObj = con.cursor()
def makeTimeStamps():
    max_time = cursorObj.execute("SELECT MAX([End Time]) FROM raw")
    min_time =  cursorObj.execute("SELECT MIN([Start Time]) FROM raw")
   # for i in max_time


    print(min_time)
    print(max_time)
