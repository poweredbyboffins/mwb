import urllib.request as u
req = u.Request(url="http://127.0.0.1:8000/static/mwb/bccanv.html",headers={'User-Agent':' User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0 '})
handler = u.urlopen(req)
