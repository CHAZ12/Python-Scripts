import requests
from flask import Flask, request, jsonify, Response
import subprocess
import sys
import os
from dotenv import load_dotenv
load_dotenv()
from TwitchSendmessage import main
print('Getting or installing necessary modules')   
try:
    import requests
    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])

try:
    import werkzeug
    print('module werkzeug is installed')
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

@app.route('/api/getraid', methods=['GET'])
def webhook():
    if request.method == "GET":
        # Handle Twitch webhook verification
        hub_mode = request.args.get("hub.mode")
        hub_challenge = request.args.get("hub.challenge")
        hub_topic = request.args.get("hub.topic")

        if hub_mode == "subscribe" and hub_challenge:
            print(f"Verifying subscription for topic: {hub_topic}")
            return Response(hub_challenge, status=200, mimetype="text/plain")
    
    # Handle actual webhook events (POST)
    if request.method == "POST":
        event = request.json
        print("Received event:", event)
        return Response(status=200)

    return Response(status=404)

@app.route('/api/getraid', methods=['POST'])
def raid_webhook():
    if request.method == 'POST':
        # Handle the incoming webhook data
        data = request.json
        if data.get("subscription") and data.get("event"):
            event_type = data["subscription"]["type"]
            event_data = data["event"]
            if event_type == "channel.raid":
                raider_id = event_data["from_broadcaster_user_id"]
                raider_name = event_data["from_broadcaster_user_name"]
                viewer_count = event_data["viewers"]

                # Get the game the raider was playing
                game_name = get_raider_game(raider_id, "o1v0a7rwoaywcs0khglor2gx81212r")

                print(f"New raid from {raider_name} with {viewer_count} viewers!")
                if game_name:
                    print(f"Raider was playing: {game_name}")

                send_request(raider_name, viewer_count, game_name)
                
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "failed"}), 400
    return jsonify({"status": "success"}), 200

def get_raider_game(raider_id, access_token):
    url = f"https://api.twitch.tv/helix/streams?user_id={raider_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-ID": "dmal2lel1xwz6nz6rulliibx3uam2t"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        stream_data = response.json()
        if stream_data["data"]:
            game_name = stream_data["data"][0]["game_name"]
            print(f"Raider was playing: {game_name}")
            return game_name
        else:
            print("Raider is not currently streaming.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def send_request(raider_name, viewer_count, game_name):
    main(raider_name, viewer_count, game_name)

if __name__ == '__main__':
    app.run()