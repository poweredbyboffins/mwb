#!/usr/bin/env python
 
import requests
 
#openssl x509 -x509toreq -in certificate.crt -out CSR.csr -signkey privateKey.key
 
 
payload = 'username=andybenson1964&password=atb100364'
headers = {'X-Application': 'SomeKey', 'Content-Type': 'application/x-www-form-urlencoded'}
 
resp = requests.post('https://identitysso.betfair.com/api/certlogin', data=payload, cert=('client-2048.crt', 'client-2048.key'), headers=headers)
 
if resp.status_code == 200:
  resp_json = resp.json()
  print resp_json['loginStatus']
  print resp_json['sessionToken']
else:
  print "Request failed."
