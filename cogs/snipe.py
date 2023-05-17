import discord
from discord.ext import commands


class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sniped_messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Snipe cog is online.')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sniped_messages[message.guild.id] = (
            message.content, message.author, message.channel.name, message.created_at)

    @commands.command()
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.sniped_messages[ctx.guild.id]

        except:
            await ctx.channel.send("Couldn't find a message to snipe!")
            return

        embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}")
        embed.set_footer(text=f"Deleted in : #{channel_name}")

        await ctx.channel.send(embed=embed)


async def setup(client):
    await client.add_cog(Snipe(client))
