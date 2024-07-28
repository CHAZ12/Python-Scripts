import requests 
from bs4 import BeautifulSoup
import re
import time
import werkzeug
import json
import os
from GetYTData import GetYTIDs, YTIDsUpdate
STREAMER = os.getenv('STREAMER')
MainPage = "https://www.youtube.com/@" + str(STREAMER)
LiveChatPage ="https://studio.youtube.com/live_chat?"

def GetVideoID():
    print(f"YOUTUBE URL: {MainPage}")
    print("getting VideoID")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(str(MainPage), headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    if r.status_code == 200:
        content = r.text
        pos = r.text.find('/hqdefault_live.jpg')
        if pos != -1:
            start_idx = content.rfind(r'\/', 0, pos) + 1
            video_id = content[start_idx:pos]
            videoId = re.findall(r'(?<=vi\/)([^\/]+)', video_id)[0]
            if videoId == None or videoId == []:
                return "Poll: Could not get VideoId"
            return videoId
        else:
            return "Poll: Could not get VideoId"   
    else:
        print('Page not found')

def GetContinuation():
    print("GEtting old Youtube IDs")
    #Check if there is already a video ID
    db_values  =  GetYTIDs()
    print(f"YTDATAGET: {db_values}")
    if db_values:
        print("Database is empty, getting new YT ID's")
        current_videoID = "NONE"
    else:
        current_videoID = db_values['videoId']
        current_continuation = db_values['continuation']
        
    StreamPage = "https://www.youtube.com/watch?v=" + current_videoID
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(str(StreamPage), headers=headers)
    if r.status_code == 200:
        content = r.text
        pos = content.find('backgroundPromoRenderer')
        if pos != -1:
            video_id = content[pos:pos+300]
            status = re.findall(r'(?<=text":")([^\"]+)', video_id)[0]
            if status == "This video isn't available anymore":
                print("VideoId does not exist.. Getting a new one")
            else:
                print("Current ID is valid... Skipping new continuation")
                return current_continuation
        else:
            print("VideoId exist... Using old continuation")
            return True 
    # Get a new continuation if failed  
    print("Getting new continuation")
    VideoID = str(GetVideoID())
    StreamPage2 = "https://www.youtube.com/watch?v=" + VideoID
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(str(StreamPage2), headers=headers)
    if r.status_code == 200:
        content = r.text
        pos = content.find('reloadContinuationData')
        if pos != -1:
            video_id = content[pos:pos+300]
            continuation = re.findall(r'(?<=continuation":")([^\"]+)', video_id)[0]
            if continuation == None or continuation == []:
                return "Poll: Could not get continuation"
            store_YTData(VideoID,continuation)
            return continuation
    else:
        print('Page not found')
        return None

def store_YTData(video_id, continuation):
    YTIDsUpdate(video_id, continuation)

def getYTPoll():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    continuationStatus = GetContinuation()
    #continuationStatus = "0ofMyANfGkJDaWtxSndvWVZVTTVSMnBtTFdReVNURjRiVWsxUmxCelNFNWxibXRuRWd0d1ZXbDJRMlZ2U2s5VlRTQU1NQUElM0QwAYIBBggEGAIgAIgBAaABpcy3z9PIhwOoAQA%253D"
    if not continuationStatus:
        print("Failed to get continuation")
        return None, None
    else:
        print('Using old continuation')
    PollPage = f"{LiveChatPage}continuation={str(continuationStatus)}"
    r = requests.get(str(PollPage), headers=headers)
    choices = []
    if r.status_code == 200:
        content = r.text
        pos = content.find('pollQuestion')
        if pos != -1:
            questionpos = content[pos:pos+250]
            Foundquestion = re.findall(r'(?<=pollQuestion":{"runs":\[{"text":")([^\"]+)', questionpos)[0]
            print("FOUND QUESTION:", Foundquestion)
            if Foundquestion == None or Foundquestion == []:
                return "Poll: Could not get continuation"
            print("Found Title")
        pos1 = content.find('pollRenderer')
        if pos != -1:
            choicesdata = content[pos1:pos1+2000]
            for i in range(len(re.findall(r'(([^"]+)(?="}]},"selected":false))', choicesdata))):
                pollchoice1 = re.findall(r'(([^"]+)(?="}]},"selected":false))', choicesdata)[i]
                choices.append(pollchoice1[0])
            if pollchoice1 == None or pollchoice1 == []:
                return "Poll: Could not get choices"
            choices = [{"title": choice} for choice in choices if choice is not None]
            print("Found Choices", choices)
        if choices == []:
            print('Could not find poll.')
            return None, None
        print('Retrieved YT data')
        return str(Foundquestion).strip("[]\'"), choices
        # soup = BeautifulSoup(r.content, "html.parser")
        # title = re.findall(r'(?<="pollQuestion":{"runs":\[{"text":")([^"]+)',str(soup.contents))
        # print(title)
        # for i in range(len(re.findall(r'(([^"]+)(?="}]},"selected":false))',str(soup.contents)))):
        #     pollchoice1 = re.findall(r'(([^"]+)(?="}]},"selected":false))',str(soup.contents))[i]
        #     choices.append(pollchoice1[0])
        # print('Retrieved YT data')
        # choices = [{"title": choice} for choice in choices if choice is not None]
        # print(choices)
        # if choices == []:
        #     print('Could not find poll.')
        #     return None, None
        # return str(title).strip("[]\'") ,choices
    else:
        print('Failed to retrieve data')
        return None, None

getYTPoll()