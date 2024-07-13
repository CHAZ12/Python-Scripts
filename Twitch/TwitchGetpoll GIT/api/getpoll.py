from flask import Flask, request
import json
import requests
import subprocess
import sys
import urllib.parse

print('Getting or installing necessary modules')
try:
    import requests
    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'Flask'])

app = Flask(__name__)

@app.route('/api/getpoll', methods=['GET', 'POST'])
def watchtime():
    baseurl,params = request.url.split('?message=', 1)
    print(baseurl)
    # Decode the URL-encoded string
    decoded_string = urllib.parse.unquote(params)
    values = decoded_string.split(',')
    if(len(values) <= 3):
        return 'You need more than one option. For example: Title, option 1, option 2, time'
    elif(len(values)> 6):
        return 'Too many options requested, only up to 5'
    # Print the separated values
    print("Separated values:")
    choice1,choice2,choice3,choice4,choice5 = None,None,None,None,None
    for index, value in enumerate(values):
        if(index == 0): # first entry is title
            title = values[index]
            print(f"title: {values[index]}")
        elif(index == len(values)-1): # get last entry as time
            print(f"Time: {values[index]}")
            ready = True
            time = values[index]
            break
        if (index == 1):
            choice1 = values[index]
        elif(index ==2):
            choice2 = values[index]
        elif(index == 3):
            choice3 = values[index]
        elif(index == 4):
            choice4 = values[index]
        elif(index == 5):
            choice5 = values[index]
        
        #print(value.strip())  # Strip to remove leading/trailing spaces if any
    choices = [{"title": choice} for choice in [choice1, choice2, choice3, choice4, choice5] if choice is not None]
    print(choices) 
    if ready:
        payload = [
  {
    "operationName": "CreatePoll",
    "variables": {
      "input": {
        "isCommunityPointsVotingEnabled": False,
        "durationSeconds": int(time)*60,
        "ownedBy": "******",
        "multichoiceEnabled": True,
        "title": f"{title}. You have {time} mins.",
        "choices": choices
      }
    },
    "extensions": {
      "persistedQuery": {
        "version": 1,
        "sha256Hash": "****"
      }
    }
  }
        ]
        headers = {
            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Authorization': 'OAuth a****',
            'Client-Integrity': '***',
            'X-Device-Id': '****'
        }
        response = requests.post("https://gql.twitch.tv/gql", data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            return f"HTTP status code: {response.status_code}\nResponse: {response.text}", 500
        if 'POLL_ALREADY_ACTIVE' in response.text:
            print("Poll creation failed: Poll is already active.")
            return "Poll is already active."
        else:
            return "Poll Created Sucessful.", 200
    else:
        return 'Poll creattion failed.'
def html_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

if __name__ == '__main__':
    app.run(debug=True)