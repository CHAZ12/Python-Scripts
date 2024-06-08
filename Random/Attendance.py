#!/usr/bin/env python3
import requests
import json

strCode = input("inter the code")
strDeviceId = "CRN-11678" # found in payload
strSelfID = "" # found in payload
url = "URL="+ strSelfID + "&" + "strDeviceID=" + strDeviceId+ "&" + "strCode=" + strCode
   
session = requests.Session()
# Get request DATA
resp1 = session.get(url)# login to Portal
print(resp1.text)
