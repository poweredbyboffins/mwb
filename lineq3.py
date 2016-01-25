import numpy as np
from scipy.linalg import *
import psycopg2
def callproc(data,type):
    try:
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
    except:
        print "I am unable to connect to the database"

    ld=data.tolist()

    cur=conn.cursor()

    cur.execute('select checkres(%s::numeric[],%s::varchar)',[data[0:4,0].astype(float).tolist(),type])

    conn.commit()

    cur.close()


def getdata(sql,type):
    try:
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
    except:
        print "I am unable to connect to the database"

    cur=conn.cursor()


    cur.execute(sql)
    results = list(cur)
    r1 = np.array(results)
    conn.commit()
    cur.close()

    
    cur=conn.cursor()

    sql='select case ftr when \'H\' then 100 when \'A\' then 100 when \'D\' then 0 end \
        from traingamepred where type=\''+type+'\''

    cur.execute(sql)

    elem = []
    for result in cur.fetchall():
        elem.append(result)
        
    conn.commit()
    cur.close()
    conn.close()

    r2=np.array(elem)
    X=np.linalg.lstsq(r1,r2)
    print X[0]
    return X[0]

print "Big home win"
sql="select round(homeformadj,2) hf ,awayformadj\
        ,winprob,loseconc from traingamepred where type='BH'"
arr1=getdata(sql,'BH')
callproc(arr1,'BH')


print "Big away win"
sql="select round(awayformadj,2) af ,homeformadj \
        ,loseprob,winconc from traingamepred where type='BA'"
arr2=getdata(sql,'BA')
callproc(arr2,'BA')

print "Shock"
sql="select round(awayformadj,2) af ,homeformadj \
        ,loseprob,winconc from traingamepred where type='S'"
arr2=getdata(sql,'S')
callproc(arr2,'S')

