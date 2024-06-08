# !/usr/bin/env python3

import sys
import re
import subprocess
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


def GetNickName():
    # Get Username from chat
    botChatFile = open("BotChatLog.txt", "r").read()  # Chat FILE Log
    # find the line for !nickname for username
    result = re.findall(r"(?:007dca6b-2343-43e5-85e9-ac8b2deb08e3.*)(?=!nickname)(.\w+\s){2}", str(botChatFile))
    if result:  # Make sure user enters a username
        user = "'" + result[-1].strip("@ ").lower() + "'"  # add missing quotations so it matches list lowercase
        print(user + " :User")
        VerifyUser(user.strip("'"))
        FoundNickname(user, botChatFile)
    else:
        print("Please Follow the format: !nickname user nickname 1")
    return


def FoundNickname(user, botChatFile):
    # Get users nickname and compare
    if not VerifyUser.verify:
        print('User does not exist')
        chatNamesFile = open("ChatNamesLog.txt", "r").read()  # Users in chat
        getUsers = re.findall(r"'(.*?)'", str(chatNamesFile), re.MULTILINE)  # retrieve just the usernames
        found = re.findall(str(user), str(getUsers), re.MULTILINE)  # Check to see if entered username is valid
    else:
        found = True
    nickname = re.findall(r"(?:007dca6b-2343-43e5-85e9-ac8b2deb08e3.*)(?=!nickname)(.\w+\s){3}", str(botChatFile))
    if found and nickname:  # Make sure user enters a nickname
        nickname = nickname[-1].strip()
        print(nickname + " :chosen nickname")
        if not nickname:  # make sure user put in a nickname
            print("please follow the layout as !nickname user nickname 2")
            return
        else:
            nicknamesFile = open("ChatNicknames.txt", 'r+')  # Find if user has already a nickname
            nicknamesRead = nicknamesFile.read()
            nicknamesFile.close()
            # pattern = user + ",\w+"
            find = str(re.findall(user + ",\w+", str(nicknamesRead))).strip("[]\"")
            print(find + ":find")
            userNickname = user + "," + nickname  # strip any white space
            if find:
                print(find + ' :replace x1')
                replace = nicknamesRead.replace(find, str(userNickname))  # replace new old w/ new nickname or add file
                print(replace + ' :replaced x2')
                with open("ChatNicknames.txt", 'w') as nw:
                    print('wrote file')
                    nw.write(replace)
            else:
                print('no match, new user nickname created')
                with open("ChatNicknames.txt", 'a') as na:
                    na.write(userNickname + "\n")
                print('append file')
    else:
        print("No valid user or nickname")
        return


def VerifyUser(streamerName):
    #  GET TWITCH.TV'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    url = ('https://www.twitch.tv/' + streamerName)
    print('Fetching a valid url response state for: ' + 'https://www.twitch.tv/' + streamerName)
    homepage = requests.get(url).text  # make sure your connected to internet

    if homepage:
        print('User page found. Continuing...')
        isLive = True
        if isLive:
            # Get Client ID just increase it changes
            # client_id = re.search('"Client-ID" ?: ?"(.*?)"', homepage).group(1)
            client_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
            headers = {"Client-Id": client_id}  # get Local Client ID

            # Get FOLLOWERS
            query = 'query {user(login: "%s") { followers { totalCount } } }' % streamerName  # Query type
            data = json.dumps([{"query": query}])

            # Post Request DATA From Network Tab
            resp = requests.post("https://gql.twitch.tv/gql", data=data, headers=headers)

            if resp.json()[0]["data"]["user"]:  # make sure user is not NONE
                VerifyUser.verify = True  # User exists
                return

    VerifyUser.verify = False
    return

GetNickName()
