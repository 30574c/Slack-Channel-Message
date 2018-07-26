from slackclient import SlackClient
import time
import threading
from threading import Thread

### DESCRIPTION ###
# There already are slack API python wrappers but this code further simplifies the ability to just
# post a message to a slack channel. All you have to do is install the above dependencies,
# and use the below example code anywhere you want. The beauty of this code is that it
# runs on its own thread and can handle a large queue of messages that might get backed up
# due to the slack API rate limit restrictions.

### EXAMPLE CODE TO USE ###
# from SlackClientIntegration import Slack
# slackObject = Slack('channel name')
# slackObject.sendMessage("add string here")
# slackObject.sendMessage("add as many more srings as you want")
# slackObject.closeThread() 

class Slack:

    def __init__(self, channelName):
        self.slack_token_NAME1 = "xxxx-your_slack_token" #MODIFY
        self.slack_token_NAME2 = "xxxx-your_slack_token" #MODIFY
        self.channelName = channelName
        self.messageQueue = []
        self.threadExitSignal = threading.Event()
        self.thread = Thread(target=self.sendMessageFromQueue)
        self.thread.start()

    def sendMessageFromQueue(self):

        try:
            ### VARIABLES ###
            slack_token = ''
            slack_channel_id = ''

            # SET UP TOKEN AND NAME (ONLY MODIFY THIS SECTION FOR NEW CHANNELS)
            if ('your_channel_name' in self.channelName): #MODIFY
                slack_token = self.slack_token_NAME1 #MODIFY

            elif ('your_other_channel_name' in self.channelName): #MODIFY
                slack_token = self.slack_token_NAME2 #MODIFY

            slack_client = SlackClient(slack_token)

            # RETRIEVE CHANNEL ID
            channels = slack_client.api_call("channels.list", exclude_archived=1)['channels']
            for channel in channels:
                if channel.get('name') == self.channelName:
                    slack_channel_id = channel.get('id')
                    break

        except Exception as error:
            print("ERROR: Class Slack , sendMessageFromQueue ... {0}".format(error))

        while self.messageQueue or not self.threadExitSignal.is_set():

            try:
                if (self.messageQueue):

                    ### POP MESSAGE FROM QUEUE ###
                    queueMessage = self.messageQueue.pop(0)

                    ### VARIABLES ###
                    slack_message = queueMessage

                    ### SEND MESSAGE ###
                    time.sleep(1)
                    slack_client.api_call(
                        "chat.postMessage",
                        channel = slack_channel_id,
                        text = slack_message
                    )

            except Exception as error:
                print ("ERROR: Class Slack , sendMessageFromQueue ... {0}".format(error))

    def sendMessage(self, message):
        self.messageQueue.append(message)

    def closeThread(self):
        self.threadExitSignal.set()
        print("Waiting for Slack thread to finish submitting messages, if any.")
        self.thread.join()