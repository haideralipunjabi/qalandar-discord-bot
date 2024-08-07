import discord
from discord.ext import commands
import json
from math import remainder
import subprocess
import psutil
from datetime import datetime as dt
from datetime import timedelta as td
import os
from constants import TEMP_FOLDER, Channels, RECEIPTS_PATH
from scripts.scanner import Scanner
import logging
import calendar


def format_seconds(delta):
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    msg = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    if days:
        msg = f"{days} days, " + msg
    return msg


def memory():
    memory = psutil.virtual_memory()
    avail = round(memory.available / 1024.0 / 1024.0, 1)
    total = round(memory.total / 1024.0 / 1024.0, 1)
    return f"{avail} MB free / {total} MB total ({memory.percent}%)"


def disk():
    disk = psutil.disk_usage("/")
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free / 1024.0 / 1024.0 / 1024.0, 1)
    total = round(disk.total / 1024.0 / 1024.0 / 1024.0, 1)
    return f"{free} GB free / {total} GB total ({disk.percent}%)"


def cpu():
    cpu = psutil.cpu_freq()
    current = round(cpu.current / 1000.0, 1)
    total = round(cpu.max / 1000.0, 1)
    return f"{current} GHz / {total} GHz ({psutil.cpu_percent()}%)"


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        logging.info("Started SystemCog")

    async def cog_check(self, ctx):
        return ctx.channel.id == Channels.PI_HOME_SERVER

    @commands.command(help="Get System Uptime")
    async def uptime(self, ctx):
        boot_time = psutil.boot_time()
        diff = dt.now() - dt.fromtimestamp(boot_time)
        await ctx.send(
            f":clock1230: Boot at: {dt.fromtimestamp(boot_time).strftime('%I:%M:%S %p - %d/%m/%Y')}"
        )
        await ctx.send(f":timer: Running for: {format_seconds(diff)}")

    @commands.command(help="Get System Stats")
    async def stats(self, ctx):
        await ctx.send(f"Memory: {memory()}")
        await ctx.send(f"Disk: {disk()}")
        await ctx.send(f"CPU: {cpu()}")

    @commands.command(help="Scan Image")
    async def scanImage(self, ctx, dpi=300, filename="scanned_image.jpg"):
        await ctx.send("Scanning Image...")
        scanner = Scanner()
        if not scanner.available:
            await ctx.send("Scanner Offline")
            return
        if not filename.endswith("jpg"):
            filename += ".jpg"
        filepath = os.path.join(TEMP_FOLDER, filename)
        try:
            scanner.scanImage(filepath, dpi)
            await ctx.send(file=discord.File(filepath))
        except Exception as e:
            await ctx.send(f"An Error Occured: {e}")

    @commands.command(help="Scan PDF")
    async def scanPDF(self, ctx, dpi=300, filename="scanned_document.pdf"):
        await ctx.send("Scanning PDF...")
        scanner = Scanner()
        if not scanner.available:
            await ctx.send("Scanner Offline")
            return
        if not filename.endswith("pdf"):
            filename += ".pdf"
        filepath = os.path.join(TEMP_FOLDER, filename)
        try:
            scanner.scanPDF(filepath, dpi)
            await ctx.send(file=discord.File(filepath))
        except Exception as e:
            await ctx.send(f"An Error Occured: {e}")

    @commands.command(help="Scan Receipt")
    async def scanReceipt(self, ctx, month=None, year=None, name="receipt"):
        now = dt.now()
        scanner = Scanner()
        if not scanner.available:
            await ctx.send("Scanner Offline")
            return
        if month and year:
            try:
                month = dt.strptime(month, "%B").month
                year = dt.strptime(year, "%Y").year
            except Exception as e:
                await ctx.send(f"Exception: {e}")
                return
        if not month and not year:
            month = now.month
            year = now.year
        if not month or not year:
            await ctx.send("Provide both month and year")
            return
        month = calendar.month_name[month]
        if not name.endswith(".pdf"):
            name = name + ".pdf"
        filepath = os.path.join(TEMP_FOLDER, name)
        await ctx.send("Scanning PDF...")
        try:
            scanner.scanPDF(filepath, 300)
            await ctx.send(file=discord.File(filepath))
            os.system(f"rclone mkdir {RECEIPTS_PATH}/{year}/{month}")
            os.system(f"rclone copy {filepath} {RECEIPTS_PATH}/{year}/{month}/")
        except Exception as e:
            await ctx.send(f"An Error Occured: {e}")
