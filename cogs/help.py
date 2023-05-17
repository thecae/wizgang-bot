import discord
from discord.ext import commands
import json


def load_changelog():
    with open('storage/changelog.json', 'r') as f:
        data = json.load(f)
        recent_version = data[-1]
    return recent_version['version'], recent_version['date']


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.version, self.date = load_changelog()

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Help cog is online.')

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title='Help',
            description='*Need help?*',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/733788698277052438/1107984909789835285/merle-ambrose.png')
        embed.set_footer(text=f'Version {self.version} as of {self.date}.')
        embed.set_author(
            name='Wizard101 Bot',
            icon_url='https://cdn.discordapp.com/attachments/733788698277052438/1107984909789835285/merle-ambrose.png'
        )
        embed.add_field(
            name='My prefix:',
            value='\"`/`\"',
            inline=True
        )
        embed.add_field(
            name='About Me:',
            value='Type `/about` to learn more!',
            inline=True
        )
        embed.add_field(
            name='/help',
            value='Returns this message',
            inline=False
        )
        embed.add_field(
            name='/ping',
            value='Returns the bot\'s latency',
            inline=False
        )
        embed.add_field(
            name='/remember_birthday',
            value='Enter your birthday as the argument and we\'ll send you a nice message on your birthday!',
            inline=False
        )
        embed.add_field(
            name='/snipe',
            value='Remembers the last deleted message and will snipe it for you!',
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Help(client))
