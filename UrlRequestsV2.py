#!/usr/bin/env python3
import subprocess
import sys
import re
import time
from datetime import datetime
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

print("------ THIS IS A SCRIPT TO GET STREAMERS STATISTICS FROM TWITCH.TV -----")


#   GET READY TO GET STREAMER INFO FROM TWITCH USING REQUESTS_HTML

def render_func():
    # Get render Request fro streamer and Content
    from requests_html import HTMLSession
    session = HTMLSession()
    url = ('https://www.twitch.tv/' + streamerName)
    print('Fetching a valid url render response state for: ' + 'https://www.twitch.tv/' + streamerName)
    response = session.get(url)
    if not response.html.render(timeout=10, sleep=5):
        print('Render response is successful')
        body = response.html.find('body', first=True).text
        newTxt = body.split('Expand')[0]
        # print(newTxt)
        if re.search(r'(Sign\sUp\nLIVE)', str(newTxt)):
            print('User is online. Continuing...')
            regex_func(newTxt, url)
        else:
            print('User is offline or does not exists. Moving on')
            time.sleep(1)
    else:
        print('Request Failed, restarting...')
        time.sleep(1)


def regex_func(newTxt, url):
    #   Up to this point nothing is written yet, so it is safe to close the program.
    streamer = re.search(r'([^\s\n]*\n(?=Follow))', newTxt).group().strip()
    print("Streamer: " + streamer)
    viewers = re.search(r'([^\s]\S{0,10}\n(?=\d+:\d))', newTxt).group().strip()
    print("Viewers: " + viewers)
    game = re.search(r'(?<=Subscribe\n)(?:[^\n]*\n)([^\n]+)', newTxt).group(1).strip()
    print("Game: " + game)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_request_func(date, game, viewers, url)


def post_request_func(date, game, viewers, url):
    #  GET TWITCH'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    print('Fetching Client Id')
    homepage = requests.get(url).text
    client_id = re.search('"Client-ID" ?: ?"(.*?)"', homepage).group(1)

    #   Get Client Id and Streamer name
    headers = {"Client-Id": client_id}  # get Local Client Id

    #    FROM TWITCH REQUESTS GET HOW MANY FOLLOWERS DATA
    query1 = 'query {user(login: "%s") { followers { totalCount } } }' % streamerName  # Query type
    data1 = json.dumps([{"query": query1}])

    #    FROM TWITCH REQUESTS GET HOW MANY UserChat DATA
    query2 = 'query {user(login: "%s")  { channel { chatters  { count } } } }' % streamerName
    data2 = json.dumps([{"query": query2}])

    #   Post request DATA
    resp1 = requests.post("https://gql.twitch.tv/gql", data=data1, headers=headers)
    resp2 = requests.post("https://gql.twitch.tv/gql", data=data2, headers=headers)

    #   make sure I just display the value only
    followers = resp1.json()[0]["data"]["user"]["followers"]["totalCount"]
    twitchChatCount = resp2.json()[0]["data"]["user"]["channel"]["chatters"]["count"]  # includes the streamer in count

    print("Followers: " + str(followers))
    print("Users In Chat: " + str(twitchChatCount))
    create_excel_func(game, followers, viewers, date, twitchChatCount)


def create_excel_func(game, followers, viewers, date, twitchChatCount):
    #   GET READY TO CREATE OR OPEN A EXCEL FILE TO POST NEW INFORMATION
    File = open('bob', 'a+', encoding='utf-8')
    File.write(
        'TwitchName:{0}, Game:{1}, Followers:{2}, Viewers:{3}, Date & Time:{4}, Twitch\'s Users In Chat:{5}'
        '\n\n'.format(
            streamerName,
            game,
            followers,
            viewers,
            date,
            twitchChatCount)
    )
    File.close()
    workbook_name = 'OldTiwtch.xlsx'

    import pandas as pd
    from openpyxl.workbook import Workbook

    #   Create or open an Excel file to append gathered values
    headers = ['TwitchName', 'Game', 'Followers', 'Viewers', 'Date/time', 'Twitch\'s Users In Chat', 'my Users in Chat']
    wb = Workbook()
    page = wb.active
    page.title = 'Steamer_Statistics'
    page.append(headers)  # write the headers to the first line

    #   Data to write:
    statistics = [streamerName, game, followers, viewers, date, twitchChatCount]

    page.append(statistics)
    wb.save(filename=workbook_name)

    #   Append Old to New stuff
    old_file = pd.read_excel("OldTiwtch.xlsx")
    New_file = pd.read_excel("NewTwitch.xlsx")
    append_df = pd.concat([old_file, New_file])  # append old and statistics

    append_df.to_excel("NewTwitch.xlsx", index=False, sheet_name='Steamer_Statistics')
    print('Excel Complete')


with open("Streamers", 'r') as TxtFile:
    for line in TxtFile.readlines():
        streamerName = line.strip('\n')
        render_func()
print('Finished')
# # EXTRAS: MODIFIED EXCEL CODE FROM: https://betterprogramming.pub/,
#   https://towardsdatascience.com/merging-spreadsheets-with-python-append-f6de2d02e3f3 # GET REQUESTS CODE FROM
#   https://docs.python-requests.org/en/master/user/quickstart/
#   https://www.gkbrk.com/2020/12/twitch-graphql/ # help Get post requests from twitch.tv
