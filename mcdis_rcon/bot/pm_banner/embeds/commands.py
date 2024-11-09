from ...pm_functions import *
from ...pm_classes import *
from ...modules import *

from ...loader import _, config, panel
from ...pm_loader import servers, networks, processes

def commands_embed(process: Process) -> discord.Embed:

    embed = discord.Embed(
        title = f'> {mcdis_path(process.path_commands)}',
        colour = embed_colour,
        description = 
        _('In the dropdown below, you will find various predefined commands.\n'
        'Select the one you wish to use.'))\
    .set_footer(text= 184*blank_space + '\n' + _('Dropdown:'))
  
    return embed