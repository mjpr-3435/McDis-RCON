from ...modules import *
from ...classes import *
from ...utils import *

def uploader_embed(client: McDisClient) -> discord.Embed:
    state       = 'Running' if client.uploader.is_running else 'Closed'
    overwrite   = str(client.uploader.overwrite)

    embed = discord.Embed(
        title = f'> Uploader Manager',
        colour = embed_colour)\
        .add_field(inline = True, name = '', value = 
            f'Si el uploader está activo, todos los archivos que se suban a este canal se subiran a la dirección establecida.')\
        .add_field(inline = True, name = '', value = 
            f'`'
            f'• Overwrite:              '[:-len(overwrite)] + overwrite + '\n'
            f'• State:                  '[:-len(state)]     + state     + '\n'
            f'`')\
        .add_field(inline = False, name = '', value = 
            f'**Path to upload:**```{emoji_pin} {mcdis_path(client.uploader.path_to_upload)}```')
  
    return embed