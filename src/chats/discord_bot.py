import discord
from discord.ext import commands

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, world!')

bot.run(TOKEN)
