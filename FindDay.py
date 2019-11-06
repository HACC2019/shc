import backend
import MySQLdb


#con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
#con = sqlite3.connect('shc.db')
cursorObj = backend.con.cursor()

def FindDayIntervals():
    maxTime = backend.findMaxTime(backend.con)
    minTime = backend.findMinTime(backend.con)
    maxTime=int(maxTime[0][0])
    minTime=int(minTime[0][0])
    UnixDayValue=86400
    indexes=int((maxTime-minTime)/UnixDayValue)+1
    TimeIndexes=[]
    for i in range(indexes):
        x=minTime+i*UnixDayValue
        TimeIndexes.append(x)
    TimeIndexes.append(maxTime)
    return(TimeIndexes)



FindDayIntervals()
backend.con.close()