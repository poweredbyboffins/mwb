import psycopg2
import pandas as pd
import numpy as np
conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
#conn = psycopg2.connect(conn_string)
query="select hometeam,fthg from rescuttmp where matchdate > '31-dec-2015'"
df=pd.read_sql_query(query, conn)
#pd.groupby(['hometeam']).sum('fthg').sort('one', ascending=False).head(10)
df['sum']=df.groupby('hometeam')['fthg'].transform(sum)
df3=df.sort(['sum'], ascending=False,axis=1).drop(['fthg'],axis=1).head(10)
print (df3)
conn.commit();
conn.close();
