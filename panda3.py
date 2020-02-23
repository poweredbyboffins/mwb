import psycopg2
import pandas as pd
import numpy as np
conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
#conn = psycopg2.connect(conn_string)
query="select hometeam,fthg from rescuttmp where matchdate > '31-dec-2015' and fthg is not null"
df=pd.read_sql_query(query, conn)
#pd.groupby(['hometeam']).sum('fthg').sort('one', ascending=False).head(10)
df2=df.groupby('hometeam').sum()
#print (df2)
df3=df2.sort_values(by='fthg',ascending=False).head(10)
print (df3)
conn.commit();
conn.close();
