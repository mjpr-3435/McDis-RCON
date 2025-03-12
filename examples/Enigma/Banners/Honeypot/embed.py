import discord

from .config import *

def banner_honeypot() -> discord.Embed:
    embed = discord.Embed(
        title='> ENIGMA HONEYPOT',
        colour=config['embed_colour']
    ).add_field(inline=True, name='DONT SEND MESSAGE', value=(
        "Any message sent here will be considered a violation of server rules and will trigger an automatic ban without warning.\n\n"
        "\n"
        "This channel is intended solely for security purposes to protect our server from possible malicious activities, such as sending unwanted messages (spam) or abuse attempts."
    )).add_field(inline=True, name='NO ENVIAR MENSAJES', value=(
        "Cualquier mensaje enviado será considerado una violación a las reglas del servidor y obtendrás un baneo automático sin aviso.\n\n"
        "\n"
        "Este canal está destinado únicamente a fines de seguridad para proteger nuestro servidor de posibles actividades maliciosas, como el envío de mensajes no deseados (spam) o intentos de abuso."
    )).set_thumbnail(url=config['Thumbnail'])
    embed.set_image(url=config['Honeypot PNG'])
    return embed