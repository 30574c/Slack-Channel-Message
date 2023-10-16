# Slack Client Integration
This is a lightweight integration for Slack to send quick messages.
The integration functions off its own thread, allowing for your primary code to not be held up by Slack messaging.
All you have to do is create an object, passing in the channel name and the Slack token. Then you call the `sendMessage` method with your message. The integration takes care of the rest.
Once your code is complete, simply call the close() method.

# Example Utilization
* You only have to create an object once and close it at the end of your script. This way you don't have to create an object every time you want to send a message.
```
from SlackClientIntegration import Slack
tradingUpdates = Slack('slack_channel_name',SLACK_TOKEN)
tradingUpdates.sendMessage('MESSAGE')
tradingUpdates.close()
```
