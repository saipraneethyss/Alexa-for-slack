
import json as js
import requests
from slackclient import SlackClient as slack


#enter the input text\
# input_text = input()




# client_key = "3e92dfca62f0e21d2d19613d3b45f7a8"
# client_id = "266423738560.266425477648"
# client_token = "D0YOuhtpPaq2r36msc4TvZse"
def postOnSlackfromAlexa(data):
	client_token = "xoxp-266423738560-266561351921-268041547894-8f6f92024f9ed5a875360078d4bfa9cb"

	sc = slack(client_token)
	sc.api_call("chat.postMessage",channel = "#kronusposts", text = data)

#LIST CHANNELS
# for channel in sc.api_call("channels.list").get('channels'):
# 	print("channel name: ", channel.get('name'), " channel id: ", channel.get('id'))
# 	print("\n")

#channels_list = js.loads(sc.api_call("channels.list"))

def get_messages(channel_id,count_val):
	client_token = "xoxp-266423738560-266561351921-268041547894-8f6f92024f9ed5a875360078d4bfa9cb"
	sc = slack(client_token)
	messages = sc.api_call("channels.history",channel= channel_id,count=count_val)#"C7V6G1UE9")
	new_messages = [message.get('text') for message in messages.get('messages')]
	return str(new_messages)