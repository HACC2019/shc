import sqlite3


def add_column(db, table, column, data):
    """Set a column equal to a list, creating the column if it doesn't exist"""

    # Sanity Checks #
    if type(db) is not sqlite3.Connection:
        raise TypeError("Expected sqlite3.Connection, got {}".format(type(db)))
    if type(table) is not str:
        raise TypeError("Expected string, got {}".format(type(table)))
    if type(column) is not str:
        raise TypeError("Expected string, got {}".format(type(column)))
    if type(data) is not list:
        raise TypeError("Expected list, got {}".format(type(data)))
