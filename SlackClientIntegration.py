from slack_sdk import WebClient
import threading, time

### EXAMPLE ###
# from SlackClientIntegration import Slack
# from config import *
# tradingUpdates = Slack('bot_testing',TRADINGUPDATEBOT_SLACK_TOKEN) # Token in config
# tradingUpdates.sendMessage('MESSAGE')
# tradingUpdates.close()

class Slack:

    def __init__(self, channelName, token):
        self.slackToken = token
        self.channelName = channelName
        self.messageQueue = []
        self.threadExitSignal = threading.Event()
        self.thread = threading.Thread(target=self.sendMessageFromQueue)
        self.thread.start()
        self.count = 0

    def sendMessageFromQueue(self):
        try:
            ### PREPARE CLIENT ###
            client = WebClient(self.slackToken)

            ### RETRIEVE CHANNEL ID ###
            channels = client.api_call('conversations.list')['channels']
            for channel in channels:
                if channel['name'] == self.channelName:
                    channelID = channel.get('id')
                    break

            while not self.threadExitSignal.is_set() or not self.count:
                while self.messageQueue:
                    ### POP MESSAGE FROM QUEUE ###
                    queueMessage = self.messageQueue.pop(0)

                    ### SEND MESSAGE ###
                    client.chat_postMessage(channel=channelID, text=queueMessage)
                    time.sleep(1)
                    self.count += 1

        except Exception as error:
            print("ERROR: Class Slack , sendMessageFromQueue ... {error}".format(error=error))

    def sendMessage(self, message):
        self.messageQueue.append(message)

    def close(self):
        self.threadExitSignal.set()
        self.thread.join()