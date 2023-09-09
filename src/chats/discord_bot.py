from random import choice
import discord
from discord.ext import commands
from infrastructure.bot_abstract import AbstractChatBot
from models.logger_model import LoggerConfig
from models.paper_model import Schedule
from service.api_consumer import ResearchPaperSearcher

config = LoggerConfig(name="DiscordBot", log_file="DiscordBot.log")
logger = config.get_logger()
class DiscordBot(AbstractChatBot):
    def __init__(self, token, 
                 research_paper_searcher: ResearchPaperSearcher, 
                 crondict: dict,
                 schedule: Schedule,
                 prefix='!'):
        super().__init__(token, research_paper_searcher, crondict, schedule, prefix)
        self.intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix=self.prefix, intents=self.intents)
        
        self.register_events()
        self.register_commands()

    def get_channel_if(self, channel_name: str):
        target_channel = discord.utils.get(self.bot.get_all_channels(), name=channel_name)
        return target_channel

    def register_events(self):
        @self.bot.event
        async def on_ready():
            await self.run()
            self.scheduler.start()

        # If more events are needed, they can be added here

    def register_commands(self):
        @self.bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
        async def nine_nine(ctx):
            brooklyn_99_quotes = [
                'I\'m the human form of the emoji.',
                'Bingpot!',
                'Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.'
            ]
            response = choice(brooklyn_99_quotes)
            await ctx.send(response)

        # If more commands are needed, they can be added here

    async def notify(self, message):
        try:
            await self.bot.wait_until_ready()
            channel = self.get_channel_if(self.schedule.channel)
            if channel:
                await channel.send(message)
        except Exception as e:
            logger.error(f"Error notifying channel: {e}")

    async def start_bot(self):
        await self.bot.start(self.token)

    def __del__(self):
        if self.scheduler:
            self.scheduler.shutdown()
