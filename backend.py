import MySQLdb


def add_column(db, table, column, data, dtype="TEXT"):
    """Set a column equal to a list, creating the column if it doesn't exist"""

    # Sanity checks #
    if type(db) is not MySQLdb.connections.dbnection:
        raise TypeError("Expected MySQLdb.connections.connection, got {}".format(type(db)))
    if type(table) is not str:
        raise TypeError("Expected string, got {}".format(type(table)))
    if type(column) is not str:
        raise TypeError("Expected string, got {}".format(type(column)))
    if type(data) is not list:
        raise TypeError("Expected list, got {}".format(type(data)))

    db.autocommit(on=True)  # Make sure to actually save changes

    # Try to drop column if it exists #
    try:
        db.query("ALTER TABLE {} DROP COLUMN {}".format(table, column))
    except MySQLdb._exceptions.OperationalError:
        pass

    # Find max row num to know when to stop updating and start inserting #
    cur = db.cursor()
    cur.execute("SELECT MAX(ID) FROM {}".format(table))
    maxindex = cur.fetchall()

    # Create column and add in data #
    db.query("ALTER TABLE {} ADD {} {}".format(table, column, dtype))
    i = 1
    for value in data:  # Replace every row with data starting at ID 1
        if i <= maxindex[0][0]:  # Update if row exists
            db.query("UPDATE {} SET {}='{}' WHERE ID={}".format(table, column, value, i))
        if i > maxindex[0][0]:  # Insert if row doesn't exist
            db.query("INSERT INTO {} ({}) VALUES ('{}')".format(table, column, value))
        i += 1
