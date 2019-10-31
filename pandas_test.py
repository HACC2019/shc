import pandas as pd
import MySQLdb

db = MySQLdb.connect(host="pf.parsl.dev", user="hacc", passwd="hacc2019")
df = pd.read_sql_query("select * from raw;", db)
cur = db.cursor()
print(cur.execute("SELECT Duration FROM raw"))
print(df)
