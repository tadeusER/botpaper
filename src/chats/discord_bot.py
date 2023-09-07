import discord
from discord.ext import commands
from infrastructure.bot_abstract import AbstractChatBot

class DiscordBot(AbstractChatBot):

    def __init__(self, token, prefix):
        self.token = token
        self.prefix = prefix
        self.bot = commands.Bot(command_prefix=self.prefix)

    async def connect(self):
        await self.bot.start(self.token)

    async def disconnect(self):
        # Discord library uses `close` to disconnect a bot.
        await self.bot.close()

    async def send_message(self, channel, message):
        target_channel = discord.utils.get(self.bot.get_all_channels(), name=channel)
        if target_channel:
            await target_channel.send(message)

    async def listen_messages(self, callback):
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            await callback(message)



