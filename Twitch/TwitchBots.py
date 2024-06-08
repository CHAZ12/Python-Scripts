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

print("\n------ THIS IS A SCRIPT TO GET STREAMERS STATISTICS FROM TWITCH.TV -----")

import pytz


def print_stats(followers, twitchChatCount, Game, viewers, date, streamerName, moderators, users, vips):
    print("Streamer: " + str(streamerName))
    print("Viewers: " + str(viewers))
    print("Game: " + str(Game))
    print("Followers: " + str(followers))
    print("Chat Count: " + str(twitchChatCount))
    print("MODS In Chat: " + str(moderators))
    print("VIPS In Chat: " + str(vips))
    print("Users In Chat: " + str(users))

    with open("TwitchFile.txt", 'a+', encoding="utf-8") as chatFile:
        chatFile.write(date + "\n Name: " + streamerName + ", Game: " + str(game) + ", Viewers: " + str(
            viewers) + ", Followers: " + str(followers) + ", UsersInChat: " + str(twitchChatCount) + "\n")
        chatFile.close()


def post_request_func(streamerName):
    #  GET TWITCH.TV'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    global game, Viewers
    url = ('https://www.twitch.tv/' + streamerName)
    timeZ_Ce = pytz.timezone('US/Central')
    date = datetime.now(timeZ_Ce).strftime('%Y-%m-%d %H:%M:%S')
    isLive = False

    print('Fetching a valid url response state for: ' + 'https://www.twitch.tv/' + streamerName)
    homepage = requests.get(url).text

    if not homepage:
        print('User page not found. Moving on..')
    else:
        print('User page found. Continuing...')
        isLive = True
    if isLive:

        # Get Client ID just increase it changes
        print('Fetching Client ID')
        # client_id = re.search('"Client-ID" ?: ?"(.*?)"', homepage).group(1)
        client_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
        headers = {"Client-Id": client_id}  # get Local Client ID

        # Get FOLLOWERS
        query1 = 'query {user(login: "%s") { followers { totalCount } } }' % streamerName  # Query type
        data1 = json.dumps([{"query": query1}])

        # USERS IN CHAT
        query2 = 'query {user(login: "%s")  { channel { chatters  { count } } } }' % streamerName
        data2 = json.dumps([{"query": query2}])

        # Get is LIVE
        query3 = 'query {user(login: "%s") { stream { type } } } ' % streamerName
        data3 = json.dumps([{"query": query3}])

        # Get GAME name
        query4 = 'query {user(login: "%s") { stream { game  { name } } } } ' % streamerName
        data4 = json.dumps([{"query": query4}])

        #  Get VIEWERS count
        query5 = 'query {user(login: "%s") { stream { viewersCount } } } ' % streamerName
        data5 = json.dumps([{"query": query5}])

        # Get MODERATORS userNames from chat
        query6 = 'query {user(login: "%s")  { channel { chatters  { moderators { login { } } } } } }' % streamerName
        data6 = json.dumps([{"query": query6}])

        # Get all VIPS userNames from chat
        query7 = 'query {user(login: "%s")  { channel { chatters  { vips { login { } } } } } }' % streamerName
        data7 = json.dumps([{"query": query7}])

        # Get all USER userNames from chat
        query8 = 'query {user(login: "%s")  { channel { chatters  { viewers { login { } } } } } }' % streamerName
        data8 = json.dumps([{"query": query8}])

        #   Post Request DATA From Network Tab
        resp1 = requests.post("https://gql.twitch.tv/gql", data=data1, headers=headers)
        resp2 = requests.post("https://gql.twitch.tv/gql", data=data2, headers=headers)
        resp3 = requests.post("https://gql.twitch.tv/gql", data=data3, headers=headers)
        resp4 = requests.post("https://gql.twitch.tv/gql", data=data4, headers=headers)
        resp5 = requests.post("https://gql.twitch.tv/gql", data=data5, headers=headers)
        resp6 = requests.post("https://gql.twitch.tv/gql", data=data6, headers=headers)
        resp7 = requests.post("https://gql.twitch.tv/gql", data=data7, headers=headers)
        resp8 = requests.post("https://gql.twitch.tv/gql", data=data8, headers=headers)

        #   make sure I just output the value I want only
        followers = resp1.json()[0]["data"]["user"]["followers"]["totalCount"]
        twitchChatCount = resp2.json()[0]["data"]["user"]["channel"]["chatters"]["count"]
        live = resp3.json()[0]["data"]["user"]["stream"] or ["type"]
        moderatorsnames = resp6.json()[0]["data"]["user"]["channel"]["chatters"]["moderators"]
        vipsnames = resp7.json()[0]["data"]["user"]["channel"]["chatters"]["vips"]
        usernames = resp8.json()[0]["data"]["user"]["channel"]["chatters"]["viewers"]

        # Users
        usernames2 = re.findall(r"(?<='login':\s')(?:\w+)", str(usernames))
        usernames3 = re.sub(r"('(.*?)')|,\s", r'\2 ', str(usernames2))  # convert to one entire line you can ping in chat
        print(usernames3)
        # Moderators
        modnames = re.findall(r"(?<='login':\s')(?:\w+)", str(moderatorsnames))
        modnames3 = re.sub(r"('(.*?)')|,\s", r'\2 ', str(modnames))
        print(modnames3)

        # VIPS
        VIPSnames = re.findall(r"(?<='login':\s')(?:\w+)", str(vipsnames))
        VIPSnames3 = re.sub(r"('(.*?)')|,\s", r'\2 ', str(VIPSnames))
        print(VIPSnames3)
        # Write all statistics in a file
        with open("ChatFile.txt", 'a+', encoding="utf-8") as chatFile:
            chatFile.write("\n" + date + " " + streamerName + "\n USERS:" + str(usernames2) + "\n MODS: " + str(
                modnames) + "\n VIPS: " + str(VIPSnames) + "\n")
            chatFile.close()

        if not live == ['type']:  # make sure that game is not NONE
            game = resp4.json()[0]["data"]["user"]["stream"]["game"]["name"]  # Game
            Viewers = resp5.json()[0]["data"]["user"]["stream"]["viewersCount"]  # VIEWERS

        if live == ['type']:
            print('User is offline or does not exists. Moving on...')

        else:
            print('User is online')
            print_stats(followers, twitchChatCount, game, Viewers, date, streamerName, modnames, usernames2, VIPSnames)
            twitch_bots(usernames2, date, streamerName)


