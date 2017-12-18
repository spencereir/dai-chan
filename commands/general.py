import datetime

def say(message):
    return message.content

logmode = ""

async def log(message, client):
    await client.send_message(message.channel, "[{}|{:<10}|{:%Y-%m-%d %H:%M:%S}] {}".format(logmode, message.author.name, datetime.datetime.now(), message.content))
    await client.delete_message(message)

async def set_logmode(message, client):
    global logmode
    logmode = message
    await client.send_message(message.channel, "Changed log mode to {}".format(logmode))
