import discord
from discord.ext import commands
import os

# get the token from the tokens.txt file
with open('../tokens.txt', 'r') as file:
    lines = [line.strip().split(': ') for line in file.readlines()]
    for item in lines:
        if item[0] == 'wizgang':
            token = item[1]

# create the bot
client = commands.Bot(command_prefix='/', intents=discord.Intents.all())
client.remove_command("help")


# load the cogs
@client.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
        else:
            print("Unable to load pycache folder.")


# on ready -- print bot info
@client.event
async def on_ready():
    print('Bot is online.')
    print(f'Version: {discord.__version__}')
    await client.change_presence(activity=discord.Game(name='Wizard101', type=3))


# run the client
client.run(token)
