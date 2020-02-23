import psycopg2
import pandas as pd
import numpy as np

class pandata:

    def __init__(self, query,dfh):
        self.query = query
        
# get data
# connects
# queries and define data frame
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
        #conn = psycopg2.connect(conn_string)
        #query="select hometeam,fthg,awayteam,ftag from rescuttmp where matchdate > '31-aug-2015' and fthg is not null"
        #self.query="select hometeam,fthg from rescuttmp where matchdate > '31-aug-2015' and fthg is not null"
        dfh=pd.read_sql_query(self.query, conn)
        conn.commit();
        conn.close();
        self.dfh=dfh;
    
