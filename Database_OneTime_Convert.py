import MySQLdb
import backend

backend.add_column(db=backend.con,table='raw',column='Start_Time',data=backend.unix_ConvertStart(backend.con))
backend.add_column(db=backend.con,table='raw',column='End_Time',data=backend.unix_ConvertEnd(backend.con))

