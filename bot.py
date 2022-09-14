#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "fab3F"
__copyright__   = "Twitch Bot"
__credits__     = ["k0nze: https://github.com/k0nze"]

__license__     = ""
__version__     = "1.0"
__contact__     = {
                    "Twitch": "https://fab3F.github.io/link/twitch",
                    "Youtube": "https://fab3F.github.io/link/youtube",
                    "Twitter": "https://fab3F.github.io/link/twitter",
                    "Instagram": "https://fab3F.github.io/link/instagram",
                    "Discord": "https://fab3F.github.io/link/discord",
                }

import os
import json

from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

# credentials
TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CHANNEL = os.environ.get('CHANNEL')

JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/data.json'


bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@bot.event
async def event_ready():
    """ Runs once the bot has established a connection with Twitch """
    print(f"{BOT_NICK} ist online!")


@bot.event
async def event_message(ctx):
    """ 
    Runs every time a message is sent to the Twitch chat and relays it to the 
    command callbacks 
    """

    # the bot should not react to itself
    if ctx.author.name.lower() == BOT_NICK.lower():
        return

    # relay message to command callbacks
    await bot.handle_commands(ctx)

@bot.command(name='discord')
async def on_count(ctx):
    """
    Runs when the discord command was issued in the Twitch chat and sends the
    current discord link to the chat
    """
    await ctx.send(f'du kannst dem Discord unter https://fab3F.github.io/link/discord beitreten')


@bot.command(name='count')
async def on_count(ctx):
    """
    Runs when the count command was issued in the Twitch chat and sends the 
    current count to the chat
    """
    count = get_count()
    await ctx.send(f'current count {count}')


@bot.command(name='add')
async def on_add(ctx):
    """
    Runs when the add command was issued in the Twitch chat and adds to the 
    count
    """
    # check if user who issued the command is a mod
    if(ctx.author.is_mod):

        # parse add command
        command_string = ctx.message.content
        # remove '!add' and white space
        command_string = command_string.replace('!add', '').strip()
        # parse int
        value = 0

        try:
            value = int(command_string) 
        except ValueError:
            value = 0

        if value > 0:
            # add to count
            count = get_count()
            count = count + value
            update_count(count)
            await ctx.send(f'updated count to {count}')


@bot.command(name='sub')
async def on_sub(ctx):
    """
    Runs when the add command was issued in the Twitch chat and subtracts from 
    the count
    """
    # check if user who issued the command is a mod
    if(ctx.author.is_mod):

        # parse add command
        command_string = ctx.message.content
        # remove '!sub' and white space
        command_string = command_string.replace('!sub', '').strip()
        # parse int
        value = 0

        try:
            value = int(command_string) 
        except ValueError:
            value = 0

        if value > 0:
            # subtract from count
            count = get_count()
            count = count - value
            update_count(count)
            await ctx.send(f'updated count to {count}')


def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['count']


def update_count(count):
    """ Updates the JSON file with count given """
    data = None

    with open(JSON_FILE) as json_file:
        data = json.load(json_file)

    if data is not None:
        data['count'] = count

    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


if __name__ == "__main__":
    # launch bot
    bot.run()
