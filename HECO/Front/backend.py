#from UnixConverter import unix_Converter
from datetime import datetime
#unix_Converter()
import MySQLdb
from statistics import mean
try:
    from .structures import Meter, Problem
except ModuleNotFoundError: # if running directly
    from structures import Meter, Problem

global meters  # List of structures.Meter objects
meters = []
global meterdict  # Dictionary of charger name vs 'meters' index
meterdict = {}

con = MySQLdb.connect(db="hacc",host="pf.parsl.dev", user="hacc", passwd="hacc2019")
cursorObj = con.cursor()


def findMinTime(db):
    db.query("SELECT MIN(Start_Time) FROM Front_raw_data")
    minTimeResult = db.store_result()
    minTime = minTimeResult.fetch_row(maxrows=0)
    return(minTime)


def findMaxTime(db):
    db.query("SELECT MAX(End_Time) FROM Front_raw_data")
    maxTimeResult = db.store_result()
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
def sql_fetch_StartTimes(db):
    db.query('SELECT Start_Time FROM Front_raw_data')
    StartTimeResult=con.store_result()
    StartTime=StartTimeResult.fetch_row(maxrows=0)
    StartList=[]
    for row in StartTime:
        StartList.append(str(row))
    return StartList


def sql_fetch_EndTimes(con):
    #EndTime = cursorObj.execute('SELECT End_Time FROM Front_raw_data')
    con.query('SELECT End_Time FROM Front_raw_data')
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
    con.query(("SELECT * FROM Front_raw_data WHERE Start_Time >= '{}' AND End_Time <= '{}'".format(starttime, endtime)))
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
    db.query("SELECT DISTINCT Charge_Station_Name FROM Front_raw_data;")
    dbnames = db.store_result()
    chargerindex = 0  # Index of charger name in 'meters'
    for chargertup in dbnames.fetch_row(maxrows=0):
        chargername = chargertup[0]
        meterdict[chargername] = chargerindex
        chargerindex += 1
        meters.append(Meter(chargername))


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
        db.query("SELECT MIN(End_Time) FROM Front_raw_data WHERE Charge_Station_Name='{}' AND End_Time>'{}'".format(metername, previous_previous_time))
        previous_time = db.store_result().fetch_row()[0][0]
        db.query("SELECT MIN(Start_Time) FROM Front_raw_data WHERE Charge_Station_Name='{}' AND Start_Time>'{}'".format(metername, previous_time))
        current_time = db.store_result().fetch_row()[0][0]
        previous_previous_time = previous_time
        time_between_charges.append(int(current_time) - int(previous_time))
    if mean(time_between_charges) <= CONGESTION_THRESH:
        return True
    else:
        return False


def findCongestionPercentage(db, start_time, end_time, metername):
    """Search for congestion **between** start_time and end_time
    Returns True if avg time between usages is less than CONGESTION_THRESH"""
    CONGESTION_THRESH = 900

    time_between_charges = []
    previous_previous_time = start_time  # When I made this variable, I realized all was lost.
    current_time = start_time
    while int(current_time) < end_time:
        db.query("SELECT MIN(End_Time) FROM Front_raw_data WHERE Charge_Station_Name='{}' AND End_Time>'{}'".format(metername, previous_previous_time))
        previous_time = db.store_result().fetch_row()[0][0]
        db.query("SELECT MIN(Start_Time) FROM Front_raw_data WHERE Charge_Station_Name='{}' AND Start_Time>'{}'".format(metername, previous_time))
        current_time = db.store_result().fetch_row()[0][0]
        previous_previous_time = previous_time
        time_between_charges.append(int(current_time) - int(previous_time))
    CongestionInstances=0
    for i in time_between_charges:
        if i <= CONGESTION_THRESH:
            CongestionInstances+=1
    print(str(round(100*CongestionInstances/(len(time_between_charges)+1), 2))+"% Congestion")
    congestionPercent = (round(100*CongestionInstances/(len(time_between_charges)+1), 2))
    return congestionPercent


def findDailyPercentage(db, starttime, metername):
    daysOfTheWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    i = 0
    percentages = []
    for day in daysOfTheWeek:
        dayofweek = starttime+(i)*86400
        endofday = dayofweek+86400
        #findCongestionPercentage(db, dayofweek, endofday, metername)
        percentages.append(float(findCongestionPercentage(db, dayofweek, endofday, metername)))
        i+=1
    highestPercentage = (max(percentages))
    highestPercentageIndex = int((percentages.index(highestPercentage)))
    #print("Within this week, " + str(daysOfTheWeek[highestPercentageIndex]) + " had the highest predicted congestion at " + str(highestPercentage) + "%")

    return highestPercentage


