import pandas as pd
import sqlite3

db = sqlite3.connect("shc.db")
df = pd.read_sql_query("select * from raw;", db)
print(db.execute("SELECT Duration FROM raw"))
print(df)

