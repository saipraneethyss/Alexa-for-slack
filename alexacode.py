"""
This is custom skill designed for Alexa to post data and get content from Slack. It takes the message and channel name as input for posting data and channel name
to retrieve data
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

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome!!"
    speech_output = "You are now connected to your slack account. "\
                    "You can post messages in your slack and get recent messages."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please post a message or retrieve messages from your slack"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Slack Integration with Alexa. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def post_to_slack(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'txt' in intent['slots']:
        messageToSlack = intent['slots']['txt']['value']
        session_attributes = slack.post_on_slack_from_alexa(messageToSlack)
        speech_output = "Your message has been posted successfully"
        reprompt_text = "Please try again"
    else:
        speech_output = "I'm not sure what what you want to do. You say post to myslack or get information from myslack."
        reprompt_text = "I'm not sure what what you want to do. You say post to myslack or get information from myslack."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_from_slack(intent, session):
   session_attributes = {}
   reprompt_text = None
   #define the channel for commiunication
   channel = "C7V6G1UE9"
   count_val = 4
   messages = slack.get_messages(channel,count_val)
   message_data = ('').join(messages) if messages else "There are no messages in this channel"
   reprompt_text = "Try again to read messages"
   should_end_session = False
   # Setting reprompt_text to None signifies that we do not want to reprompt
   # the user. If the user does not respond or says something that is not
   # understood, the session will end.
   return build_response(session_attributes, build_speechlet_response(
       intent['name'], message_data, reprompt_text, should_end_session))



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
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "postToSlack":
        return post_to_slack(intent, session)
    elif intent_name == "getFromSlack":
        return get_from_slack(intent, session)
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
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
