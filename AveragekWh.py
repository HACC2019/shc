import MySQLdb
import sys
con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')

cursorObj = con.cursor()
global starttime
global endtime
global rowDataList
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

starttime = 1535768703
endtime = 1535878761
column = 3
averageDataActually(column)
#starttime = starttimenum.to_bytes(32, 'little')
#endtime = endtimenum.to_bytes(32, 'little')
#print(starttime)
#print(endtime)




