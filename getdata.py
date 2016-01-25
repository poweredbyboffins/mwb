import csv
import urllib2

leagues = ('E0','E1','E2','E3')

for i,val in enumerate(leagues):
    url = 'http://www.football-data.co.uk/mmz4281/1516/'+val+'.csv'
    response = urllib2.urlopen(url)
    cr = response.read()
    # Save the string to a file
    csvstr = str(cr).strip("b'")

    lines = csvstr.split("\\n")
    fname="1516"+val+".csv"
    f = open(fname, "wb")
    for line in lines:
        f.write(line + "\n")
    f.close()
