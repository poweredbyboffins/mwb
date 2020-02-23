#select hometeam,homeformadj from gamepred where active_ind='Y' and homeformadj is not null order by homeformadj desc limit 5;
import urllib.request as url
#img=urllib.request.urlopen("http://127.0.0.1:8000/static/mwb/bccanv.html")
url.urlretrieve("http://127.0.0.1:8000/static/mwb/bccanv.html","img.png")
str="http://127.0.0.1:8000/static/mwb/bccanv.html"
try:
    response = url.urlopen(str)
    response.geturl()
except URLError as e:
    if hasattr(e, 'reason'):
        print ('We failed to reach a server.')
        print ('Reason: ', e.reason)
    elif hasattr(e, 'code'):
        print ('The server couldn\'t fulfill the request.')
        print ('Error code: ', e.code)
else:
    # everything is fine
    print ('OK')
