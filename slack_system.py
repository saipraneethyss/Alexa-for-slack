
import json as js
import requests
from slackclient import SlackClient as slack



class slack_account:

	def __init__(self,client_token):
		self.slack_client = slack(client_token)

	def post_on_slack(self,data,channel_to_post):
		self.slack_client.api_call("chat.postMessage",channel = channel_to_post, text = data)


	def get_from_slack(self,channel_id):
		messages = self.slack_client.api_call("channels.history",channel= channel_id)
		count = len(messages.get('messages')) if len(messages.get('messages'))<=3 else 3
		if messages.get('messages'):
			new_messages = [message.get('text') for iteration,message in enumerate(messages.get('messages')) 
							if iteration<count and 'has joined the channel' not in message.get('text')]
			return new_messages
		else:
			return None

	def list_channels(self):
		channels_list = {}
		for channel in self.slack_client.api_call("channels.list").get('channels'):
			channels_list[channel.get('name')] = channel.get('id')
			# print(channels_list)
		return channels_list



# #testing
# slack_app = slack_account()
# # slack_app.post_on_slack(input(),)

# for key,value in slack_app.list_channels().items():
# 	print("current messages from channel: "+key)
# 	print(slack_app.get_from_slack(value))
# 	print('\n')