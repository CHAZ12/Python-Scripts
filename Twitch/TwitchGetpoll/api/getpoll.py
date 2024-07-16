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
load_dotenv()
from main import tokendataget, tokendataUpdate

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
def getpoll():
    db_values  =  tokendataget()
    print(f"TOKENDATAGET: {db_values}")
    if db_values == None:
        print('Database is empty')
        return 'Database is empty'
    print(db_values)
    
    current_refresh_token = db_values['refresh_token']
    current_access_token = db_values['access_token']
    if is_token_expired(db_values['expires_at']):
        print("Access token expired. Refreshing token...")
        refreshtoken(current_refresh_token)
    else:
        print("Access token is valid... Continuing to Get poll data...")
    
    ready = False
    message_param = request.args.get('message')
    if not message_param:
        print('No message was entered')
        return "No message was enetered"
    
    baseurl,params = request.url.split('?message=', 1)
    print(baseurl, " -BASEURL")
    # Decode the URL-encoded string
    decoded_string = urllib.parse.unquote(params)
    print(params, " -PARMAMATERS")
    values = decoded_string.split(',')
    
    print(values , ": VALUES")
    if(len(values) <= 3):
        print('You need more than one option. For example: Title, option 1, option 2, time')
        return 'You need more than one option. For example: Title, option 1, option 2, time'
    elif(len(values)> 7):
        print('TOO MANY OPTION, ONLY 5')
        return 'Too many options requested, only up to 5'
    choice1,choice2,choice3,choice4,choice5 = None,None,None,None,None
    for i in range(len(values)):
        print(i)
        if(i == 0): # first entry is title
            title = values[i]
            #print(f"title: {values[i]}")
        if(i == len(values)-1): # get last entry as time
            #print(f"Time: {values[i]}")
            ready = True
            time = int(values[i])
            if time >30:
                return "Twitch Poll: Max duration exceeded max 30 mins"
            break
        if (i == 1):
            choice1 = values[i]
        if(i ==2):
            choice2 = values[i]
        if(i == 3):
            choice3 = values[i]
        if(i == 4):
            choice4 = values[i]
        if(i == 5):
            choice5 = values[i]
        
    if ready:
        choices = [{"title": choice} for choice in [choice1, choice2, choice3, choice4, choice5] if choice is not None]
        print(choices) 
        if ready:
            # Poll data
            poll_data = {
                "broadcaster_id": broadcaster_id,
                "title": f"{title}. You have {time} mins.",
                "choices":choices,
                "duration": time*60  # Duration in seconds
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
            if response.status_code != 200:
                if 'PollAlreadyActive' in response.text:
                    print("Poll creation failed: Poll is already active.")
                    return "Poll is already active."
                if response.json() == "Invalid OAuth token":
                    print("Poll: Token expired or invalid")
                    print("Retrieving new acess token and validate it")
                    refreshtoken()
                    return "Poll: Token expired or invalid"
                    
                elif 'failed integrity check':
                    print("You need to update Client integrity")
                return "Intergity Failed"
            else:
                return "Poll Created Sucessful.", 200
        else:
            return 'Poll creattion failed.'
        
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
        print(f"Access Token: {access_token}, Refresh Token: {refresh_token}, Expires in: {expires_in}")
        store_tokens(access_token, refresh_token, expires_in)
        validate_token(access_token)
        return "Access token updated scuessful"
    
    else:
        print(f"Error: {response.status_code} - {response.text}")

def validate_token(auth_token):
    url = 'https://id.twitch.tv/oauth2/validate'
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get(url, headers=headers)
    if 'invalid access token' in str(response.json()):
        print('Token is invlaid')
        return 'Invalid token' 
    else:
        print('success token is valid')
        return 'Token is valid' 
    
def store_tokens(access_token, refresh_token, expires_in):
    print(f"New acess: {access_token}, New refresh: {refresh_token}, new expires: {expires_in}")
    tokendataUpdate(access_token, refresh_token, expires_in)
    print(tokendataUpdate)

def is_token_expired(expires_at):
    return int(time.time()) >= expires_at - int(60)

if __name__ == '__main__':
    app.run(debug=True)
