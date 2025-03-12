import discord

from .config import *

def banner_grinder() -> discord.Embed:
    embed = discord.Embed(
        title='> Application Form',
        colour=config['embed_colour']
    ).add_field(inline=True, name='Grinder & Digger', value=(
        "Responsible for collecting materials and constructing mechanisms, as well as performing general activities needed within the server."
        "\n"
        "Members passionate about mining, dedicated to excavating and removing blocks in their path."
        "\n"
        f"[:scroll: Clic here to apply]({config['En Form']})\n"
    )).add_field(inline=True, name='Grinder/Digger', value=(
        "Encargados de recolectar los materiales y construir mecanismos, así como el de realizar las actividades generales necesarias dentro del servidor."
        "\n"
        "Miembros apasionados por la minería,y dedicados a excavar y eliminar los bloques a su paso."
        "\n"
        f"[:scroll: Clic here to apply]({config['Es Form']})\n"
    )).set_thumbnail(url=config['Thumbnail'])
    embed.set_image(url=config['Grinder PNG'])
    return embed

def banner_cmp() -> discord.Embed:
    embed = discord.Embed(
        title='> Application Form',
        colour=config['embed_colour']
    ).add_field(inline=True, name='CMP & Redstoner', value=(
        "Specialists in creating unique mechanisms and developing new applications of redstone within the game."
        "\n"
        "- StorageTech.\n"
        "- SlimeTech.\n"
        "- Mob Farming.\n"        
        "- Tree Farming.\n"
        "- Other."
        "\n"
        f"[:scroll: Clic here to apply]({config['En Form']})\n"
    )).add_field(inline=True, name='CMP & Redstoner', value=(
        "Especialistas en la creación de mecanismos únicos y desarrollo de nuevas aplicaciones de la redstone."
        "\n"
        "- StorageTech.\n"
        "- SlimeTech.\n"
        "- Mob Farming.\n"        
        "- Tree Farming.\n"
        "- Other."
        "\n"
        f"[:scroll: Clic here to apply]({config['En Form']})\n"
    )).set_thumbnail(url=config['Thumbnail'])
    embed.set_image(url=config['CMP PNG'])
    return embed

def banner_builder() -> discord.Embed:
    embed = discord.Embed(
        title='> Application Form',
        colour=config['embed_colour']
    ).add_field(inline=True, name='Builder', value=(
        "Members tasked with designing and decorating perimeters and farms within the server."
        "\n\n"
        "- Arceon.\n"
        "- Axiom.\n"
        "- GoPaint.\n"
        "- World Edit.\n"
        "- Other."
        "\n"
        f"[:scroll: Clic here to apply]({config['En Form']})\n"
    )).add_field(inline=True, name='Decorador', value=(
        "Responsables del diseño y decoración de los perímetros y granjas dentro del servidor."
        "\n\n"
        "- Arceon.\n"
        "- Axiom.\n"
        "- GoPaint.\n"
        "- World Edit.\n"
        "- Other."
        "\n"
        f"[:scroll: Clic here to apply]({config['En Form']})\n"
    )).set_thumbnail(url=config['Thumbnail'])
    embed.set_image(url=config['Builder PNG'])
    return embed

def banner_faq() -> discord.Embed:
    embed = discord.Embed(
        title='> Frequently Asked Questions',
        colour=config['embed_colour']
    ).add_field(inline=True, name='FAQ EN', value=(
        "- **1) I deleted my world and I have no photos, I can apply?**\n"
        "Unfortunately, photos are a mandatory requirement to evaluate your form. If you are unable to provide pictures, your form will be automatically rejected.\n\n"
        "- **2) I don't have Minecraft Premium, can I submit the form?**\n"
        "Although you can complete the form, please note that our server is exclusively for players with Minecraft Premium.\n\n"
        "- **3) I don't have technical Minecraft experience, can I be accepted?**\n" 
        "We are looking for players with at least some experience in the technical side of Minecraft. If you don't have that experience, it will be difficult to get your form approved.\n\n"
        "- **4) I submitted my form, how long does it take to get a response?**\n"        
        "The answer to your application will be sent by direct message (DM) within a maximum of one week.\n"
    )).add_field(inline=True, name='FAQ ES', value=(
        "- **1) He borrado mi mundo y no tengo fotos, ¿puedo aplicar?**\n"
        "Lamentablemente, las fotos son obligatorias al evaluar su formulario. Si no proporciona fotos, su formulario será rechazado automáticamente.\n\n"
        "- **2) No tengo Minecraft Premium, ¿puedo enviar el formulario?**\n"
        "Aunque puedes rellenar el formulario, nuestro servidor es exclusivo para jugadores con Minecraft Premium.\n\n"
        "- **3) No tengo experiencia técnica en Minecraft, ¿puedo ser aceptado?**\n" 
        "Buscamos jugadores con al menos algo de experiencia en la parte técnica de Minecraft. Si no tienes esa experiencia, será difícil que tu formulario sea aprobado.\n\n"
        "- **4) He enviado mi formulario, ¿cuánto tiempo se tarda en recibir una respuesta?**\n"        
        "La respuesta a tu solicitud se enviará por mensaje directo (DM) en un plazo máximo de una semana.\n"
    ))
    return embed