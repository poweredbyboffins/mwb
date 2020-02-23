import pandas as pd
from pandata import *
from pandcls import *

dir = "/home/andy/lit-basin-8962/mwb/static/mwb/"
dfh = pd.DataFrame()

qry = "select hometeam,fthg from rescuttmp where matchdate >= '31-aug-2015' and fthg is not null"
x = pandata(qry,dfh)
y=pander(x.dfh)
z=y.sumhome(x.dfh,'fthg')
m=y.mean(x.dfh,'fthg')
m.to_csv(dir+'besthome.tsv', sep='\t')


qry = "select hometeam,ftag from rescuttmp where matchdate >= '31-aug-2015' and fthg is not null"
x = pandata(qry,dfh)
y=pander(x.dfh)
z=y.sumhome(x.dfh,'ftag')
m=y.mean(x.dfh,'ftag')
m.columns = ['fthg']

#rm=y.movingAverage(x.dfh)
#print (rm)

j=y.json(z)
print(j)

m.to_csv(dir+'worsthome.tsv', sep='\t')

qry = "select matchdate,case ftr when 'H' then 3 when 'A' then 0 else 1 end fthr from rescuttmp where matchdate >= '31-aug-2015' and fthg is not null and hometeam='Liverpool'"
x = pandata(qry,dfh)
y=pander(x.dfh)
rm=y.movingAverage(x.dfh)
print(rm.size)
print(rm)
