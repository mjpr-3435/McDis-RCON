from ...modules import *
from ...classes import *
from ...utils import *

def commands_embed(client: McDisClient, process: Process) -> discord.Embed:

    embed = discord.Embed(
        title = f'> {mcdis_path(process.path_commands)}',
        colour = embed_colour,
        description = 
        client._('In the dropdown below, you will find various predefined commands.\n'
        'Select the one you wish to use.'))\
    .set_footer(text= 184*blank_space + '\n' + client._('Dropdown:'))
  
    return embed