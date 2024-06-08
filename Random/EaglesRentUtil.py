#!/usr/bin/env python3
import requests
import json

def post_request_func():
    global headers1
    #need to login to get token
    token = ''
    
    headers1 = { 
         'Content-Type': 'text/html; charset=UTF-8', 
         #'Transfer-Encoding': 'chunked', 
         'Connection': 'keep-alive', 
               'Vary': 'Accept-Encoding', 
               'X-Cnection': 'close', 
               'authorization':token,
               'authority':'eagleslandingnew.residentportal.com',
               #'path':'/api/?controller=ledger&action=getLedgerWithSettings',
               }
    Query()
        
def Query():
    session = requests.Session()
    # Query parmas
    queryString1 = {"controller":"user",
                   "action":"login"} # query parmas for login
    queryString2 = {"controller":"ledger",
                   "action":"getLedgerWithSettings"} # Query for ledger
    
    #payloads
    payload1 = {'password': 'Eagleslanding.com123!', #payload for login
               'username':'zpmass@gmail.com'}
    #queryDumps
    query2 = 'query {}'  # Query type
    data2 = json.dumps([{"query": query2}])
    
    # Get request DATA
    resp1 = session.get("https://eagleslandingnew.residentportal.com/api/?controller=user&action=login", data=payload1, params=queryString1)# login to Portal
    resp2 = session.get("https://eagleslandingnew.residentportal.com/api/?controller=ledger&action=getLedgerWithSettings",params=queryString2, data=data2,headers=headers1 ) # get Ledger Data
    #print(resp2.json()["ledger"])
    for i in range(len(resp2.json()["ledger"])):
        date = resp2.json()["ledger"][i]["date"]
        label = resp2.json()["ledger"][i]["label"]
        Uamount = resp2.json()["ledger"][i]["amount"]
        if label == "Utilities" or label == "Rent":
            print(str(date) + ": "+ str(label) +"-$" + str(Uamount))
            w = open("EaglesLanding.txt","a+", encoding='utf-8')
            w.write(str(date) + ": "+ str(label) +"-$" + str(Uamount) +"\n")
post_request_func()

# Nework Reference For Ledger
'''
{
  "ledger": [
    {
      "id": 862946028,
      "amount": 585.45,
      "customer_id": 16609578,
      "type": "Payment",
      "transaction_type": 1,
      "fee_amount": 0,
      "balance": 0,
      "date": "2023-03-04T15:40:40-06:00",
      "label": "Payment - eCheck 8284",
      "description": "You",
      "status_type_id": 10,
      "status": " Captured",
      "is_negative_balance": false,
      "taxes": [],
      "created_by_name": "Zachary Massey",
      "customer_invoice_id": 0,
      "document_id": 0
    },
  ],
  "scheduled_charges": [
    {
      "amount": "545",
      "date": "2023-04-01T00:00:00-05:00",
      "label": "Rent",
      "frequency_code": "monthly",
      "taxes": []
    },
    {
      "amount": 11.95,
      "date": "2023-04-01T00:00:00-05:00",
      "label": "Additional Rent  Mitigated Risk",
      "frequency_code": "monthly",
      "taxes": []
    }
  ],
  "settings": {
    "tax_exclusive": true,
    "display_ledger_by": "Charges"
  }
}












'''
