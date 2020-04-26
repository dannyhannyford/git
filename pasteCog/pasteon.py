import discord
from discord.ext import commands, tasks
from redbot.core import commands, Config, checks
import asyncio
from collections import namedtuple
import io
import re
from datetime import datetime, timedelta
import pytz
from pytz import timezone
#from .pastepoints import PastePoints
from redbot.core.utils.chat_formatting import box, pagify

upemoji_id = 397064398830829569
downemoji_id = 272737368916754432
channel_id = 331655111644545027

class Pasteon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374544)
        default_guild = {}
        self.config.register_guild(**default_guild)
        self.config.register_user(karmon=0)

    @commands.command()
    async def setppmonth(self, ctx: commands.Context, user: discord.Member, amount: int):
        """Resets a user's Monthly karma."""
        await self.config.user(user).karmon.set(amount)
        await ctx.send("{}'s karma has been set.".format(user.display_name))

    @commands.command()
    async def ppmonth(self, ctx: commands.Context, top: int = 10):
        channel = self.bot.get_channel(id = channel_id)
        thirty = self.get_30_days()
        msglst = await channel.history(limit=1000, after=thirty, oldest_first = False).flatten()
        for msg in msglst:
            for react in msg.reactions:
                await self._check_reaction(react, react.count)
        '''LEADERBOARD PART'''
        reverse = True
        if top == 0:
            top = 10
        elif top < 0:
            reverse = False
            top = -top
        members_sorted = sorted(
            await self._get_all_members(ctx.bot), key=lambda x: x.karmon, reverse=reverse
        )

        if len(members_sorted) < top:
            top = len(members_sorted)
        topten = members_sorted[:top]
        highscore = ""
        place = 1
        for member in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += "{} | ".format(member.name).ljust(18 - len(str(member.karmon)))
            highscore += str(member.karmon) + "\n"
            place += 1
        if highscore != "":
            for page in pagify(highscore, shorten_by=12):
                await ctx.send(box(page, lang="py"))
        else:
            await ctx.send("No one has any karma 🙁")
        '''this clears all users karma counts after leaderboard is posted'''
        for msg in msglst:
            for react in msg.reactions:
                await self._check_reaction(react, -react.count)

    async def _get_all_members(self, bot):
        member_info = namedtuple("Member", "id name karmon")
        ret = []
        for member in bot.get_all_members():
            if any(member.id == m.id for m in ret):
                continue
            karmon = await self.config.user(member).karmon()
            if karmon ==0:
                continue
            ret.append(member_info(id=member.id, name=str(member), karmon=karmon))
        return ret

    async def _check_reaction(self, reaction: discord.Reaction, count):
        message = reaction.message
        (author, channel, guild) = (message.author, message.channel, message.guild)
        if (reaction.emoji.id == upemoji_id):
            await self._add_karmon(author, count)
        if (reaction.emoji.id == downemoji_id):
            await self._add_karmon(author, -count)

    async def _add_karmon(self, user: discord.User, amount: int):
        settings = self.config.user(user)
        karmon = await settings.karmon()
        await settings.karmon.set(karmon + amount)
    '''past 30 days object'''
    def get_30_days(self):
        lastmonth = datetime.utcnow()
        lastmonth -= timedelta(days =30)
        return lastmonth

def setup(bot):
    bot.add_cog(Pasteon(bot))