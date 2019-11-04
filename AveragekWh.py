import MySQLdb
con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
cursorObj = con.cursor()

#given start + end time, find values between it, find avg
#select avg kwh from raw where timestamp is less than or greater than __

def gatherRows(starttime, endtime):
    con.query('SELECT * FROM raw WHERE Start_Time BETWEEN (%s!) AND (%s!)'(starttime, endtime))
    rowDataResult = con.store_result()
    rowData = rowDataResult.fetch_row(maxrows=0)
    rowDataList = []
    for i in rowDataResult:
        rowDataList.append(str(i))
    print(rowDataList)


#def averageData(column):



gatherRows(1535768703,1535796123)