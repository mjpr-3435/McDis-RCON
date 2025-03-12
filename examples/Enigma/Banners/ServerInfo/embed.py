import discord

from datetime import datetime
from .config import config

def banner_server_info() -> discord.Embed:
    embed = discord.Embed(
        title='> Server Information',
        colour=config['embed_colour']
    ).add_field(inline=False, name='> What is Enigma?', value=(
        "Enigma is introduced as a Technical and Decorative"
        "Minecraft server, focused on the pursuit of a rewarding experience"
        "through fun and collaboration in project creation.\n"
        "Our primary focus lies in building an environment where"
        "participants can enjoy their gaming time while working on both"        
        "technical and decorative projects.\n"
    )).add_field(inline=False, name='> Characteristics', value=(
        "Currently, the server operates on Minecraft Java Edition version 1.17.1."
        "The languages used within the platform are Spanish and English."
        "The use of easyPlaceMode (Litematica) is authorized exclusively"
        "when building schematics for decorative purposes."
        "It's worth noting that the server is hosted in Germany."
    )).set_thumbnail(url=config['Thumbnail'])
    return embed


def banner_host_information() -> discord.Embed:
    years = int(((datetime.today()-datetime.strptime(config['Foundation Date'], "%Y-%m-%d")).days)//365.25)
    days = int((datetime.today()-datetime.strptime(config['Foundation Date'], "%Y-%m-%d")).days%365.25)
    
    if years == 0:
        active_time = f'- Active time: `{days} days`'
    elif days == 0:
        active_time = f'- Active time: `{years} years`'
    else:
        active_time = f'- Active time: `{years} years {days} days`'

    embed = discord.Embed(
        title='Host Information',
        colour=config['embed_colour']
    ).add_field(inline=False, name='', value=(
    "```asciidoc\n"
    "Type::       Dedicated Server\n"
    "Location::   Germany\n"
    "Processor::  AMD Ryzen 9 7950X3D\n"
    "Servers::    SMP/CMP/Mirror/Building\n"
    "Storage::    2 x 1.92 TB NVMe SSD\n"
    "RAM::        128 GB DDR5\n"
    "```"
    )).add_field(inline=True, name='', value=(
        "> **Carpet Rules**\n"
        "- CarefulBreak\n"
        "- CommandCameraMode\n"
        "- CommandHat\n"
        "- CtrlQCraftingFix\n"
        "- DefaultLoggers mobcaps,tps\n"
        "- DragonEggBedrockBreaking\n"
        "- EssentialCarefulBreak\n"
        "- FlippinCactus\n"
        "- MissingTools\n"
        "- OptimizedTNT\n"
        "- PlacementRotationFix\n"
        "- ShadowItemMode\n"
        "- SpectatorPlayersUsePortals\n"
        "- StackableShulkerBoxes\n"
        "- StackableShulkersInInventories\n"
        "- XpNoCooldown\n"
        "\n\n"
        "> **Social Media**\n"
        "- <:Enigma_Tech_Linktree:1327731556378214583> TikTok\n"
        "- <:Enigma_Tech_Twitch:1327726615836364820> Twtich\n"
        "- <:Enigma_Tech_Twitter:1327732027893743676> Twitter\n"
        "- <:Enigma_Tech_Youtube:1327725346879049879> Youtube\n"
        
    )).add_field(inline=True, name='', value=(
        "> **Mods**\n"
        "- BlueMap\n"
        "- Carpet-Addons\n"
        "- Carpet-Addons-Not-Found\n"
        "- Carpet-Extra\n"
        "- Carpet-Shadow\n"
        "- Chronos-Carpet-Addons\n"
        "- Dropfullcarts\n"
        "- Essentialaddons\n"
        "- Fabric-Carpet\n"
        "- Lithium\n"
        "- PCA-Protocol\n"
        "- Servux\n"
        "- Smoothboot\n"
        "- Spark\n"
        "- Starlight\n"
        "- Syncmatica\n"
        "\n\n"
        "> **Information**\n"
        f"{active_time}\n"
        "- Fundation: `02/03/2024`\n"
        "- Version: `1.17.1`\n"
        f"- Host: `EnigmaHosting`"
    )).set_thumbnail(url=config['Thumbnail'])
    return embed


def banner_enigma_map() -> discord.Embed:
    embed = discord.Embed(
        title='> Enigma Map',
        colour=config['embed_colour']
    ).add_field(inline=False, name='', value=( 
        "You can see the enigma tech map and its players in real time by clicking on the following link.\n\n"
        "`It is recommended to activate the “Hardware Acceleration”"
        "option found in the settings of your browser of choice.`\n"
        "\n\n"
        f":globe_with_meridians: [Overviewer Enigma:]({config['Overviewer Link']})"
    )).set_thumbnail(url=config['Thumbnail'])
    embed.set_image(url=config['Overviewer PNG'])
    return embed
