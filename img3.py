import urllib.request as u
req = u.Request(url="http://127.0.0.1:8000/static/mwb/bccanv.html",headers={ 'Content-Disposition': 'filename="picture.png"'})
handler = u.urlopen(req)
