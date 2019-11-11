#from UnixConverter import unix_Converter
from datetime import datetime
from statistics import mean
import structures


def findMinTime(con):
    con.query("SELECT MIN(Start_Time) FROM raw")
    minTimeResult = con.store_result()
    minTime = minTimeResult.fetch_row(maxrows=0)
    return(minTime)

def findMaxTime(con):
    con.query("SELECT MAX(End_Time) FROM raw")
    result = con.store_result()
    maxTimeResult = result
    maxTime = maxTimeResult.fetch_row(maxrows=0)
    return(maxTime)

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
    listOfValues=averageData(column)
    totalAmount=0
    totalValues=0
    for i in listOfValues:
        totalAmount+=i
        totalValues+=1
    print(totalAmount/totalValues)


#Find TimeIntervals and add Timeintervals to proc table
def FindDayIntervals(db):
    maxTime = findMaxTime(db)
    minTime = findMinTime(db)
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
    # add_column(db=con, table='proc', column='TimeInterval', data=FindDayIntervals())


def populate_meters(db):
    db.query("SELECT DISTINCT Charge_Station_Name FROM raw;")
    dbnames = db.store_result()
    chargerindex = 0  # Index of charger name in 'meters'
    for chargertup in dbnames.fetch_row(maxrows=0):
        chargername = chargertup[0]
        meterdict[chargername] = chargerindex
        chargerindex += 1
        meters.append(structures.Meter(chargername))


def chargeTypeUsages(db, startTime, endTime, stationName):
    rowDataList = gatherRows(startTime, endTime, db)

    DCCData = 0
    CHADData = 0
    for row in rowDataList:
        if row[0] == stationName:
            if row[6] == 'CHADEMO':
                CHADData += 1
            elif row[6] == 'DCCOMBOTYP1':
                DCCData += 1
            else:
                print("new charger type: {}".format(row[6]))


def detect_congestion(db, start_time, end_time, metername):
    """Search for congestion **between** start_time and end_time
    Returns True if avg time between usages is less than CONGESTION_THRESH"""
    CONGESTION_THRESH = 60

    time_between_charges = []
    previous_previous_time = start_time  # When I made this variable, I realized all was lost.
    current_time = start_time
    while int(current_time) < end_time:
        db.query("SELECT MIN(End_Time) FROM raw WHERE Charge_Station_Name='{}' AND End_Time>'{}'".format(metername, previous_previous_time))
        previous_time = db.store_result().fetch_row()[0][0]
        db.query("SELECT MIN(Start_Time) FROM raw WHERE Charge_Station_Name='{}' AND Start_Time>'{}'".format(metername, previous_time))
        current_time = db.store_result().fetch_row()[0][0]
        previous_previous_time = previous_time
        time_between_charges.append(int(current_time) - int(previous_time))
    if mean(time_between_charges) <= CONGESTION_THRESH:
        return True
    else:
        return False


# BEGIN MAIN PROBLEM DETECTION #

populate_meters(con)

for meter in meters:
    days = FindDayIntervals(con)
    i = 0
    for day in days:
        startofday = days[i]
        endofday = days[i+1]
        if detect_congestion(con, startofday, endofday, meter.name):
            meter.probsems.append(structures.ProblemCongestion(startofday, endofday))
