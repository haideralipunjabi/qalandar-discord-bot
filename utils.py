import json
import click
import os


def dump_data(bot):
    print("Dumping Data")
    for channel in bot.get_all_channels():
        click.echo(f"{channel.name}\t{channel.id}")
