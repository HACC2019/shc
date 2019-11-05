import MySQLdb
import sys
con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
cursorObj = con.cursor()
global starttime
global endtime
#given start + end time, find values between it, find avg
#select avg kwh from raw where timestamp is less than or greater than __

def gatherRows(starttime, endtime):
    #con.query('SELECT Start_Time FROM raw WHERE Start_Time >= starttime (%s!) AND (%s!)', (starttime, endtime))
    #con.query('SELECT * FROM raw WHERE Start_Time >= {?} '
    #          'AND '
    #          'End_Time <= {?}' % (int(starttime, ), int(endtime, )))
    #con.query(("SELECT * FROM raw WHERE Start_Time >= '%d' AND End_Time <= '%d", b'(starttime, endtime)'))
    con.query(("SELECT * FROM raw WHERE Start_Time >= '%d' AND End_Time <= '%d", (1535768703, 1535878761)))
    rowData = con.store_result()
    rowDataResults = rowData.fetch_row(maxrows=0)
    con.query('SELECT * FROM raw WHERE Start_Time BETWEEN (%s!) AND (%s!)'(starttime, endtime))
    rowDataList = []
    for i in rowDataResults:
        rowDataList.append(str(i))
    print(rowDataList)


#def averageData(column):

#starttime = bytes([1535768703]);
#endtime = bytes([1535878761]);

starttimenum = 1535768703
endtimenum = 1535878761

starttime = starttimenum.to_bytes(32, 'little')
endtime = endtimenum.to_bytes(32, 'little')
print(starttime)
print(endtime)

gatherRows(starttime, endtime)

'''print(sys.getsizeof(starttime))
print(sys.getsizeof(endtime))

<<<<<<< HEAD
myint = 12
print(sys.getsizeof(myint))'''

