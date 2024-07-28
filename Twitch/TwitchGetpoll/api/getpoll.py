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
    
    current_refresh_token = db_values['refresh_token']
    current_access_token = db_values['access_token']
    
    if (validate_token(current_access_token) == 'Invalid token'):
        print('Token was invalid')
        refreshtoken(current_refresh_token)
        current_access_token = access_token
    else:
        print('Access Token is valid.. Continuing to get poll data..')
        
    global ytpoll, title
    ytpoll = False
    ready = False
    params = None
    #message_param = request.args.get('message')
    #if not message_param:
        #print('No Condtion after command was entered')
        #return "No condtion after command was entered"

    baseurl,params = request.url.split('?message=', 1)
    # Decode the URL-encoded string
    if params is not None:
        decoded_string = urllib.parse.unquote(params or '')
    print(f"PARMAMATERS:{decoded_string}")

    # Get Poll values from Youtube
    if request.path == '/api/getytpoll':
        print('Gettting values from youtube')
        if decoded_string == None or decoded_string == '':
            print('User did not choose a time')
            return 'Poll: User did not set a time duration. Ex !getyt 20'
        cleaned_string = re.sub(r'[^\d]', '', decoded_string)
        polltime = int(cleaned_string)
        ytpoll = True
        title, choices = getYTPoll()
        if title is None or choices is None:
            return 'Poll: Falied:(YT) User is not LIVE or no poll was found'
        elif len(title) > 60:
            print('Title was too long')
            return(f'Poll: Title was too long, max is 60 char, FOUND:{len(title)}')
        else:
            print('Poll: Got YT poll scuessfully')
            values = choices
    
    #Get Poll values from Twitch
    elif request.path == '/api/getpoll':
        print('Setting user values from twitch')
        message_param = request.args.get('message')
        if not message_param:
            print('No Condtions after command was entered')
            return "Poll: No condtions after command was entered"
        if len(decoded_string) >= 2:
            values = decoded_string.split(',')
        if(len(values) < 4):
            print('You need more than one condtions. Minimum example: Title, option 1, option 2, time')
            return 'Poll: You need more than one condtions. Minimum example: Title, option 1, option 2, time'
        elif(len(values)> 7):
            print('TOO MANY OPTION, ONLY 5')
            return 'Poll: Too many options requested, only up to 5'
    else:
        print('Domain error, unknown')
        return ('Poll: Domain Error, Unknown')
    
    choice1,choice2,choice3,choice4,choice5 = None,None,None,None,None
    if ytpoll == False:
        # SET POL VALUES FROM USER
        for i in range(len(values)):
            if(i == 0): # first entry is title
                title = values[i]
                if len(title) > 60:
                    print('Title was too long')
                    return(f'Poll: Title was too long, max is 60 char. FOUND:{len(title)}')
            if(i == len(values)-1): # get last entry as time
                ready = True
                cleaned_string = re.sub(r'[^\d]', '', str(values[i]))
                polltime = int(cleaned_string)
                if polltime > 30:
                    return "Poll: Max duration exceeded max 30 mins"
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
            return "Poll: Max duration exceeded max 30 mins"
         # SET POLL VALUES FROM USER
        for i in range(len(values)):
            if(len(str(values[i]['title'])) > 25):
                print(f"Option, {i+1} was too long. Found: {len(str(values[i]['title']))} chars in... {values[i]['title']}")
                return f"Poll: Option was too long. Found: {len(str(values[i]['title']))} chars in... {values[i]['title']}"
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
            
    if ready:
        if not ytpoll:
            choices = [{"title": choice} for choice in [choice1, choice2, choice3, choice4, choice5] if choice is not None or choice != '']
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
            "duration":polltime*60  # Duration in seconds max(1800 sec)
        }

        # Headers for the request
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {current_access_token}",
        }

        # Make the POST request to create a poll
        response = requests.post("https://api.twitch.tv/helix/polls", json=poll_data, headers=headers)
        # Check the response
        if response.status_code != 200:
            if 'Error.PollAlreadyActive' in response.json().get('message', ''):
                print("Poll: Poll is already active.")
                return "Poll: Is already active."
            if response.json() == "Invalid OAuth token":
                print("Poll: Token expired or invalid")
                return 'Poll: Token is invalid'
            if (response.status_code == 400 or response.status_code == 401):
                return f"Poll: Creation failed, Error: {response.json()}"
            return 'Poll: Create failed'
        else:
            request.close()
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
        global access_token # save if value is ever changed
        access_token = response_json.get('access_token')
        refresh_token = response_json.get('refresh_token')
        expires_in = response_json.get('expires_in')
        print(f"NEW: Access Token: {access_token}, Refresh Token: {refresh_token}, Expires in: {expires_in}")
        if (validate_token(access_token) == 'Invalid token'): # Always have to validate new token
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
    if 'invalid access token' in str(response.json() or 'Invalid OAuth token' in str(response.json())):
        return 'Invalid token'
    else:
        return 'Token is valid'
    
def store_tokens(access_token, refresh_token, expires_in):
    tokendataUpdate(access_token, refresh_token, expires_in)

if __name__ == '__main__':
    app.run(debug=True)