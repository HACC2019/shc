import MySQLdb
con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
cursorObj = con.cursor()

#given start + end time, find values between it, find avg
#select avg kwh from raw where timestamp is less than or greater than __

def sql_data_averages(starttime, endtime):
    con.query('SELECT Start_Time FROM raw WHERE Start_Time BETWEEN starttime AND endtime ')
    TotalTimeResult = con.store_result()




