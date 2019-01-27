""" A very simple Slack bot that will listen to incoming messages, compare their senders
    to a list of valid users and if they are not allowed to post, delete the messages.
    This is to implement an "Announcement"-like channel where only certain people may post.
"""
import os
from slackclient import SlackClient

SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL_TOKEN = os.environ["SLACK_CHANNEL_TOKEN"]
SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
USERS_ALLOW = os.environ["USERS_ALLOW"].split(',')
DEBUG = True

def lambda_handler(event, context):
    """ This is the function Lambda will call. It uses the collection of command_handlers
    created in the handlers module.
    """
    print(event)
    retval = {}

    try:
        if event["token"] == SLACK_CHANNEL_TOKEN:
            if event["event"]["user"] in USERS_ALLOW:
                if DEBUG:
                    print("User allowed: " +event["event"]["user"])
                    #retval['text'] = "User allowed: " + event["user"]
                    send_to_slack(retval['text'])
            else:
                if DEBUG:
                    print("User not allowed: " +event["event"]["user"])
                    #retval['text'] = "User not allowed: " + event["user"]
                    print(event["event"]["ts"])
                sc = SlackClient(SLACK_API_TOKEN)
                if DEBUG:
                    print("Deleting message: " + str(event["event"]["ts"]))
                ret = sc.api_call(
                    "chat.delete",
                    channel=SLACK_CHANNEL_ID,
                    ts=event["event"]["ts"]
                )
                if DEBUG:
                    print(ret)
        else:
            #print("Wrong channel token")
            retval['text'] = "Error: Wrong channel token"

    except Exception as e:
        retval['text'] = 'Error: {}'.format(str(e))

    return retval
