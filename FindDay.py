import backend
import MySQLdb


con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
#con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def FindDayIntervals():
    maxTime = backend.findMaxTime(con)
    minTime = backend.findMinTime(con)
    UnixDayValue=86400
    indexes=int((maxTime-minTime)/UnixDayValue)
    TimeIndexes=[]
    for i in range(indexes+1):
        x=minTime+i*UnixDayValue
        TimeIndexes.append(x)
    TimeIndexes.append(maxTime)
    print(TimeIndexes)