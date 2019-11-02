#from UnixConverter import unix_Converter
#unix_Converter()
import MySQLdb
#import sqlite3

con = MySQLdb.connect(db="hacc",host="pf.parsl.dev", user="hacc", passwd="hacc2019")
#con = sqlite3.connect('shc.db')
cursorObj = con.cursor()

def findMaxTime(con):
    con.query("SELECT MIN([Start_Time]) FROM raw")
    maxTimeResult = con.store_result()
    maxTime = maxTimeResult.fetch_row(maxrows=0)
    return(maxTime)

def findMinTime(con):
    con.query("SELECT MAX([End_Time]) FROM raw")
    minTimeResult = con.store_result()
    minTime = minTimeResult.fetch_row(maxrows=0)
    return(minTime)

    '''max_time = cursorObj.execute("SELECT MAX([End_Time]) FROM raw")
    min_time =  cursorObj.execute("SELECT MIN([Start_Time]) FROM raw")'''
    print(minTime)
    print(maxTime)

def add_column(db, table, column, data, dtype="TEXT"):
    """Set a column equal to a list, creating the column if it doesn't exist"""

    # Sanity checks #
    if type(db) is not MySQLdb.connections.Connection:
        raise TypeError("Expected MySQLdb.connections.Connection, got {}".format(type(db)))
    if type(table) is not str:
        raise TypeError("Expected string, got {}".format(type(table)))
    if type(column) is not str:
        raise TypeError("Expected string, got {}".format(type(column)))
    if type(data) is not list:
        raise TypeError("Expected list, got {}".format(type(data)))

    con.autocommit(on=True)  # Make sure to actually save changes

    # Try to drop column if it exists #
    try:
        con.query("ALTER TABLE {} DROP COLUMN {}".format(table, column))
    except MySQLdb._exceptions.OperationalError:
        pass

    # Create column and add in data #
    con.query("ALTER TABLE {} ADD {} {}".format(table, column, dtype))
    i = 1
    for value in data:  # Replace every row with data starting at ID 1
        con.query("UPDATE {} SET {}={} WHERE ID={}".format(table, column, "'" + value + "'", i))
        i += 1