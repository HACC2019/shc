import backend
import MySQLdb

def usesPer(startTime, endTime, stationName):
    rowDataList= backend.gatherRows(startTime, endTime, backend.con)
    DCCuseInstances = 0
    CHADuseInstances = 0
    DCCData = 0
    CHADData=0
    listList=[]
    x=0
    for i in rowDataList:
        if rowDataList[x][0]==stationName:
            listList.append(rowDataList[x][6])
        x+=1
    for i in listList:
        if i == 'CHADEMO':
            CHADData+=1
        elif i == 'DCCOMBOTYP1':
            DCCData+=1
        else:
            print("excuse me")
    print(listList)
    print(CHADData)
    print(DCCData)

startTime=1535981923
endTime=1535989810
usesPer(startTime, endTime, "A")