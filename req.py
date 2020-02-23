import requests
#from PIL import Image
#from StringIO import StringIO

r = requests.get('http://127.0.0.1:8000/static/mwb/bcc2.html')
#print (r.status_code)
print (r.content)
#i = Image.open(StringIO(r.content))
