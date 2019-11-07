import backend
import MySQLdb

def chargeTypeUsages(db, startTime, endTime, stationName):
    rowDataList = backend.gatherRows(startTime, endTime, db)

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
    print(CHADData)
    print(DCCData)

startTime = backend.findMinTime(backend.con)[0][0]
endTime = backend.findMaxTime(backend.con)[0][0]
chargeTypeUsages(backend.con, startTime, endTime, "B")