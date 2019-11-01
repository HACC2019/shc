import UnixConverter
import MySQLdb
import backend

con = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019", db='hacc')
#con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

UnixConverter.unix_Converter()
backend.add_column(db=con,table='raw',column='Start_Time',data=UnixConverter.StartListInt)
backend.add_column(db=con,table='raw',column='End_Time',data=UnixConverter.EndListInt)
