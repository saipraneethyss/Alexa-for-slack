# Alexa-for-slack: 
Slack being used in almost all the hackathons and the volunteers can make their lives easier by speaking what they want to post in the channels and Alexa shall take care of message management in channels

## Info: 
Aims to post and get messages to/from Slack, along with listing all the channels present in your slack account.
We use Slack's API methods to post and get information using Web Hooks. Bundled the python code along with dependencies and deployed to amazon lambda,
to communicate between Alexa and Slack API's

## Requirements:
* [Slack WorkSpace](https://slack.com/) and [Slack API service](https://api.slack.com/)
* [Amazon Alexa Skills Kit](https://developer.amazon.com/alexa-skills-kit/)
* [Amazon Lambda Service](https://console.aws.amazon.com/lambda/)
* [Slack Dev kit for Python](https://slackapi.github.io/python-slackclient/index.html)

## Setup:

#### Slack-configuration:
Create a slack workspace and a few channels. Register a new application in [Slack Api Apps](https://api.slack.com/apps). Make sure that the app has
`Incoming Webhooks` , `Bots` and `Permissions` configured and installed to workspace. Use the [Token generator](https://api.slack.com/custom-integrations/legacy-tokens) and place it in `alexacode.py` to test the app.

#### AWS-configuration:

Create a new [Alexa Skill](https://developer.amazon.com/alexa-skills-kit) and provide the following intent schema:
```
{
  "intents": [
    {
      "slots": [
        {
          "name": "txt",
          "type": "LITERAL"
        },
        {
          "name": "channel",
          "type": "LIST_OF_CHANNELS"
        }
      ],
      "intent": "postToSlack"
    },
    {
      "slots": [
        {
          "name": "channel",
          "type": "LIST_OF_CHANNELS"
        }
      ],
      "intent": "getFromSlack"
    },
    {
      "intent": "getChannelNames"
    }
  ]
}

```

Login to the Lambda service and create a function with Alexa Skil Sets as `Trigger Point`. Copy the ARN. 
