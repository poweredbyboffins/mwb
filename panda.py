import psycopg2
import pandas as pd
import numpy as np
conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
#conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
cursor.execute("select matchdate,hometeam,ftr from rescuttmp")
rows=pd.DataFrame(cursor.fetchall(),columns=['matchdate','hometeam','ftr'])

for row in rows:
   print (row)
for ind, row in rows.iterrows(): 
    print(row.values)
conn.commit();
conn.close();
