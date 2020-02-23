import psycopg2
import pandas as pd
import numpy as np
conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
#conn = psycopg2.connect(conn_string)
query="select hometeam,fthg from rescuttmp where matchdate > '31-aug-2015' and fthg is not null"
dfh=pd.read_sql_query(query, conn)
query="select awayteam,fthg from rescuttmp where matchdate > '31-aug-2015' and fthg is not null"
dfa=pd.read_sql_query(query, conn)
# rename columns`
dfa.columns = ['hometeam','fthg']
frames=[dfh,dfa]
df3=pd.concat(frames)
df4=df3.groupby('hometeam').sum()
df5=df4.sort_values(by='fthg',ascending=False).head(10)
print (df5)
df6=df3.groupby('hometeam').mean()
df7=df6.sort_values(by='fthg',ascending=False).head(10)
print (df7)
conn.commit();
conn.close();
