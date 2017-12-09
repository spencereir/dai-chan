import asyncio

async def music(message, client):
    if message.author.voice.voice_channel is None:
        await client.send_message(message.channel, "You don't appear to be in a voice channel")
        return

    voice = await client.join_voice_channel(message.author.voice.voice_channel)
    player = await voice.create_ytdl_player(message.content, use_avconv=True)
    player.start()
    await asyncio.sleep(player.duration+5.0)
    await voice.disconnect()
