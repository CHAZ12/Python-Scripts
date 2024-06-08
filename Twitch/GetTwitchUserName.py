# !/usr/bin/env python3
import subprocess
import sys
import json

print('Getting or installing necessary modules')
#   Inorder for the script to run properly you need all modules below, so make sure they are installed
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

print("\n------ THIS IS A SCRIPT TO GET USERNAME FROM TWITCH.TV-----")
def post_request_func(streamerName):
    #  GET TWITCH.TV'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    url = ('https://www.twitch.tv/' + streamerName)
    print('Fetching a valid url response state for: ' + 'https://www.twitch.tv/' + streamerName)
    homepage = requests.get(url).text  # make sure your connected to internet

    if not homepage:
        print('User page not found. Moving on..')
    else:
        print('User page found. Continuing...')
        isLive = True
        if isLive:
            # Get Client ID just increase it changes
            print('Fetching Client ID')

            client_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
            headers = {"Client-Id": client_id}  # get Local Client ID

            # Get FOLLOWERS
            query = 'query {user(login: "%s") { followers { totalCount } } }' % streamerName  # Query type
            data = json.dumps([{"query": query}])

            # Post Request DATA From Network Tab
            resp = requests.post("https://gql.twitch.tv/gql", data=data, headers=headers)

            if resp.json()[0]["data"]["user"]:  # make sure user is not NONE
                print("passed")
            else:
                print("failed")


post_request_func('tevin_vrrrr')
# # EXTRAS: MODIFIED EXCEL CODE FROM: https://betterprogramming.pub/,
#   https://towardsdatascience.com/merging-spreadsheets-with-python-append-f6de2d02e3f3 # GET REQUESTS CODE FROM
#   https://docs.python-requests.org/en/master/user/quickstart/
#   https://www.gkbrk.com/2020/12/twitch-graphql/ # help Get post requests from twitch.tv
