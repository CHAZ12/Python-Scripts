import socket
import time
import os

# Bot's credentials

BOT_USERNAME = os.getenv('botName')  # The username of your bot
OAUTH_TOKEN = os.getenv('oauth')  # Your bot's OAuth token
CHANNEL_NAME = 'kinstruction'  # The target channel name to send the message to
print(os.environ)  # Check all environment variables to ensure CLIENT_ID is present
# Twitch IRC server details
SERVER = 'irc.chat.twitch.tv'
PORT = 6667

# Connect to the server
def connect():
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((SERVER, PORT))
    return irc

# Authenticate with Twitch IRC
def authenticate(irc):
    irc.send(f"PASS {OAUTH_TOKEN}\r\n".encode('utf-8'))  # Pass the OAuth token
    irc.send(f"NICK {BOT_USERNAME}\r\n".encode('utf-8'))  # The bot's username
    irc.send(f"JOIN #{CHANNEL_NAME}\r\n".encode('utf-8'))  # Join the target channel

# Send a single message to the channel
def send_message(irc, message):
    irc.send(f"PRIVMSG #{CHANNEL_NAME} :{message}\r\n".encode('utf-8'))

# Main bot function to send the message
def main(raider_name, viewer_count, game_name):
    RaidmessagePart1 = f"New raid from {raider_name} with {viewer_count} viewers!"
    RaidmessagePart2 = f"Raider was playing: {game_name}"
    irc = connect()  # Connect to the server
    authenticate(irc)  # Authenticate the bot
    print(f"Bot connected to #{CHANNEL_NAME} and sending message...")
    send_message(irc, RaidmessagePart1)  # type: ignore # Send the message
    time.sleep(2)  # Delay to prevent flooding
    send_message(irc, RaidmessagePart2)  # Send the message again
    irc.close()  # Close the connection

if __name__ == "__main__":
    main()
