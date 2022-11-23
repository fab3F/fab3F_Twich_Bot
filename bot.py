#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "fab3F"
__copyright__ = "Twitch Bot"
__credits__ = ["NinjaBunny9000: https://github.com/NinjaBunny9000/barebones-twitch-bot"]

__license__ = "MIT License"
__version__ = "1.1"
__contact__ = {
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

    if not await bot.handle_commands(ctx):
        await ctx.send(f'Dieser Befehl ist nicht verfügbar')


@bot.command(name='discord')
async def on_discord(ctx):
    """
    Runs when the discord command was issued in the Twitch chat and sends the
    current discord link to the chat
    """
    await ctx.send(f'Du kannst dem Discord unter https://fab3F.github.io/link/discord beitreten')
    return True


@bot.command(name='help')
async def on_help(ctx):
    """
    Runs when the help command was issued in the Twitch chat and sends the
    current project link to the chat
    """
    await ctx.send(f'Unter https://fab3F.github.io/projects/twitchbot findest du alle Infos zum Bot')
    return True


@bot.command(name='zählen')
async def on_count(ctx):
    """
    Runs when the count command was issued in the Twitch chat and sends the 
    current count to the chat
    """
    count = get_count()
    await ctx.send(f'Momentaner Stand: {count}')
    return True


@bot.command(name='plus')
async def on_add(ctx):
    """
    Runs when the add command was issued in the Twitch chat and adds to the 
    count
    """
    # check if user who issued the command is a mod
    if (ctx.author.is_mod):

        # parse add command
        command_string = ctx.message.content
        # remove '!add' and white space
        command_string = command_string.replace('!plus', '').strip()
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
            await ctx.send(f'Zahl wurde zu {count} aktualisiert')

    else:
        await ctx.send(f'Du bist kein Moderator')

    return True


@bot.command(name='minus')
async def on_sub(ctx):
    """
    Runs when the add command was issued in the Twitch chat and subtracts from 
    the count
    """
    # check if user who issued the command is a mod
    if (ctx.author.is_mod):

        # parse add command
        command_string = ctx.message.content
        # remove '!sub' and white space
        command_string = command_string.replace('!minus', '').strip()
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
            await ctx.send(f'Zahl wurde zu {count} aktualisiert')

    else:
        await ctx.send(f'Du bist kein Moderator')

    return True


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
