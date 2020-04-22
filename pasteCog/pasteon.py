import discord
from discord.ext import tasks
from redbot.core import commands, Config
import asyncio
import re
from datetime import datetime
import pytz
from pytz import timezone

#general channel id
channel_id = 701921344748650557
class Pasteon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timechannel.start()

    """My custom cog"""

    @commands.command()
    async def mycog(self, ctx):

        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    @commands.command()
    async def channelname(self, ctx, new_name):
        channel_name = ctx.guild.get_channel(channel_id)
        await channel_name.edit(name= new_name)

    @tasks.loop(minutes = 1.0)
    async def timechannel(self):
        fmt = '%H:%M %Z'
        channel_name = self.bot.get_channel(channel_id)
        seattle = datetime.now(timezone('PST8PDT'))
        seattle = seattle.strftime(fmt)
        await channel_name.edit(name = seattle)
        await asyncio.sleep(0.1)

    @timechannel.before_loop
    async def before_timechannel(self):
        minutecheck = datetime.now(timezone('PST8PDT'))
        fmt2 = "%S"
        minutecheck = int(minutecheck.strftime(fmt2))
        minutecheck = 61 - (minutecheck % 60)
        await asyncio.sleep(minutecheck)

def setup(bot):
    bot.add_cog(Pasteon(bot))
