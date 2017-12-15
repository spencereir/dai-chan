from logger import logger

async def purge(message, client):
    if message.server is None:
        await client.send_message(message.channel, "This function may not be used in PM's")
        return

    messages = list(reversed(client.messages))
    deleted = 0
    to_delete = 0
    for m in message.content.split(' '):
        if m.isdigit():
            to_delete = int(m)

    logger.log_msg('INFO', 'Deleting {} messages from {}/{}'.format(to_delete, message.server, message.channel))

    if to_delete > len(messages):
        await client.send_message(message.channel, "There are not enough messages to delete this many; as many as {} will be deleted".format(to_delete))

    ind = 0
    while deleted < to_delete and ind < len(messages):
        if messages[ind] != message and messages[ind].channel == message.channel and (not message.mentions or messages[ind].author in message.mentions):
            await client.delete_message(messages[ind])
            deleted += 1
        ind += 1
