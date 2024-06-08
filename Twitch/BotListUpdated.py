# !/usr/bin/env python3
import subprocess
import sys
import re
import time
from datetime import datetime
import json

print('Getting or installing necessary modules')
#   Inorder for the script to run properly you need all modules below, so make sure they are installed
try:
    import pytz

    print('module pytz is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pytz'])

try:
    import requests_html

    print('module requests_html is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests_html'])
try:
    import requests

    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])

try:
    import pandas

    print('module pandas installed')
except ModuleNotFoundError:
    print('module pandas is not installed')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

print("\n------ THIS IS A SCRIPT TO GET LIST OF BOTS FROM SITE -----")

import pytz


def post_request_func(url):
    print('Fetching a valid url response state for: ' + 'https://twitchinsights.net/bots')
    homepage = requests.get(url).text
    isLive = False

    if not homepage:
        print('User page not found. Moving on..')
    else:
        print('User page found. Continuing...')
        isLive = True

    if isLive:
        # Get online Bots
        query1 = 'query { bots {  } } '  # Query type
        data1 = json.dumps([{"query": query1}])

        resp1 = requests.post("https://api.twitchinsights.net/v1/bots/all", data=data1)
        bots = str(resp1.json()['bots'])
        Usernames4 = re.findall(r"\w+?(?=')", bots)
        BotList = open("NewBotList.txt", "w+")
        Usernames3 = re.sub(r"\[|\]", '', str(Usernames4))  # replace brackets with nothing because findall looks weird
        Usernames4 = re.sub(r",\s", '\n', str(Usernames3))  # replace brackets with nothing because findall looks weird
        BotList.write(str(Usernames4))
        BotList.close()


post_request_func('https://twitchinsights.net/bots')

## Thanks for https://twitchinsights.net/bots the Bot list