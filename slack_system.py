
import json as js
import requests
from slackclient import SlackClient as slack



class slack_account:
	'''
		class to create the slack objects through test token
	'''

	def __init__(self,client_token):
		self.slack_client = slack(client_token)

	def post_on_slack(self,data,channel_to_post):
		'''
			method to post data to channel_to_post
		'''
		self.slack_client.api_call("chat.postMessage",channel = channel_to_post, text = data)


	def get_from_slack(self,channel_id):
		'''
			mehtod that retrives the latest 3 messages from the specified channel
		'''
		messages = self.slack_client.api_call("channels.history",channel= channel_id)
		count = len(messages.get('messages')) if len(messages.get('messages'))<=3 else 3
		if messages.get('messages'):
			new_messages = [message.get('text') for iteration,message in enumerate(messages.get('messages')) 
							if iteration<count and 'has joined the channel' not in message.get('text')]
			return new_messages
		else:
			return None

	def list_channels(self):
		'''
			method that lists all the available channels in slack
		'''
		channels_list = {}
		for channel in self.slack_client.api_call("channels.list").get('channels'):
			channels_list[channel.get('name')] = channel.get('id')
		return channels_list
