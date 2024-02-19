import discord
from discord.ext import commands
from constants import Channels
from scripts.calendar_gen import generate_pdf
from datetime import datetime as dt


class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Started CalendarCog")

    async def cog_check(self, ctx):
        return ctx.channel.id == Channels.PI_HOME_SERVER

    @commands.command(help="Generate Printable Calendar")
    async def calendar(self, ctx, month, year):
        try:
            month = dt.strptime(month, "%b").month
            year = dt.strptime(year, "%Y").year
            f = generate_pdf(month, year)
            await ctx.send(file=discord.File(f))
        except Exception as e:
            await ctx.send(f"Exception: {e}")
