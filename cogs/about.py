import discord
from discord.ext import commands
import json


def load_changelog():
    with open('storage/changelog.json', 'r') as f:
        data = json.load(f)
        recent_version = data[-1]
    return recent_version['version'], recent_version['date']


class AboutMe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.version, self.date = load_changelog()

    @commands.Cog.listener()
    async def on_ready(self):
        print('* AboutMe cog is online.')

    @commands.command(name='about')
    async def about(self, ctx):
        embed = discord.Embed(
            title='Merle Ambrose',
            description='*Headmaster of Ravenwood School of Magical Arts*',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/733788698277052438/1107984909789835285/merle-ambrose.png')
        embed.set_footer(text=f'Version {self.version} as of {self.date}.')
        embed.set_author(name='Wizard101 Bot', icon_url='https://cdn.discordapp.com/attachments/733788698277052438/1107984909789835285/merle-ambrose.png')
        embed.add_field(name='My prefix:', value='\"`/`\"', inline=True)
        embed.add_field(name='Need help?', value='Type `/help` for assistance!', inline=True)
        embed.add_field(name='List of Commands', value='* birthday\n * ping\n * register_counter\n * snipe', inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(AboutMe(client))
