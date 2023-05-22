import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, time
import asyncio
from airtable import Airtable

def load_table():
    with open('storage/token.txt', 'r') as file:
        lines = [line.strip().split(': ') for line in file.readlines()]
        for item in lines:
            if item[0] == 'base-id':
                token = item[1]
            if item[0] == 'api-token':
                api_pat = item[1]
        table = Airtable(token, api_key=api_pat).table('birthdays')
    return table

def validate_date(date):
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']

    for fmt in formats:
        try:
            return datetime.strptime(date, fmt).date().isoformat()
        except ValueError:
            pass

    raise ValueError(f'No valid date format found for {date}')


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.table = load_table()
        self.check_birthdays.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Birthdays cog is online.')

    def find_record(self, user_id):
        table = self.table.get(fields={'user-id': user_id})['records']
        for item in table:
            if item['fields']['user-id'] == user_id:
                return item
        return None

    @commands.command()
    async def remember_birthday(self, ctx):
        # validate the date
        date = validate_date(ctx.message.content.split()[1])
        print(date)

        # check if the user has already registered a birthday
        if self.find_record(str(ctx.author.id)) is not None:
            embed = discord.Embed(title='Warning!', description=f'<@{ctx.author.id}> has already registered a birthday!',
                                    color=0xeed202)
            embed.set_footer(text='Use /forget_birthday to forget your birthday.')
            await ctx.send(embed=embed)
            return

        # register the birthday
        self.table.create({'user-id': str(ctx.author.id), 'birthday': date})
        await ctx.send(embed=discord.Embed(title='Success!', description=f'I\'ve remembered your birthday as {date}.', color=0x4bb543))

    @commands.command()
    async def forget_birthday(self, ctx):
        # check if the user has registered a birthday
        if self.find_record(str(ctx.author.id)) is None:
            embed = discord.Embed(title='Warning!', description=f'<@{ctx.author.id}> has not registered a birthday!',
                                    color=0xeed202)
            embed.set_footer(text='Use /remember_birthday to remember your birthday.')
            await ctx.send(embed=embed)
            return

        # forget the birthday
        self.table.delete(self.find_record(str(ctx.author.id))['id'])
        await ctx.send(embed=discord.Embed(title='Success!', description=f'I\'ve forgotten <@{ctx.author.id}>\'s birthday.', color=0x4bb543))

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        """Check if today is someone's birthday."""
        today = datetime.now().date().isoformat()
        for record in self.table.get(fields={'user-id': self.client.id})['records']:
            birthday = record['fields']['birthday']
            if datetime.strptime(birthday, '%Y-%m-%d').month == datetime.strptime(today,'%Y-%m-%d').month and datetime.strptime(birthday, '%Y-%m-%d').day == datetime.strptime(today, '%Y-%m-%d').day:
                user = self.client.get_user(record['fields']['user-id'])
                if user:
                    await user.send('Happy Birthday!')

    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        """Ensure the loop waits until bot is ready and then starts at midnight."""
        await self.client.wait_until_ready()

        now = datetime.now()
        midnight = datetime.combine(now + timedelta(days=1), time(0))
        seconds_until_midnight = (midnight - now).seconds
        await asyncio.sleep(seconds_until_midnight)


async def setup(client):
    await client.add_cog(Birthdays(client))
