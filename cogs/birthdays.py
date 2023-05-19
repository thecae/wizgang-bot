import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, time
import asyncio
import json


def validate_date(date):
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']

    for fmt in formats:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass

    raise ValueError(f'No valid date format found for {date}')


def load_birthdays():
    try:
        with open('../storage/birthdays.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.birthdays = load_birthdays()
        self.check_birthdays.start()

    def save_birthdays(self):
        with open('birthdays.json', 'w') as f:
            json.dump(self.birthdays, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Birthdays cog is online.')

    @commands.command()
    async def remember_birthday(self, ctx):
        date = validate_date(ctx.message.content.split()[1])
        if self.birthdays.get(ctx.author.id) is not None:
            embed = discord.Embed(title='Warning!', description=f'<@{ctx.author.id}> has already registered a birthday!',
                                    color=0xeed202)
            embed.set_footer(text='Use /forget_birthday to forget your birthday.')
            await ctx.send(embed=embed)
            return
        self.birthdays[ctx.author.id] = date.date().isoformat()
        await ctx.send(embed=discord.Embed(title='Success!', description=f'I\'ve remembered your birthday as {date}', color=0x4bb543))

    @commands.command()
    async def forget_birthday(self, ctx):
        if self.birthdays.get(ctx.author.id) is None:
            embed = discord.Embed(title='Warning!', description=f'<@{ctx.author.id}> has not registered a birthday!',
                                    color=0xeed202)
            embed.set_footer(text='Use /remember_birthday to remember your birthday.')
            await ctx.send(embed=embed)
        self.birthdays.pop(ctx.author.id)
        await ctx.send(embed=discord.Embed(title='Success!', description=f'I\'ve forgotten <@{ctx.author.id}>\'s birthday.', color=0x4bb543))

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        """Check if today is someone's birthday."""
        today = datetime.now().date().isoformat()
        for user_id, birthday in self.birthdays.items():
            if datetime.strptime(birthday, '%Y-%m-%d').month == datetime.strptime(today,'%Y-%m-%d').month and datetime.strptime(birthday, '%Y-%m-%d').day == datetime.strptime(today, '%Y-%m-%d').day:
                user = self.client.get_user(user_id)
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
