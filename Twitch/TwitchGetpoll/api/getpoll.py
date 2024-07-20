import requests
from flask import Flask, request
import requests
import subprocess
import sys
import urllib.parse
import os
import time
import werkzeug
import json
from dotenv import load_dotenv
import re
load_dotenv()
from main import tokendataget, tokendataUpdate
from GetYTpoll import getYTPoll

print('Getting or installing necessary modules')   
try:
    import requests
    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])

try:
    import subprocess
    print('module subprocess is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'subprocess'])


try:
    import werkzeug
    print('module subprocess is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'werkzeug'])
# Broadcaster ID of the streamer you are managing polls for
broadcaster_id = "995402437"
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
print(CLIENT_SECRET)
print(CLIENT_ID)
print(os.environ)  # Check all environment variables to ensure CLIENT_ID is present
CONFIG_FILE = 'config.json'

app = Flask(__name__)
@app.route('/api/getpoll', methods=['GET', 'POST'])
@app.route('/api/getytpoll', methods=['GET', 'POST'])
def getpoll():
    db_values  =  tokendataget()
    print(f"TOKENDATAGET: {db_values}")
    if db_values == None:
        print('Database is empty')
        return 'Database is empty'
    print(db_values)
    
    current_refresh_token = db_values['refresh_token']
    global current_access_token
    current_access_token = db_values['access_token']
    
    if (validate_token(current_access_token) == 'Invalid token'):
        print('Token was invalid')
        refreshtoken(current_refresh_token)
    else:
        print('Access Token is valid.. Continuing to get poll data..')
        
    global ytpoll, title
    ytpoll = False
    
    ready = False
    message_param = request.args.get('message')
    if not message_param:
        print('No message was entered')
        return "No message was enetered"

    baseurl,params = request.url.split('?message=', 1)
    #print(baseurl, " -BASEURL")
    # Decode the URL-encoded string
    decoded_string = urllib.parse.unquote(params)
    print(f"PARMAMATERS:{decoded_string}")

    # Get Poll values from Youtube
    if request.path == '/api/getytpoll':
        print('Gettting values from youtube')
        if decoded_string == None or decoded_string == "":
            print('User did not choose a time')
            return 'User did not set a time duration'
        cleaned_string = re.sub(r'[^\d]', '', decoded_string)
        polltime = int(cleaned_string)
        ytpoll = True
        title, choices = getYTPoll()
        if title is None or choices is None:
            return 'Falied: (YT) User is not LIVE'
        elif len(title) > 60:
            print('Title was too long')
            return(f'Poll: Title was too long, max is 60 char, FOUND:{len(title)}')
        else:
            print('Got YT poll scuessfully')
            values = choices
    
    #Get Poll values from user input from Twitch
    elif request.path == '/api/getpoll':
        print('Setting user values from twitch')
        if len(decoded_string) >= 2:
            values = decoded_string.split(',')
        if(len(values) < 4):
            print('You need more than one option. For example: Title, option 1, option 2, time')
            return 'You need more than one option. For example: Title, option 1, option 2, time'
        elif(len(values)> 7):
            print('TOO MANY OPTION, ONLY 5')
            return 'Too many options requested, only up to 5'
    else:
        print('Domain error, unknown')
        return ('Domain Error, Unknown')
    
    choice1,choice2,choice3,choice4,choice5 = None,None,None,None,None
    if ytpoll == False:
        # SET POL VALUES FROM USER
        for i in range(len(values)):
            if(i == 0): # first entry is title
                title = values[i]
                if len(title) > 60:
                    print('Ttitle was too long')
                    return(f'Poll: Title was too long, max is 60 char, FOUND:{len(title)}')
            if(i == len(values)-1): # get last entry as time
                ready = True
                polltime = int(values[i].strip())
                if polltime > 30:
                    return "Twitch Poll: Max duration exceeded max 30 mins"
                break
            if (i == 1):
                choice1 = values[i]
            if(i == 2):
                choice2 = values[i]
            if(i == 3):
                choice3 = values[i]
            if(i == 4):
                choice4 = values[i]
            if(i == 5):
                choice5 = values[i]
    elif ytpoll:
        if polltime > 30:
            return "Twitch Poll: Max duration exceeded max 30 mins"
         # SET POL VALUES FROM USER
        for i in range(len(values)):
            if(i == 0):
                choice1 = values[i]
            if (i == 1):
                choice2 = values[i]
            if(i == 2):
                choice3 = values[i]
            if(i == 3):
                choice4 = values[i]
            if(i == 4):
                choice5 = values[i]
        ready = True
        
    SetpollValues(choice1, choice2, choice3, choice4, choice5, title, polltime, ready)
    return "Got Poll Values Sucessfully"
        
def SetpollValues(choice1, choice2, choice3, choice4, choice5, title, polltime, ready):       
    if ready:
        if not ytpoll:
            choices = [{"title": choice} for choice in [choice1, choice2, choice3, choice4, choice5] if choice is not None]
        else:
            choices = [choice for choice in [choice1, choice2, choice3, choice4, choice5] if choice is not None]
        print(f'TITLE:{title}')
        print(f'OTPIONS:{choices}')
        print(f'TIME:{polltime}') 
        # Poll data
        poll_data = {
            "broadcaster_id": broadcaster_id,
            "title":title,
            "choices":choices,
            "duration":polltime*60  # Duration in seconds
        }

        # Headers for the request
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {current_access_token}",
        }

        # Make the POST request to create a poll
        response = requests.post("https://api.twitch.tv/helix/polls", json=poll_data, headers=headers)
        print(response.status_code)
        # Check the response
        #print(response.json())
        if response.status_code != 200:
            if 'Error.PollAlreadyActive' in response.json().get('message', ''):
                print("Poll: Poll is already active.")
                return "Poll: Is already active."
            if response.json() == "Invalid OAuth token":
                print("Poll: Token expired or invalid")
                return 'Poll: Token is invalid'
            return 'Poll: Create failed'
        else:
            return "Poll: Created Sucessful."
    else:
        return 'Poll: Creattion failed... ready was False'
        
def refreshtoken(refresh_token):
    poll_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token # Duration in seconds
    }

    # Headers for the request
    headers = {
        "Authorization": "application/x-www-form-urlencoded"
    }

    # Make the POST request to update token
    response = requests.post("https://id.twitch.tv/oauth2/token", json=poll_data, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        #print(response_json)  # Print the entire response JSON
        access_token = response_json.get('access_token')
        refresh_token = response_json.get('refresh_token')
        expires_in = response_json.get('expires_in')
        print(f"NEW: Access Token: {access_token}, Refresh Token: {refresh_token}, Expires in: {expires_in}")
        if (validate_token(access_token) == 'Invalid token'):
            print(f"Error UPDATING FAILED: {response.status_code} - {response.text}")
            return 'NEW: Access Token UPDATE Failed..'
        else:
            print('NEW: Access Token is valid.. Continuing to get poll data..')
            store_tokens(access_token, refresh_token, expires_in)
            return "NEW: Access token updated successful"
    else:
        print('NEW: Access Token is invalid..,')
        return "NEW: Access Token update falied"
        
    
def validate_token(auth_token):
    url = 'https://id.twitch.tv/oauth2/validate'
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get(url, headers=headers)
    if 'invalid access token' in str(response.json()):
        return 'Invalid token'
    else:
        return 'Token is valid'
    
def store_tokens(access_token, refresh_token, expires_in):
    print(f"New acess: {access_token}, New refresh: {refresh_token}, new expires: {expires_in}")
    tokendataUpdate(access_token, refresh_token, expires_in)
    print(tokendataUpdate)

if __name__ == '__main__':
    app.run(debug=True)