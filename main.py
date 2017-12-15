import discord
import asyncio
import sys
import datetime
import commands.general
import commands.random
import commands.parser
import commands.games
import commands.sound
from logger import logger
from config import config

client = discord.Client()

@client.event
async def on_ready():
    logger.log_msg('INFO', 'Logged in as {}'.format(client.user.name))

@client.event
async def on_message(message):
    intended_recipient = False
    for bn in config.bot_names:
        if message.content.lower().startswith(bn + ' '):
            intended_recipient = True
            message.content = message.content[len(bn)+1:]
            break
    if not intended_recipient:
        return

    logger.log_msg('INFO', 'Received message from {} on {}/{}, contents = {}'.format(message.author.name, message.server, message.channel, message.content))

    for (k, v) in config.command_map.items():
        for cmd in k.split('|'):
            if message.content.lower().startswith(cmd):
                message.content = message.content[len(cmd)+1:]
                response = await commands.parser.option_call(v, message)
                await client.send_message(message.channel, response)

    for (k, v) in config.interactive_command_map.items():
        for cmd in k.split('|'):
            if message.content.lower().startswith(cmd):
                message.content = message.content[len(cmd)+1:]
                await commands.parser.option_call(v, message, client)

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <bot-token>'.format(sys.argv[0]))
    else:
        client.run(sys.argv[1])
