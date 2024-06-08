# !/usr/bin/env python3
# ---------------------------
#   Import Libraries
# ---------------------------
import os
import sys
import json
import re
from datetime import datetime
import clr

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings



# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = "NicknamesScript"
Website = "https://www.streamlabs.com"
Description = "Get and Set TWITCH.TV USER Nicknames scipt"
Creator = "KllerRain"
Version = "1.0.6.0"
Command = "!nickname"
# ---------------------------
#   Define Global Variables
# ---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()
## my public vars
global GameState
GameState = False
global CurrentlyRunning
CurrentlyRunning = ""
# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    UpdateModerators()
    return

# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
#data.RawData.split("name=")[1].split(";")[0] == "StreamElements": # What did streamelements say
def Execute(data):
    if not data.IsChatMessage() or not data.IsFromTwitch():
        return
    if "!nickname" in data.Message.lower():
        SetNickName(data)

    if "!getnickname" in data.Message.lower():
        user = "'" + data.User.lower() + "'"
        nickname = ""
        userName = data.GetParam(1).strip("@")
        if userName == data.GetParam(1).strip("@"):
            Send_Message(userName)
            user = "'" + str(data.GetParam(1).strip("@")) + "'"
    GetNickName(data, user, nickname)

    if "!getrequest" in data.Message.lower():
        streamName = data.GetParam(1).strip("@")
        if streamName:
            VerifyUser(streamName)
        else:
            Send_Message('Enter a valid Streamer')
            return


   # ReadFile()
    return

# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return


# ---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
# ---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString


# ---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return


# ---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
# ---------------------------
def Unload():
    Send_Message(' {0} script reloaded'.format(ScriptName))
    return


# ---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
# ---------------------------
def ScriptToggled(state):
    return


def Send_Message(message):
    Parent.SendStreamMessage(str(message))
    return


def GetDateTime():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


def UpdateModerators(): # update moderators list for file
    Send_Message('/mods')
    m = open("Services\Twitch\Logs\BotChatLog.txt", "r+")
    read = m.read()
    moderators= re.findall(r"(?<=are:)(?:\s.+)", str(read), re.MULTILINE)[-1]
    m.close()
    Send_Message('Please welcome our helper(s): %s' % moderators)
    return


def GetBadgeInfo(data):
    badges = data.RawData.split("badges=")[1].split("/")[0]
    if badges =='broadcaster' or badges == 'moderator' or badges == 'vip':
      GetBadgeInfo.verify = True
    else:
        GetBadgeInfo.verify = False
    return

def SetNickName(data):
    GetBadgeInfo(data) 
    if GetBadgeInfo.verify:  # is user a mod/broadcatser/vip
        if data.GetParam(1).strip("@"):
            userName =  "'" + data.GetParam(1).lower().strip("@") + "'"
            VerifyUser(data.GetParam(1).lower())  # Verify user exists from TWITCH.TV
            FoundNickname(data, userName)
        else:
            Send_Message("Please follow the format: !nickname <username> [nickname]")
    else:
        Send_Message("You are not a mod")
    return


def FoundNickname(data, user):
#       Get users nickname and compare
    nickname = str(data.GetParam(2)).strip()
    if VerifyUser.verify and nickname:  # Make sure user enters a nickname
        if not nickname:  # make sure user put in a nickname
            Send_Message("Please follow the format: !nickname <username> [nickname]")
            return
        else:
            GetNickName(data, user, nickname)
    else:
        Send_Message("No valid user or nickname")
        return

def GetNickName(data, user, nickname):
    nicknamesFile = open("Services\Twitch\Logs\ChatNicknames.txt", 'r')  # Find if user has already a nickname
    nicknamesRead = nicknamesFile.read()
    nicknamesFile.close()
    if nickname == "":
        find = str(re.findall("(?<=" + user + ",)\w+", str(nicknamesRead))).strip("[]\"")
        if find:
            Send_Message('{0}, Your nickname is: {1}' .format(user.strip("'"),find.strip("'")))
            return
        else:
           Send_Message('{0}, You do not have a nickname yet only MODS/VIPS can give you one' .format(user.strip("'")))
           return
    else:
        find = str(re.findall(user + ",\w+", str(nicknamesRead))).strip("[]\"") # find if user already has a nickname
        userNickname = user + "," + nickname  # strip any white space
        if find:
            replace = nicknamesRead.replace(find, str(userNickname))  # replace new old w/ new nickname
            with open("Services\Twitch\Logs\ChatNicknames.txt", 'w') as nw:
               Send_Message('{0} nickname was changed to {1}'.format(user.strip("'"), nickname.strip("'")))
               nw.write(replace)
        else:
           with open("Services\Twitch\Logs\ChatNicknames.txt", 'a') as na: # add new user nickname to file
                na.write(userNickname + "\n")
                Send_Message('{0} new nickname {1} was added'.format(user.strip("'"), nickname.strip("'")))
           return 


def VerifyUser(streamerName):
    #  GET TWITCH.TV'S USER IN CHAT DATA DIRECTLY FROM A POST REQUEST
    url = ('https://www.twitch.tv/' + streamerName)
    # Get Client ID just increase it changes
    #client_id = re.search('"Client-ID" ?: ?"(.*?)"', homepage).group(1)
    client_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
    headers = {"Client-Id": client_id}  # get Local Client ID
    result = Parent.GetRequest(url, headers)

    if not result:
        Send_Message(' \w GetRequest passed (streamer is connected to internet)')
            # Get FOLLOWERS
    query = 'query {user(login: "%s") { followers { totalCount } } }' % streamerName  # Query type
    data = {"query": query}

    # Post Request DATA From Network Tab
    result = str(Parent.PostRequest("https://gql.twitch.tv/gql", headers, data))
    find = re.findall(r'(?<=\\\"user\\\":)null', result) # find is user is null from TWITCH.TV
    if not find:  # make sure user is not NONE
      Send_Message('User does exists')
      VerifyUser.verify = True  # User exist
      return
    VerifyUser.verify = False # Use ChatNameLog as reference for valid username 
    Send_Message('User does not exists')
    return


#EXTRAS
#   https://towardsdatascience.com/merging-spreadsheets-with-python-append-f6de2d02e3f3 # GET REQUESTS CODE FROM
#   https://docs.python-requests.org/en/master/user/quickstart/
#   https://www.gkbrk.com/2020/12/twitch-graphql/ # help Get post requests from twitch.tv