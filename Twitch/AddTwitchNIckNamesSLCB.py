# !/usr/bin/env python3

import sys
import re
import subprocess
import json


try:
    import requests_html

    print('module requests_html is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'iuests_html'])
try:
    import requests

    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])
print('Getting or installing necessary modules')nstall', 'req


#   Inorder for the script to run properly you need all modules below, so make sure they are installed


def post_request_func(streamerName):
    #  GET TWITCH.TV'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    url = ('C:/Users/BillyBOB/Desktop/Gethtml/index.html')
    print('Fetching a valid url response state for: ' + url)
    homepage = requests.get(url, data={'key': 'value'})  # make sure your connected to internet
    print(homepage)


post_request_func('tevin_vrrrr')
