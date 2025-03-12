import discord

from .config import *

def banner_member_info() -> discord.Embed:
    embed = discord.Embed(
        title='> Members Info',
        colour=config['embed_colour']
    ).add_field(inline=False, name='> Servers IP & Seed', value=(
        "Here you can find the ips and versions of the different servers and the seed with which the server started."
        "\n"
        "||```asciidoc\n"
        "Network  1.17.1::\n"
        "smp.enigmahosting.com\n"
        "Creative 1.20.4::\n"
        "creative.enigmahosting.com\n"
        "Building 1.20.4::\n"
        "plugins.enigmahosting.com\n"
        "```||"
        "\n\n"
        "> **SMP Seed**\n"
        "||```-409265062656536628```||\n"
        "Use `/server` to move between SMP, CMP and Mirror."
    )).set_thumbnail(url=config['Thumbnail'])
    return embed

def banner_smp_rules() -> discord.Embed:
    embed = discord.Embed(
        title='> Rules',
        colour=config['embed_colour']
    ).add_field(inline=True, name='> SMP Rules', value=(
        "- If you're unable to play for a period of time, don't worry, just let us know via the inactivity channel and return when you're able and feel like it.\n"
        "- If you're unfamiliar with how to use a farm, please refrain from using it. Instead, ask a knowledgeable member to teach you.\n"
        "- If you accidentally break a farm or mechanism, inform a member/admin.\n"
        "- When using Litematica, follow a layer by layer approach. Only move on to the next layer once the previous one is complete (with exceptions).While easyplace is allowed, be careful with redstone and similar components.\n"
        "- Duplication of elytras, sponges, and falling blocks is permitted only for staff members.\n"        
        "- Exploration of the world is prohibited to prevent overloading of the map\n"
    )).add_field(inline=True, name='> Reglas del SMP', value=(
        "- Si no puedes jugar durante un periodo de tiempo, no te preocupes, avísanos a través del canal de inactividad y vuelve cuando puedas y te apetezca.\n"
        "- Si no estás familiarizado con el uso de una granja, abstente de utilizarla. En su lugar, pide a un miembro experto que te enseñe.\n"
        "- Si accidentalmente rompes una granja o mecanismo, informa a un miembro/admin.\n"
        "- Cuando utilice Litematica, siga un enfoque por capas. Pasa a la siguiente capa sólo cuando hayas completado la anterior (salvo excepciones).Aunque easyplace está permitido, ten cuidado con redstone y componentes similares.\n"
        "- La duplicación de elytras, esponjas y bloques que caen sólo está permitida para los miembros del staff.\n"        
        "- La exploración del mundo está prohibida para evitar la sobrecarga del mapa.\n"
    )).add_field(inline=False, name='', value=(
        "**Any breach of these rules may lead to a sanction or a ban from the server.**\n"
    )).set_thumbnail(url=config['Thumbnail'])
    return embed

def banner_project_info() -> discord.Embed:
    embed = discord.Embed(
        title='> Projec Info',
        colour=config['embed_colour']
    ).add_field(inline=True, name='> How it works?', value=(
        "In Enigma, we work on multiple projects simultaneously. To make this task more efficient, we have decided to assign colors to the channels of each project, as follows."
        "\n\n"
        "🟢 : Working at SMP\n"
        "🔵 : Passive projects\n"
        "🟡 : Preparing the schematic\n"
        "🔴 : In development\n"
        "⚪ : Reporting bugs"
        "\n\n"
        "When a project is labeled 🟢 : Working at SMP ,you can find the instructions in the to-do-list-smp, and the coordinates and schematics in the pinned messages of the channel."
        "The schematics are also shared on Syncmatica."
    )).add_field(inline=True, name='> Cómo funciona?', value=(
        "En Enigma trabajamos en varios proyectos simultáneamente. Para hacer esta tarea más eficiente, asignamos colores a los canales de cada proyecto, de la siguiente manera."
        "\n\n"
        "🟢 : Trabajando en SMP\n"
        "🔵 : Proyectos pasivos\n"
        "🟡 : Preparando el esquema\n"
        "🔴 : En desarrollo\n"
        "⚪ : Informando de errores"
        "\n\n"
        "Si el proyecto lleva la etiqueta 🟢 : Trabajando en SMP, puedes encontrar las instrucciones en la lista de tareas pendientes (to-do-list-smp), y las coordenadas y"
        "esquemas en los mensajes anclados del canal y Syncmatica."
    )).set_thumbnail(url=config['Thumbnail'])
    return embed

def banner_additional_files() -> discord.Embed:
    embed = discord.Embed(
        title='> Additional Files',
        colour=config['embed_colour']
    ).add_field(inline=True, name='> Mods', value=(
        f"[Version 1.17.1:]({config['Mods 1.17']})\n"
        f"[Version 1.20.1:]({config['Mods 1.20']})\n"
        f"[Version 1.21.1:]({config['Mods 1.21']})\n"
    )).add_field(inline=True, name='> Other Stuff', value=(
        f"[Enigma KCP:]({config['KCP']})\n"
        f"[Enigma Digy Pack:]({config['DigPack']})\n"
        f"[Enigma Cape:]({config['EnigmaCape']})\n"
    )).add_field(inline=False, name='> Other Channels', value=(
        "FAQ\n"
        "TechincalStuff\n"
        "IGN\n"
    )).set_thumbnail(url=config['Thumbnail'])
    embed.set_image(url=config['Other PNG'])
    return embed