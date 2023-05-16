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
        self.birthdays[ctx.author.id] = date.date().isoformat()
        await ctx.send(f"I've remembered your birthday as {date}.")

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
