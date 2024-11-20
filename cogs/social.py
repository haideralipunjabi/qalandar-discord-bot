from discord.ext import commands

from constants import Channels
from scripts import viral
import logging


class SocialCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        logging.info("Started SocialCog")

    async def cog_check(self, ctx):
        return ctx.channel.id == Channels.RANDOM

    @commands.command(help="Send Message to Viral Anonymous Box")
    async def viral(self, ctx, uid, content="🤗", amount=10):
        await ctx.send(f"Sending user: {uid} Message: {content} - {amount} times")
        try:
            viral.run(uid, amount, content)
        except Exception as e:
            await ctx.send(e)
