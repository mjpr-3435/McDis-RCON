from ...modules import *
from ...classes import *
from ...utils import *

def uploader_embed(client: McDisClient) -> discord.Embed:

    embed = discord.Embed(
        title = f'> Uploader Manager',
        colour = embed_colour)\
        .add_field(inline = True, name = '', value = 
            f'Si el uploader está activo, todos los archivos que se suban a este canal se subiran a la dirección establecida.')\
        .add_field(inline = True, name = '', value = 
            f'`'
            f'• Overwrite:              '[:-len(str(client.uploader.overwrite))] + str(client.uploader.overwrite)   + '\n'
            f'• State:                  '[:-len(client.uploader.is_running)]          + client.uploader.is_running            + '\n'
            f'`')\
        .add_field(inline = False, name = '', value = 
            f'**Path to upload:**```{emoji_pin} {mcdis_path(client.uploader.path_to_upload)}```')
  
    return embed