#!/usr/bin/env python3
import subprocess
import sys
import re
import time
from datetime import datetime
import json
import pytz

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

try:
    import pandas

    print('module pandas installed')
except ModuleNotFoundError:
    print('module pandas is not installed')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

try:
    import xlsxwriter

    print('module xlsxwriter installed')
except ModuleNotFoundError:
    print('module xlsxwriter is not installed')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'xlsxwriter'])

try:
    import xlrd

    print('module xlrd installed')
except ModuleNotFoundError:
    print('module xlrd is not installed')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'xlrd'])

try:
    import openpyxl

    print('module openpyxl installed')
except ModuleNotFoundError:
    print('module openpyxl is not installed')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])

print("\n------ THIS IS A SCRIPT TO GET STREAMERS STATISTICS FROM TWITCH.TV -----")


def print_stats(followers, twitchChatCount, Game, viewers, date):
    print("Streamer: " + str(streamerName))
    LogFile.write("\nStreamer: " + str(streamerName))
    print("Viewers: " + str(viewers))
    LogFile.write("\nViewers: " + str(viewers))
    print("Game: " + str(Game))
    LogFile.write("\nGame: " + str(Game))
    print("Followers: " + str(followers))
    LogFile.write("\nFollowers: " + str(followers))
    print("Users In Chat: " + str(twitchChatCount))
    LogFile.write("\nUsers In Chat: " + str(twitchChatCount))
    create_excel_func(Game, followers, viewers, date, twitchChatCount)


def post_request_func():
    #  GET TWITCH'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    global game, Viewers
    url = ('https://www.twitch.tv/' + streamerName)
    timeZ_Ce = pytz.timezone('US/Central')
    date = datetime.now(timeZ_Ce).strftime('%Y-%m-%d %H:%M:%S')
    isLive = False

    print('Fetching a valid url response state for: ' + 'https://www.twitch.tv/' + streamerName)
    LogFile.write(
        "\nTime:" + date + ', Fetching a valid url response state for: ' + 'https://www.twitch.tv/' + streamerName)
    homepage = requests.get(url).text
    if not homepage:
        print('User page not found. Moving on..')
        LogFile.write('\nUser page not found. Moving on...')
    else:
        print('User page found. Continuing...')
        LogFile.write('\nUser page found. Continuing...')
        isLive = True

    if isLive:
        # Get Client Id just increase it changes
        print('Fetching Client Id')
        LogFile.write('\nFetching Client Id')
        client_id = re.search('"Client-ID" ?: ?"(.*?)"', homepage).group(1)
        headers = {"Client-Id": client_id}  # get Local Client Id

        # From Twitch Get FOLLOWERS
        query1 = 'query {user(login: "%s") { followers { totalCount } } }' % streamerName  # Query type
        data1 = json.dumps([{"query": query1}])

        # From twitch is USERS IN CHAT
        query2 = 'query {user(login: "%s")  { channel { chatters  { count } } } }' % streamerName
        data2 = json.dumps([{"query": query2}])

        # From Tiwtch Get is LIVE
        query3 = 'query {user(login: "%s") { stream { type } } } ' % streamerName
        data3 = json.dumps([{"query": query3}])

        # From Twitch get GAME name
        query4 = 'query {user(login: "%s") { stream { game  { name } } } } ' % streamerName
        data4 = json.dumps([{"query": query4}])

        # From Twitch get VIEWERS
        query5 = 'query {user(login: "%s") { stream { viewersCount } } } ' % streamerName
        data5 = json.dumps([{"query": query5}])

        #   Post request DATA
        resp1 = requests.post("https://gql.twitch.tv/gql", data=data1, headers=headers)
        resp2 = requests.post("https://gql.twitch.tv/gql", data=data2, headers=headers)
        resp3 = requests.post("https://gql.twitch.tv/gql", data=data3, headers=headers)
        resp4 = requests.post("https://gql.twitch.tv/gql", data=data4, headers=headers)
        resp5 = requests.post("https://gql.twitch.tv/gql", data=data5, headers=headers)

        #   make sure I just output the value I want only
        followers = resp1.json()[0]["data"]["user"]["followers"]["totalCount"]
        twitchChatCount = resp2.json()[0]["data"]["user"]["channel"]["chatters"]["count"]
        live = resp3.json()[0]["data"]["user"]["stream"] or ["type"]

        if not live == ['type']:  # make sure that game is not NONE
            game = resp4.json()[0]["data"]["user"]["stream"]["game"]["name"]  # Game name
            Viewers = resp5.json()[0]["data"]["user"]["stream"]["viewersCount"]  # VIEWERS

        if live == ['type']:
            print('User is offline or does not exists. Moving on...')
            LogFile.write('\nUser is offline or does not exists. Moving on...')
        else:
            print('User is online')
            LogFile.write('\nUser is offline or does not exists. Moving on...')
            print_stats(followers, twitchChatCount, game, Viewers, date)


