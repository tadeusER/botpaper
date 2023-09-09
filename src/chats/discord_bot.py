from random import random
import discord
from discord.ext import commands
from bot import ResearchBotScheduler
from infrastructure.bot_abstract import AbstractChatBot
from models.logger_model import LoggerConfig
from discord.ext import commands
from infrastructure.bot_abstract import AbstractChatBot
from models.logger_model import LoggerConfig
import discord


class DiscordBot:

    def __init__(self, token, prefix, ResearchBotSchedulerClass: ResearchBotScheduler):
        self.token = token
        self.prefix = prefix
        self.bot = commands.Bot(command_prefix=self.prefix)
        self.scheduler_class = ResearchBotSchedulerClass

        # Registering events and commands
        self.register_events()
        self.register_commands()
    def get_channel_if(self, channel_name: str):
        target_channel = discord.utils.get(self.bot.get_all_channels(), name=channel_name)
        return target_channel
    def register_events(self):
        @self.bot.event
        async def on_ready():
            print("Ready")
            self.scheduler_class.start_scheduler()

        # If more events are needed, they can be added here

    def register_commands(self):
        @self.bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
        async def nine_nine(ctx):
            brooklyn_99_quotes = [
                'I\'m the human form of the 💯 emoji.',
                'Bingpot!',
                'Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.'
            ]

            response = random.choice(brooklyn_99_quotes)
            await ctx.send(response)
        
        # If more commands are needed, they can be added here

    def run(self):
        self.bot.run(self.token)


