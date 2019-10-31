import MySQLdb

con = MySQLdb.connect(db="hacc", host="pf.parsl.dev", user="hacc", passwd="hacc2019")


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

    # Find max row num to know when to stop updating and start inserting
    maxindex = con.query("SELECT MAX(ID) FROM {}".format(table))

    # Create column and add in data #
    con.query("ALTER TABLE {} ADD {} {}".format(table, column, dtype))
    i = 1
    for value in data:  # Replace every row with data starting at ID 1
        if i <= maxindex
            con.query("UPDATE {} SET {}='{}' WHERE ID={}".format(table, column, value, i))
        if i > maxindex:
            con.query("INSERT INTO {} ({}) VALUES ('{}')".format(table, column, value))
        i += 1
