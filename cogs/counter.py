import discord
from discord.ext import commands
import json
import pandas as pd


def load_counters():
    try:
        with open('../storage/counters.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

class Counter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.counters = load_counters()

    def save_counters(self):
        with open('storage/counters.json', 'w') as f:
            json.dump(self.counters, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Counter cog is online.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def register_counter(self, ctx):
        # check if the channel is already registered
        if self.counters.get(ctx.channel.id) is not None:
            await ctx.send(embed=discord.Embed(title='Warning!', description=f'<#{ctx.channel.id}> is already registered!', color=0xeed202))
            return

        # register the channel
        self.counters[ctx.channel.id] = {'count': 0, 'last_user': ''}
        self.save_counters()
        await ctx.send(embed=discord.Embed(title='Success!', description=f'Counter registered for <#{ctx.channel.id}>.', color=0x4bb543))

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore messages sent by bots
        if message.author.bot:
            return

        # ignore messages not in a registered channel
        if self.counters.get(message.channel.id) is not None:
            current_count = self.counters[message.channel.id]['count']
            last_author = self.counters[message.channel.id]['last_user']

            # don't allow someone to count twice in a row
            if message.author.id == last_author:
                return

            try:
                # attempt to eval the expression
                res = pd.eval(message.content)

                # if valid and correct, increment the counter and change last user
                if res == current_count + 1:
                    self.counters[message.channel.id]['count'] = res
                    self.counters[message.channel.id]['last_user'] = message.author.id
                    self.save_counters()
                    await message.add_reaction('✅')
                # if valid but incorrect, reset the counter and reset last user
                else:
                    await message.add_reaction('❌')
                    self.counters[message.channel.id]['count'] = 0
                    self.counters[message.channel.id]['last_user'] = ''
                    self.save_counters()
                    embed = discord.Embed(
                        title=f'{message.author.nick} fucked it up!',
                        description=f'Count was ruined at **{current_count}**.  **{res}** was inputted instead.',
                        color=0xff9494
                    )
                    embed.set_footer(text='*The counter now resets at 1.*')
                    channel = self.client.get_channel(message.channel.id)
                    await channel.send(embed=embed)
            # expression failed, ignore it
            except SyntaxError:
                return


async def setup(client):
    await client.add_cog(Counter(client))