def create_excel_func(Game, followers, viewers, date, twitchChatCount):
    #   GET READY TO CREATE OR OPEN A EXCEL FILE TO POST NEW INFORMATION
    print('Creating Excel data')
    LogFile.write('\nCreating excel data')
    time.sleep(1)
    File = open('bob.txt', 'a+', encoding='utf-8')
    File.write(
        'TwitchName:{0}, Game:{1}, Followers:{2}, Viewers:{3}, Date & Time CDT:{4}, Twitch\'s Users In Chat:{5}'
        '\n\n'.format(
            streamerName,
            Game,
            followers,
            viewers,
            date,
            twitchChatCount)
    )
    File.close()
    workbook_name = 'OldTiwtch.xlsx'

    import pandas as pd
    from openpyxl.workbook import Workbook

    #   Create a simple log file of statistic value(s)
    headers = ['TwitchName', 'Game', 'Followers', 'Viewers', 'Date & time CDT', 'Twitch\'s Users In Chat']
    wb = Workbook()
    page = wb.active
    page.title = 'Steamer_Statistics'
    page.append(headers)  # write the headers to the first line
    nameExcel = streamerName + ".xlsx"
    statistics = [streamerName, Game, followers, viewers, date, twitchChatCount]
    
    #   Create or open Excel file by stramer name to append gathered values
    # Create Excel file by stramer name for Current statistic values
    page.append(statistics)
    wb.save(filename=workbook_name)

    # Create an excel file for Older statistic values excel file(s) if needed
    try:
        open(nameExcel)  #try to open an excel file by streamer name
        pass
    except IOError:
        print('Created new excel file for streamer:' + streamerName)
        wb2 = Workbook()
        page = wb2.active
        page.title = streamerName + '_Statistics'
        wb2.save(filename=nameExcel)

    #   Append Old to New stuff excel files
    old_file = pd.read_excel("OldTiwtch.xlsx")
    New_file = pd.read_excel(nameExcel)
    append_df = pd.concat([old_file, New_file])  # append old and statistics

    append_df.to_excel(nameExcel, index=False, sheet_name=streamerName + '_Statistics')
    print('Excel Complete')
    LogFile.write('\nExcel Complete')


with open("LogFile.txt", 'a+', encoding="utf-8") as LogFile:
    with open("Streamers.txt", 'r') as TxtFile:
        for line in TxtFile.readlines():
            streamerName = line.strip('\n')
            post_request_func()
            time.sleep(1)

    LogFile.write('\n------------------Finished------------------)
    LogFile.close()

print('Finished')
exit()

# # EXTRAS: MODIFIED EXCEL CODE FROM: https://betterprogramming.pub/,
#   https://towardsdatascience.com/merging-spreadsheets-with-python-append-f6de2d02e3f3 # GET REQUESTS CODE FROM
#   https://docs.python-requests.org/en/master/user/quickstart/
#   https://www.gkbrk.com/2020/12/twitch-graphql/ # help Get post requests from twitch.tv
