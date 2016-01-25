import numpy as np
from scipy.linalg import *
import psycopg2

def le_solve():
    ar = np.array ([[0.6,0,0.5661,0.2234,0.1975]
,[0,0.9,0.5486,0.2791,0.1693]
,[0,-0.47,0.1104,0.1614,0.6859]
,[0.14,0,0.5598,0.214,0.2082]
#,[0.33,3,0.5492,0.3006,0.1484]
,[0,-0.2,0.532,0.1617,0.7635]]);

    #print ar

    P,L,U = lu(ar)

    #v= array ([3,3,2,1,2]);
    v= np.array ([3,3,2,1,3]);

    s = solve(ar,np.transpose(v))
    print s

    X=np.linalg.lstsq(ar,v)
    print X[0]

#le_solve()
def callproc(data):
    try:
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
    except:
        print "I am unable to connect to the database"

    ld=data.tolist()

    cur=conn.cursor()
    
    #sql='select checkres(%s)
    #cur.execute('select checkres(%s)',[str(data[0:3,0].astype(float).tolist())[1:-1]])
    cur.execute('select checkres(%s::numeric[])',[data[0:3,0].astype(float).tolist()])
    #cur.mogrify('select checkres(%s)',{[data[0:3,0].astype(float).tolist()]})
    conn.commit()
    
    cur.close()

def getdata(sql):
    try:
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
    except:
        print "I am unable to connect to the database"

    cur=conn.cursor()

    #sql='select round(homeformadj,2) hf,round(awayformadj,2) af \
    #    ,winprob from traingamepred'

    cur.execute(sql)
    results = list(cur)
    #r1 = np.core.records.array(results, names='hf, af, win,draw,lose') 
    r1 = np.array(results)
    conn.commit()
    cur.close()

    
    cur=conn.cursor()

    sql='select case ftr when \'H\' then 0 when \'A\' then 5 when \'D\' then 0 end \
        from traingamepred'

    cur.execute(sql)
    #results = list(cur)
    #r2 = np.core.records.array(results, names='results') 
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

sql='select round(homeformadj,2) hf,round(awayformadj,2) af \
        ,winprob from traingamepred'
arr1=getdata(sql)
callproc(arr1)
#sql='select pctwin,winprob from traingamepred'
#getdata(sql)
sql='select round(homeformadj,2) hf,round(awayformadj,2) af \
        ,loseprob from traingamepred'
arr2=getdata(sql)
