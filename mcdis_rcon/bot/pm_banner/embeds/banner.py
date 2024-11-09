from ...pm_functions import *
from ...pm_classes import *
from ...modules import *

from ...loader import _, config, panel
from ...pm_loader import servers, networks, processes, flask_manager

def banner_embed() -> discord.Embed:

    cpu_info    = psutil.cpu_freq(), psutil.cpu_percent(interval=1)
    cpu_freq    = f'{int(cpu_info[0].current)} MHz'
    cpu_load    = f'{cpu_info[1]} %'
    cpu_temp    = get_cpu_temp()

    ram_info    = psutil.virtual_memory()
    ram_total   = f'{ram_info.total/(1024 ** 3):.1f} GB'
    ram_used    = f'{ram_info.used/(1024 ** 3):.1f} GB'
    ram_load    = f'{ram_info.percent:.1f} %'

    disk_info   = psutil.disk_usage("/")
    disk_total  = f'{disk_info.total/(1024 ** 3):.1f} GB'
    disk_used   = f'{disk_info.used/(1024 ** 3):.1f} GB'
    disk_load   = f'{disk_info.percent:.1f} %'
    
    bot_ram_used = f'{psutil.Process().memory_info().rss/(1024**2):.1f} MB'

    warnings = []
    if disk_info.percent > 90: 
        warning = f'{emoji_pin} ' + _('[Disk Usage]: Disk usage is over 90%.')
        warning += (66-len(warning))*blank_space
        warnings.append(warning)
    
    embed = discord.Embed(
            title = _('Server Panel'),
            colour = embed_colour,
            description = _('Here you will find an overview of the server resource usage. Additionally, McDis RCON recognizes the following commands in the following instances:\n') +
            f'- {_("Console")} : {" ".join([f"`{command}`" for command in console_commands])}' + '\n'
            f'- {_("Panel")  } : {" ".join([f"`{mcdis_prefix}{command}`" for command in panel_commands])}' )
    
    
    embed.add_field(name = _('> Server Resources'), inline = True, value =
            f'```asciidoc\n'
            f'CPU\n'
            f'Freq::           '[:-len(cpu_freq)] + cpu_freq + '\n'
            f'Load::           '[:-len(cpu_load)] + cpu_load + '\n'
            f'Temp::           '[:-len(cpu_temp)] + cpu_temp + '```')\
        .add_field(name = omit_space, inline = True, value =
            f'```asciidoc\n'
            f'RAM\n'
            f'Total::          '[:-len(ram_total)] + ram_total + '\n'
            f'Used::           '[:-len(ram_used)] + ram_used + '\n'
            f'Load::           '[:-len(ram_load)] + ram_load + '```')\
        .add_field(name = omit_space, inline = True, value =
            f'```asciidoc\n'
            f'Storage\n'
            f'Total::          '[:-len(disk_total)] + disk_total + '\n'
            f'Used::           '[:-len(disk_used)] + disk_used + '\n'
            f'Load::           '[:-len(disk_load)] + disk_load + '```')\

    i = 0
    for server in servers:
        if i%2 == 0 and i!= 0: embed.add_field(name = '', value = '', inline = False)
        i += 1
        
        state = server.state()
        ram_usage = server.ram_usage()
        disk_usage = server.disk_usage()
        
        embed.add_field(
            inline = True, 
            name = f'> <#{next(filter(lambda thread: server.name in thread.name, panel.threads)).id}>',
            value = 
                f'```asciidoc\n'
                f'Disk Usage::              '[:-len(disk_usage)] + disk_usage + '\n'
                f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '\n'
                f'State::                   '[:-len(state)] + state + '```')
    
    if len(servers)%2 == 1:
        embed.add_field(name = '', value = '', inline = True)
    
    embed.add_field(name = '', value = '', inline = False)
          
    for process in networks:
        ram_usage = process.ram_usage()

        embed.add_field(
            inline = True, 
            name = f'> <#{next(filter(lambda thread: process.name in thread.name, panel.threads)).id}>',
            value = 
                f'```asciidoc\n'
                f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '```')
    
    if len(networks)%2 == 0:
        embed.add_field(name = '', value = '', inline = False)

    embed.add_field(
        inline = True,
        name = f'> McDis RCON',
        value =
                f'```asciidoc\n'
                f'RAM Usage::               '[:-len(bot_ram_used)] + bot_ram_used + '```')
    
    if len(networks)%2 == 0:
        embed.add_field(name = '', value = '', inline = True)

    if warnings:
        embed.add_field(name = _('> Warnings'), inline = False, value = '\n'.join([f'`{warning}`' for warning in warnings]))
    return embed