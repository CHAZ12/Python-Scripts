import requests 
from bs4 import BeautifulSoup
import json
import re
import os
YT_URL= os.getenv('YT_URL')
print(f"YOUTUBE URL: {YT_URL}")
def getYTPoll():
    bob = "https://studio.youtube.com/live_chat?continuation=0ofMyANfGkJDaWtxSndvWVZVTTVSMnBtTFdReVNURjRiVWsxUmxCelNFNWxibXRuRWdzdE5IYzVXbTh0VVVGTlFTQU1NQUElM0QwAYIBBggEGAIgAIgBAaABv_SA9IG1hwOoAQA%253D"
    headers = {  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(bob, headers=headers)
    choices = []
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        #print(soup)
        title = re.findall(r'(?<="pollQuestion":{"runs":\[{"text":")([^"]+)',str(soup.contents))
        #print(title)
        for i in range(len(re.findall(r'(([^"]+)(?="}]},"selected":false))',str(soup.contents)))):
            pollchoice1 = re.findall(r'(([^"]+)(?="}]},"selected":false))',str(soup.contents))[i]
            #print(pollchoice1[0])
            choices.append(pollchoice1[0])
        print('Retrieved YT data')
        choices = [{"title": choice} for choice in choices if choice is not None]
        print(choices)
        if choices == []:
            print('User is not live.')
            return None, None
        return str(title).strip("[]") ,choices
    else:
        print('Failed to retrieve data')
        return None, None
getYTPoll()