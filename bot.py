import discord
import os
from discord.ext import commands, tasks
import cogs
import click
from constants import BASE_FOLDER, TEMP_FOLDER
import utils
from dotenv import load_dotenv
import logging

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
if not token:
    logging.error("Discord Token not found!")
    exit()

healthchecks_url = os.getenv("HEALTHCHECKS_ENDPOINT")

logging.info(f"Base Folder: {BASE_FOLDER}")

if not os.path.exists(TEMP_FOLDER):
    logging.info(f"Creating temp folder at: {TEMP_FOLDER}")
    os.mkdir(TEMP_FOLDER)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(hours=1)
async def ping_healthchecks():
    os.system(f"curl {healthchecks_url} > /dev/null")

@click.group
def cli():
    pass


@cli.command()
def dump_data():
    click.echo("Running dump_data")

    @bot.event
    async def on_ready():
        utils.dump_data(bot)
        await bot.close()

    bot.run(token)


@cli.command
def clean_temp_folder():
    os.system(f"rm -rf {TEMP_FOLDER}/*")


@cli.command()
def run():
    @bot.event
    async def setup_hook() -> None:
        await bot.add_cog(cogs.SystemCog(bot))
        await bot.add_cog(cogs.SocialCog(bot))
        await bot.add_cog(cogs.CalendarCog(bot))

    @bot.event
    async def on_ready():
        await ping_healthchecks()
        ping_healthchecks.start()

    bot.run(token)


if __name__ == "__main__":
    cli()
