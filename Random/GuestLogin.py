import requests
connected = False
url2 = "/reg.php"
url = "/reg.php?ah_goal=index.html&ah_login=true&url=E2B8F3578D88E9E37BDEBB16D6D912CC8C7A5085533388E08E76"
try:
    r = requests.get(url, timeout = 3)
    connected = True
except requests.exceptions.Timeout:
    print("The request timed out")

headers = {
        "cache-Control": "max-age=0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "connection": "keep-alive",
        "Server":"Hiawatha v9.6",
        "transfer-encoding": "chunked",
        "x-frame-options": "sameorigin",
        "Host": "198.18.34.1",
        "origin":"http://198.18.34.1",
        "referer": "http://198.18.34.1/reg.php?ah_goal=index.html&ah_login=true&url=E2B8F3578D88E9E37BDEBB16D6D912CC8C7A50",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57"
        
        }

params = {  "url":"E2B8F3578D88E9E37BDEBB16D6D912CC8C7A41", 
            "field1": "a@a.com",
            "field2": "a@a.com",
            "field3": "a@a.com",
            "phoneNumber":"",
            "opt_field": "1",
            "field4": "a@a.com", 
            "opt_field2":"",
            "checkbox":"checkbox"
           }
  
if connected:
    try:
        p = requests.post(url, data = params)
        connected = True
        print(p)
    except:
        print("Can not Post")
