import pandas as pd
from pandata import *
from pandcls import *

dfh = pd.DataFrame()
dfh2 = pd.DataFrame()
dfh3 = pd.DataFrame()
dfh4 = pd.DataFrame()
dfh5 = pd.DataFrame()

qry="select row_number() OVER (ORDER BY greatest(result,result2) DESC) AS i, id,hometeam,awayteam,winprob,drawprob,loseprob,matchdate,pctwin,pctnotwin,homeformadj,awayformadj,commentary from predview"
x = pandata(qry,dfh)
y=pander(x.dfh)
for index, row in x.dfh.iterrows():
    #print(row['hometeam']+' '+row['awayteam'])

    qry = "select matchdate,case ftr when 'H' then 3 when 'A' then 0 else 1 end fthr from rescuttmp where matchdate >= '31-aug-2015' and fthg is not null and replace(lower(hometeam),' ','')='"+row['hometeam']+"'"
    x = pandata(qry,dfh)
    y=pander(x.dfh)
    rm=y.movingAverage(x.dfh)
    print(rm)

    away=row['awayteam']
    qry = "select matchdate,case ftr when 'H' then 0 when 'A' then 3 else 1 end fthr from rescuttmp where matchdate >= '31-aug-2015' and fthg is not null and replace(lower(awayteam),' ','')='"+row['awayteam']+"'"
    x = pandata(qry,dfh)
    y=pander(x.dfh)
    rm=y.movingAverage(x.dfh)
    dfh3=rm.to_frame()
    dfh3[away]=dfh3.index
    #dfh3=dfh3.pivot(dfh3.index,'awayteam')
    dfh3=dfh3.T
    #print(dfh3)
    #print(rm)
    dfh2=row.append(dfh3)
    #print(dfh2)
#dfh5=pd.concat([dfh2,dfh4])
#j=dfh4.to_json
#print(dfh2)