def twitch_bots(usernames2, date, streamerName):
    # Find Bots from twitch from a  specific list
    with open("BotFile.txt", 'a', encoding="utf-8") as BotFile:
        Usernames3 = re.sub(r",\s", r'|', str(usernames2))  # remove the space and comma
        Usernames3 = re.sub(r"\[|\]", '', Usernames3)  # replace brackets with nothing because findall looks weird
        BotList = open("BotList.txt", "r")
        lines = BotList.read()
        BotList.close()
        BotNames = re.findall(Usernames3, str(lines))
        BotFile.write(date + ": " + streamerName + "\n Bots:" + str(BotNames) + "\n")
        BotFile.close()
        print("Bots: " + str(BotNames))


with open("LogFile.txt", 'a+', encoding="utf-8") as LogFile:
    with open("Streamers.txt", 'r') as TxtFile:
        for line in TxtFile.readlines():
            streamerName = line.strip('\n')
            post_request_func(streamerName)
            time.sleep(1)
print('Finished')
exit()

# # EXTRAS: MODIFIED EXCEL CODE FROM: https://betterprogramming.pub/,
#   https://towardsdatascience.com/merging-spreadsheets-with-python-append-f6de2d02e3f3 # GET REQUESTS CODE FROM
#   https://docs.python-requests.org/en/master/user/quickstart/
#   https://www.gkbrk.com/2020/12/twitch-graphql/ # help Get post requests from twitch.tv
