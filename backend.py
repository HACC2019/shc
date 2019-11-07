#from UnixConverter import unix_Converter
from datetime import datetime
#unix_Converter()
import MySQLdb
import structures


global meters  # List of structures.Meter objects
meters = []
global meterdict  # Dictionary of charger name vs 'meters' index
meterdict = {}

con = MySQLdb.connect(db="hacc",host="pf.parsl.dev", user="hacc", passwd="hacc2019")
cursorObj = con.cursor()


def findMinTime(con):
    con.query("SELECT MIN(Start_Time) FROM raw")
    minTimeResult = con.store_result()
    minTime = minTimeResult.fetch_row(maxrows=0)
    return(minTime)


def findMaxTime(con):
    con.query("SELECT MAX(End_Time) FROM raw")
    maxTimeResult = con.store_result()
    maxTime = maxTimeResult.fetch_row(maxrows=0)
    return(maxTime)


def add_column(db, table, column, data, dtype="TEXT"):
    """Set a column equal to a list, creating the column if it doesn't exist"""

    # Sanity checks #
    if type(db) is not MySQLdb.connections.Connection:
        raise TypeError("Expected MySQLdb.connections.connection, got {}".format(type(db)))
    if type(table) is not str:
        raise TypeError("Expected string, got {}".format(type(table)))
    if type(column) is not str:
        raise TypeError("Expected string, got {}".format(type(column)))
    if type(data) is not list:
        raise TypeError("Expected list, got {}".format(type(data)))

    db.autocommit(on=True)  # Make sure to actually save changes

    # Try to drop column if it exists #
    try:
        db.query("ALTER TABLE {} DROP COLUMN {}".format(table, column))
    except MySQLdb._exceptions.OperationalError:
        pass

    # Find max row num to know when to stop updating and start inserting #
    cur = db.cursor()
    cur.execute("SELECT MAX(ID) FROM {}".format(table))
    maxindex = cur.fetchall()

    # Create column and add in data #
    db.query("ALTER TABLE {} ADD {} {}".format(table, column, dtype))
    i = 1
    for value in data:  # Replace every row with data starting at ID 1
        if i <= maxindex[0][0]:  # Update if row exists
            db.query("UPDATE {} SET {}='{}' WHERE ID={}".format(table, column, value, i))
        if i > maxindex[0][0]:  # Insert if row doesn't exist
            db.query("INSERT INTO {} ({}) VALUES ('{}')".format(table, column, value))
        i += 1

#Unix Converter and stuff
def sql_fetch_StartTimes(con):
    con.query('SELECT Start_Time FROM raw')
    StartTimeResult=con.store_result()
    StartTime=StartTimeResult.fetch_row(maxrows=0)
    StartList=[]
    for row in StartTime:
        StartList.append(str(row))
    return StartList


def sql_fetch_EndTimes(con):
    #EndTime = cursorObj.execute('SELECT End_Time FROM raw')
    con.query('SELECT End_Time FROM raw')
    EndTimeResult = con.store_result()
    EndTime=EndTimeResult.fetch_row(maxrows=0)
    EndList=[]
    for row in EndTime:
        EndList.append(str(row))
    return EndList


def unix_ConvertStart(con):
    StartListInt=[]
    StartList=sql_fetch_StartTimes(con)
    for date in StartList:
        try:
            utc = datetime.strptime(date, "('%m-%d-%y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        except ValueError:
            utc = datetime.strptime(date, "('%m/%d/%Y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        StartListInt.append(utcint)
    return StartListInt


def unix_ConvertEnd(con):
    EndListInt = []
    EndList=sql_fetch_EndTimes(con)
    for date in EndList:
        try:
            utc = datetime.strptime(date, "('%m-%d-%y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        except ValueError:
            utc = datetime.strptime(date,"('%m/%d/%Y %H:%M:%S',)")
            #print(int(utc.timestamp()) - 36000)
            utcint = int(utc.timestamp()) - 36000
            #print (utcint)
        EndListInt.append(utcint)
    return EndListInt


#given start + end time, find values between it, find avg
#select avg kwh from raw where timestamp is less than or greater than __
def gatherRows(starttime, endtime, con):
    con.query(("SELECT * FROM raw WHERE Start_Time >= '{}' AND End_Time <= '{}'".format(starttime, endtime)))
    rowData = con.store_result()
    rowDataResults = rowData.fetch_row(maxrows=0)
    rowDataList = []
    for i in rowDataResults:
        rowDataList.append(i)
    print(rowDataList)
    return rowDataList


def averageData(column):
    rowDataList = gatherRows(starttime, endtime, con)
    columndata = []
    numba=0
    for i in rowDataList:
        columndata.append(rowDataList[numba][column])
        numba+=1
    print(columndata)
    return columndata


def averageDataActually(column):
    listOfValues=averageData(column)
    totalAmount=0
    totalValues=0
    for i in listOfValues:
        totalAmount+=i
        totalValues+=1
    print(totalAmount/totalValues)


#Gather by Time and Average by Column functions
    #given start + end time, find values between it, find avg
    #select avg kwh from raw where timestamp is less than or greater than __
def gatherRows(starttime, endtime, con):
    con.query(("SELECT * FROM raw WHERE Start_Time >= '{}' AND End_Time <= '{}'".format(starttime, endtime)))
    rowData = con.store_result()
    rowDataResults = rowData.fetch_row(maxrows=0)
    rowDataList = []
    for i in rowDataResults:
        rowDataList.append(i)
    print(rowDataList)
    return rowDataList


def averageData(starttime, endtime, column):
    rowDataList = gatherRows(starttime, endtime, con)
    columndata = []
    numba=0
    for i in rowDataList:
        columndata.append(rowDataList[numba][column])
        numba+=1
    print(columndata)
    return columndata


def averageDataActually(starttime, endtime, column):
    listOfValues=averageData(starttime, endtime, column)
    totalAmount=0
    totalValues=0
    for i in listOfValues:
        totalAmount+=i
        totalValues+=1
    print(totalAmount/totalValues)


#Find TimeIntervals and add Timeintervals to proc table
def FindDayIntervals():
    maxTime = findMaxTime(con)
    minTime = findMinTime(con)
    maxTime=int(maxTime[0][0])
    minTime=int(minTime[0][0])
    UnixDayValue=86400
    indexes=int((maxTime-minTime)/UnixDayValue)+1
    TimeIndexes=[]
    for i in range(indexes):
        x=minTime+i*UnixDayValue
        TimeIndexes.append(x)
    TimeIndexes.append(maxTime)
    print(maxTime)
    print(minTime)
    print(TimeIndexes)
    return(TimeIndexes)
    add_column(db=con, table='proc', column='TimeInterval', data=FindDayIntervals())


def populate_meters(db):
    db.query("SELECT DISTINCT Charge_Station_Name FROM raw;")
    dbnames = db.store_result()
    chargerindex = 0  # Index of charger name in 'meters'
    for chargertup in dbnames.fetch_row(maxrows=0):
        chargername = chargertup[0]
        meterdict[chargername] = chargerindex
        chargerindex += 1
        meters.append(structures.Meter(chargername))