import discord
import asyncio
import sys
import datetime
from functools import reduce
import commands.general
import commands.random
import commands.parser

client = discord.Client()

def log_msg(lvl, msg):
    print('{} : {:%Y-%m-%d %H:%M:%S} : {}'.format(lvl, datetime.datetime.now(), msg))

@client.event
async def on_ready():
    log_msg('INFO', 'Logged in as {}'.format(client.user.name))

@client.event
async def on_message(message):
    content = message.content
    intended_recipient = False
    for bn in bot_names:
        if content.lower().startswith(bn + ' '):
            intended_recipient = True
            content = content[len(bn)+1:]
            break
    if not intended_recipient:
        return
    
    for (k, v) in command_map.items():
        for cmd in k.split('|'):
            if content.lower().startswith(cmd + ' '):
                await client.send_message(message.channel, commands.parser.option_call(v, content[len(cmd)+1:]))
       
bot_names = ['dai', 'dai-chan', 'daichan', 'daiyousei', 'small cirno']

command_map = {
    'choose|pick': commands.random.choose,
    'roll': commands.random.roll,
    'say': commands.general.say
}

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <bot-token>'.format(sys.argv[0]))
    else:
        client.run(sys.argv[1])
