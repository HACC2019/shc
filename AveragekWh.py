import MySQLdb
import sys
con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
cursorObj = con.cursor()
global starttime
global endtime
#given start + end time, find values between it, find avg
#select avg kwh from raw where timestamp is less than or greater than __

def gatherRows(starttime, endtime):
    con.query(("SELECT * FROM raw WHERE Start_Time >= '{}' AND End_Time <= '{}'".format(starttime, endtime)))
    rowData = con.store_result()
    rowDataResults = rowData.fetch_row(maxrows=0)
    rowDataList = []
    for i in rowDataResults:
        rowDataList.append(str(i))
    print(rowDataList)



#def averageData():



#starttime = bytes([1535768703]);
#endtime = bytes([1535878761]);

starttime = 1535768703
endtime = 1535878761

#starttime = starttimenum.to_bytes(32, 'little')
#endtime = endtimenum.to_bytes(32, 'little')
#print(starttime)
#print(endtime)

gatherRows(starttime, endtime)


