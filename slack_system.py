
import json as js
import requests
from slackclient import SlackClient as slack


#enter the input text
# input_text = input()



# client_key = "3e92dfca62f0e21d2d19613d3b45f7a8"
# client_id = "266423738560.266425477648"
# client_token = "D0YOuhtpPaq2r36msc4TvZse"
client_token = "xoxp-266423738560-266561351921-267975201286-77ef913454a982d73fdbac7caf8acaa3"

data = {
    "text": "I am a test message http://slack.com",
    "attachments": [
        {
            "text": "And here’s an attachment!"
        }
    ]
}


sc = slack(client_token)
sc.api_call("chat.postMessage",channel = "#kronusposts", text = data.get('text'),attachments= data.get("attachments"))

#LIST CHANNELS
# for channel in sc.api_call("channels.list").get('channels'):
# 	print("channel name: ", channel.get('name'), " channel id: ", channel.get('id'))
# 	print("\n")

#channels_list = js.loads(sc.api_call("channels.list"))