def chargeCHADUsages(db, startTime, endTime, stationName):
    rowDataList = gatherRows(startTime, endTime, db)
    CHADData = 0
    #pdb.set_trace()
    for row in rowDataList:
        if row[0] == stationName:
            if row[6] == 'CHADEMO':
                CHADData += 1
            elif row[6] == 'DCCOMBOTYP1':
                pass
            else:
                print("new charger type: {}".format(row[6]))
    print(CHADData)
    return CHADData


def chargeDCCUsages(db, startTime, endTime, stationName):
    rowDataList = gatherRows(startTime, endTime, db)
    DCCData = 0
    for row in rowDataList:
        if row[0] == stationName:
            if row[6] == 'DCCOMBOTYP1':
                DCCData += 1
            elif row[6] == 'CHADEMO':
                pass
            else:
                print("new charger type: {}".format(row[6]))
    print(DCCData)
    return DCCData


def findUsageAverage(starttime, endtime, stationName):
    CHADStatus=False
    DCCStatus=False
    timeInterval=endtime-starttime
    if (chargeCHADUsages(con, starttime, endtime, stationName) == 0) and (chargeDCCUsages(con, starttime, endtime, stationName) == 0):
        #print("From " + str(starttime) + " to " + str(endtime) + " (" + str(round(timeInterval/86400.0, 3)) + " days), both chargers appear to be broken.")
        CHADStatus = True
        DCCStatus = True
    elif chargeCHADUsages(con, starttime, endtime, stationName) == 0:
        #print("From " + str(starttime) + " to " + str(endtime) + " (" + str(round(timeInterval/86400.0, 3)) + " days), the CHADEMO charger appears to be broken.")
        CHADStatus = True
        DCCStatus = False
    elif chargeDCCUsages(con, starttime, endtime, stationName) == 0:
        #print("From " + str(starttime) + " to " + str(endtime) + " (" + str(round(timeInterval/86400.0, 3)) + " days), the DCCOMBOTYP1 charger appears to be broken.")
        CHADStatus = False
        DCCStatus = True
    else:
        pass
        #print("From " + str(starttime) + " to " + str(endtime) + " (" + str(round(timeInterval/86400.0, 3)) + " days), both chargers are being used.")
    statusList={"CHADEMO": CHADStatus, "DCCOMBOTYP1": DCCStatus}
    print(CHADStatus)
    print(DCCStatus)
    return statusList


def FindTimeIntervals(db, timeInterval):
    maxTime = findMaxTime(db)
    minTime = findMinTime(db)
    maxTime=int(maxTime[0][0])
    minTime=int(minTime[0][0])
    UnixDayValue=timeInterval
    indexes=int((maxTime-minTime)/UnixDayValue)+1
    DayIndexes=[]
    for i in range(indexes):
        x=minTime+i*UnixDayValue
        DayIndexes.append(x)
    DayIndexes.append(maxTime)
    print(DayIndexes)
    return DayIndexes
    # add_column(db=con, table='proc', column='TimeInterval', data=FindDayIntervals())


# BEGIN MAIN PROBLEM DETECTION #
def find_problems():
    populate_meters(con)

    for meter in meters:
        days = FindTimeIntervals(con, 86400)
        weeks = FindTimeIntervals(con, 604800)
        try:
            i = 0
            # Checks that run for each day#
            for day in days:
                startofday = days[i]
                endofday = days[i+1]
                #if detect_congestion(con, startofday, endofday, meter.name):
                #    meter.problems.append(Problem(startofday, endofday, "Congestion", 0x7C007E))

                i += 1
        except IndexError:
            print("reached end of table")

        try:
            i = 0
            # Checks that run for each week #
            for week in weeks:
                startofweek = weeks[i]
                endofweek = weeks[i + 1]
                portUse = findUsageAverage(startofweek, endofweek, meter.name)
                if portUse["CHADEMO"] and portUse["DCCOMBOTYP1"]:
                    meter.problems.append(Problem(startofweek, endofweek, "Charger Broken", 0xFF0000))
                elif portUse["CHADEMO"]:
                    meter.problems.append(Problem(startofweek, endofweek, "Broken Port (CHADEMO)", 0xFF00D1))
                elif portUse["DCCOMBOTYP1"]:
                    meter.problems.append(Problem(startofweek, endofweek, "Broken Port (DCCOMBOTYP1)", 0xF0FF00))
                i += 1

        except IndexError:
            print("reached end of table")


'''
find_problems()

for meter in meters:
    for problem in meter.problems:
        print(problem.problemName)
'''