import json
import click
import os
import logging


def dump_data(bot):
    logging.info("Dumping Data")
    for channel in bot.get_all_channels():
        click.echo(f"{channel.name}\t{channel.id}")
