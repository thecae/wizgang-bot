import discord
import pandas.errors
from discord.ext import commands
import pandas as pd
from airtable import Airtable

# get the token from the tokens.txt file
def load_table():
    with open('storage/token.txt', 'r') as file:
        lines = [line.strip().split(': ') for line in file.readlines()]
        for item in lines:
            if item[0] == 'base-id':
                token = item[1]
            if item[0] == 'api-token':
                api_pat = item[1]
        table = Airtable(token, api_key=api_pat).table('counter')
    return table

class Counter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.table = load_table()

    def find_record(self, channel_id):
        table = self.table.get(fields={'channel-id': channel_id})['records']
        for item in table:
            if item['fields']['channel-id'] == channel_id:
                return item
        return None

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Counter cog is online.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def register_counter(self, ctx):
        # check if the channel is already registered
        if self.find_record(str(ctx.channel.id)) is not None:
            await ctx.send(embed=discord.Embed(title='Warning!', description=f'<#{ctx.channel.id}> is already registered!', color=0xeed202))
            return

        # register the channel
        self.table.create({'channel-id': str(ctx.channel.id), 'count': 0, 'last-user': '0'})
        await ctx.send(embed=discord.Embed(title='Success!', description=f'Counter registered for <#{ctx.channel.id}>.', color=0x4bb543))

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore messages sent by bots
        if message.author.bot:
            return

        # get the record
        record = self.find_record(str(message.channel.id))

        # ignore messages not in a registered channel
        if record is not None:
            # don't allow someone to count twice in a row
            if message.author.id == record['fields']['last-user']:
                return

            try:
                # attempt to eval the expression
                res = pd.eval(message.content)
                current_count = record['fields']['count']

                # if valid and correct, increment the counter and change last user
                if res == current_count + 1:
                    self.table.update(record['id'], {'count': res, 'last-user': str(message.author.id)})
                    await message.add_reaction('✅')
                # if valid but incorrect, reset the counter and reset last user
                else:
                    await message.add_reaction('❌')
                    self.table.update(record['id'], {'count': 0, 'last-user': '0'})
                    embed = discord.Embed(
                        title=f'{message.author.nick} fucked it up!',
                        description=f'Count was ruined at **{current_count}**.  **{res}** was inputted instead.',
                        color=0xff9494
                    )
                    embed.set_footer(text='*The counter now resets at 1.*')
                    channel = self.client.get_channel(message.channel.id)
                    await channel.send(embed=embed)
            # expression failed, ignore it
            except (SyntaxError, pandas.errors.UndefinedVariableError):
                return


async def setup(client):
    await client.add_cog(Counter(client))
