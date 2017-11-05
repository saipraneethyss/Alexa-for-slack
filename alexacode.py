"""
This is custom skill designed for Alexa to post data and get content from Slack
"""

from __future__ import print_function
import slack_system as slack

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def channel_in_context(intent,slack_app):
    '''
        this method returns the channel from which messages are read from or posted to to. By default, the general channel
        is returned else returns the specific channel mentioned in the text input
    '''
    #returns dict of channels; key= name , value = channel Id
    list_of_channels_in_slack = slack_app.list_channels() 
    
    channel_to_post = list_of_channels_in_slack['general']
    if 'channel' in intent['slots'] and 'value' in intent['slots']['channel'].keys() :
        if intent['slots']['channel']['value'] in list_of_channels_in_slack.keys():
            channel_to_post = list_of_channels_in_slack[intent['slots']['channel']['value']]
    
    return channel_to_post



def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those heres
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Connected to your slack account"\
                    " you can say, post to my slack or, get messages from slack "\
                    " or, list channels in my slack account."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your choice. "\
                     " you can say, post to my slack or, get messages from slack "\
                    " or, list channels in my slack account."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa for slack app " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def post_to_slack(intent, session, slack_app):
    """ 
        This method posts the message contents to the specified slack channel. Default channel - general
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    #check for the custom text
    if 'txt' in intent['slots']:
        messageToSlack = intent['slots']['txt']['value']
        session_attributes = slack_app.post_on_slack(messageToSlack,channel_in_context(intent,slack_app))
        speech_output = "Your message has been posted successfully"
        reprompt_text = "please try again to post the message to your slack account"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def get_from_slack(intent, session, slack_app):
    '''
        this method returns the responses/messages posted in the specified slack channel. Default channel - general
    '''
   session_attributes = {}
   reprompt_text = None
   #define the channel for communication
   messages = slack_app.get_from_slack(channel_in_context(intent,slack_app))

   #retrive the messages
   message_data = (', ').join(messages) if messages else "Currently there are no meesages in this channel "
   reprompt_text = "Try again to read messages"
   should_end_session = False
   
   return build_response(session_attributes, build_speechlet_response(
       intent['name'], message_data, reprompt_text, should_end_session))


def get_channel_info(intent, session, slack_app):
    '''
        this method returns the list of channels available on slack
    '''
   session_attributes = {}
   reprompt_text = None
   
   #get the list of channels
   channels = slack_app.list_channels()
   channel_data = (', ').join(channels) if channels.keys() else " there are no channels "
   reprompt_text = "Try again to read messages"
   should_end_session = False
   
   return build_response(session_attributes, build_speechlet_response(
       intent['name'], channel_data, reprompt_text, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to Alexa for Slack skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    #obtain the token - work around for now using test token
    token= "xoxp-266423738560-266561351921-268280166855-7a30e0df9a7406137263ff656b1a0e30"

    #initialize the slack client object using outh 2.0 test token
    slack_app = slack.slack_account(token)

    # Dispatch to  skill's intent handlers
    if intent_name == "postToSlack":
        return post_to_slack(intent, session,slack_app)
    elif intent_name == "getFromSlack":
        return get_from_slack(intent, session,slack_app)
    elif intent_name == "getChannelNames":
        return get_channel_info(intent,session,slack_app)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
