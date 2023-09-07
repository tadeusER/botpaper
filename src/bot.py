import os
import yaml
import aiocron
from chats.discord_bot import DiscordBot
# Suponiendo que tengas un SlackBot similar al DiscordBot
# from chats.slack_bot import SlackBot
from infrastructure.api_abstract import APIExtraction

class ArticleBot:
    def __init__(self, strategy, chat_bot, schedule, extraction_tokens=None, bot_token=None):
        self.strategy = strategy
        self.chat_bot = chat_bot
        self.extraction_tokens = extraction_tokens or {}
        self.bot_token = bot_token

        @self.chat_bot.bot.event
        async def on_ready():
            print(f'Conectado como: {self.chat_bot.bot.user}')

            for schedule_item in schedule:
                app = schedule_item.get('app')
                token = self.extraction_tokens.get(app)
                
                if app == "discord" and token:
                    self.chat_bot = DiscordBot(token=self.bot_token, prefix="!")
                # elif app == "slack" and token:  # Si decides implementar Slack
                #     self.chat_bot = SlackBot(token=self.bot_token)

                exists = await self.chat_bot.channel_exists(schedule_item.get('channel'))
                if not exists:
                    print(f"Channel {schedule_item.get('channel')} doesn't exist or bot has no permissions.")

                cron_time = schedule_item.get('cron_schedule', '')
                if cron_time:
                    @aiocron.crontab(cron_time)
                    async def cronjob():
                        for keyword in schedule_item.get('search_keywords', []):
                            articles = self.get_articles(keyword)
                            for article in articles:
                                await self.chat_bot.send_message(schedule_item.get('channel'), article)

        async def message_callback(message):
            if message.content.startswith('!articles'):
                articles = self.get_articles()
                await message.channel.send('\n'.join(articles))

        self.chat_bot.listen_messages(message_callback)

    def get_articles(self, keyword=None):
        return self.strategy.extract(keyword)

    def run(self):
        self.chat_bot.connect()

