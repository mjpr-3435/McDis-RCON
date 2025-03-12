import discord
from discord.ext import commands
from .config import *

async def friends_creator(client: commands.Bot) -> None:
    try: 
        channel = await client.fetch_channel(config['Channel ID'])
        if isinstance(channel, discord.Thread):
            await channel.edit(archived = False)
    except: 
        print('EnFriendsDisords: canal no encontrado. Saliendo...')
        return

    messages =  [msg async for msg in channel.history(limit = None, oldest_first = True)]
    messages_to_send = []

    for key, value in config['Discords'].items():
        dummy = "\n".join([f"- {key}: {value}" for key, value in value.items()])
        dummy = f'> {key}:\n{dummy}'
        messages_to_send.append(dummy)

    if not messages:
        for i in range(len(messages_to_send)): await channel.send(messages_to_send[i])

    elif len(messages) == len(messages_to_send) and all([message.author.id == client.user.id for message in messages]):
        for i in range(len(messages_to_send)): await messages[i].edit(content = messages_to_send[i])
    
    else:
        await channel.purge(limit = 100)
        await friends_creator(client)
