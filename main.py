import os
import requests
import logging
import yaml
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# TODO: Add command line arguments parsing
# Uncomment next line for debugging
#logging.basicConfig(level=logging.INFO)
channels = {}
users = {}
with open("routing.conf", "r") as f:
	routing = yaml.safe_load(f)
logging.info ("Routing is loaded: %s", routing)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
tgtoken = os.environ.get("TG_BOT_TOKEN")

@app.event("message")
def handle_message_events(message):

	# Find and cache real user name
	try:
		users[message['user']]
	except KeyError:
		user = client.users_info(
        	user=message['user']
    	)
		user_name = user['user']['real_name']
		users[message['user']] = user_name
		logging.info ("Added %s user to cache", user_name)
	else:
		user_name = users[message['user']]
	
	# Find and cache real channel name
	try:
		channels[message['channel']]
	except KeyError:
		channel = client.conversations_info(
	    	channel=message['channel']
	    )
		channel_name = channel['channel']['name']
		channels[message['channel']] = channel_name
		logging.info ("Added %s channel to cache", channel_name)
	else:
		channel_name = channels[message['channel']]

	# Find if routing is defined, otherwise drop the message
	try:
		routing[channel_name]
	except KeyError:
		logging.info ('No route for %s', channel_name)
	else:
		logging.info ('%s => %s', message['channel'], channel_name)
		chat_id = routing[channel_name]
		text = f"{user_name}: {message['text']}"
		url = f"https://api.telegram.org/bot{tgtoken}/sendMessage?chat_id={chat_id}&text={text}"
		r = requests.get(url)
		status = r.json()
		if status['ok'] != True:
			logging.warning ('%s', status)
		
# Start the app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()