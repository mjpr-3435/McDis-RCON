from ...pm_functions import *
from ...pm_classes import *
from ...modules import *

from ...loader import _, config, panel
from ...pm_loader import servers, networks, processes

def command_embed(process: Process, file_name : str, action : int) -> discord.Embed:

    embed = discord.Embed(
        title = f'{file_name[:-4]}',
        colour = embed_colour)
    
    with open(os.path.join(process.path_commands,file_name), 'r') as file:
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping = 2, sequence = 4, offset = 2)
        yaml.preserve_quotes = True

        data = yaml.load(file)
    
    embed.add_field(name = f'> {_("Description")}:', inline = False, value = data['Description'])
    embed.add_field(name = f'> {list(data.keys())[action+1]}:', 
                    inline = False, 
                    value = ''.join([f'```{truncate(value,56)}```' for value in list(data.values())[action+1]]))
    
    embed.set_footer(text = 184*blank_space + '\n' + _('Use {} to iterate over the options.').format(emoji_update))
    
    return embed