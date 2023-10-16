# Slack Client Integration
This is a lightweight integration for Slack to send quick messages.
The integration functions off its own thread, allowing for your primary code to not be held up by Slack messaging.
All you have to do is create an object, pass in the channel name and the Slack token. The integration takes care of the rest.
Once your code is complete, simply call the close() method.
