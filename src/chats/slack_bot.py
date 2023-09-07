import slack
from slack.errors import SlackApiError
from flask import Flask
from slackeventsapi import SlackEventAdapter
from infrastructure.bot_abstract import AbstractChatBot

class SlackBot(AbstractChatBot):

    def __init__(self, token, signing_secret):
        self.token = token
        self.signing_secret = signing_secret
        self.client = slack.WebClient(token=self.token)
        self.app = Flask(__name__)
        self.slack_event_adapter = SlackEventAdapter(self.signing_secret, '/slack/events', self.app)

    def run(self):
        self.app.run(debug=True)

    def send_message(self, channel, message):
        self.client.chat_postMessage(channel=channel, text=message)

    def send_image(self, channel, file_path, initial_comment):
        try:
            response = self.client.files_upload(
                file=file_path,
                initial_comment=initial_comment,
                channels=channel
            )
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")

    def listen_messages(self, callback):
        @self.slack_event_adapter.on('message')
        def message(payload):
            event = payload.get('event', {})
            user_id = event.get('user')
            text = event.get('text')
            
            # Ignore messages from the bot itself
            if user_id == self.client.auth_test()["user_id"]:
                return
            
            # Pass the event to the provided callback
            callback(event)

if __name__ == "__main__":
    # Create an instance of the SlackBot
    bot = SlackBot("<Your Token>", "<Your SIGNING SECRET>")

    # Logic for processing incoming messages
    def my_callback(event):
        channel_id = event.get('channel')
        text = event.get('text')
        
        if text == "hi":
            bot.send_message(channel_id, "Hello")
        
        if text == "image":
            bot.send_image(channel_id, '/home/pragnakalpdev23/mysite/slack_file_display/download (2).jpg', 'This is a sample Image')

    bot.listen_messages(my_callback)
    bot.run()

