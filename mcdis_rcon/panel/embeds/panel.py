from ...modules import *
from ...classes import *
from ...utils import *

def banner_embed(client: McDisClient) -> discord.Embed:

    warnings            = []
    mcdis_ram_used      = f'{psutil.Process().memory_info().rss/(1024**2):.1f} MB'
    mrkd_console_cmds   = " ".join([f"`{command}`" for command in console_commands])
    mrkd_panel_cmds     = " ".join([f"`{client.prefix}{command}`" for command in panel_commands])

    cpu_info            = psutil.cpu_freq(), psutil.cpu_percent(interval=1)
    cpu_freq            = f'{int(cpu_info[0].current)} MHz'
    cpu_load            = f'{cpu_info[1]} %'
    cpu_temp            = get_cpu_temp()

    ram_info            = psutil.virtual_memory()
    ram_total           = f'{ram_info.total/(1024 ** 3):.1f} GB'
    ram_used            = f'{ram_info.used/(1024 ** 3):.1f} GB'
    ram_load            = f'{ram_info.percent:.1f} %'

    disk_info           = psutil.disk_usage("/")
    disk_total          = f'{disk_info.total/(1024 ** 3):.1f} GB'
    disk_used           = f'{disk_info.used/(1024 ** 3):.1f} GB'
    disk_load           = f'{disk_info.percent:.1f} %'

    if disk_info.percent > 90: 
        warning = f'{emoji_pin} ' + client._('[Disk Usage]: Disk usage is over 90%.')
        warning += (66-len(warning))*blank_space
        warnings.append(warning)
    if client.uploader.is_running: 
        warning = f'{emoji_pin} ' + client._('[Uploader]: Uploader is currently running.')
        warning += (66-len(warning))*blank_space
        warnings.append(warning)
    if client.config['Flask']['Allow'] and client.flask.is_running == True: 
        warning = f'{emoji_pin} ' + client._('[Flask]: Flask is currently running.')
        warning += (66-len(warning))*blank_space
        warnings.append(warning)
    
    mrkd_warnings = '\n'.join([f'`{warning}`' for warning in warnings])

    embed = discord.Embed(
        title = client._('Server Panel'),
        colour = embed_colour,
        description = client._('Here you will find an overview of the server resource usage. Additionally, McDis RCON recognizes the following commands in the following instances:\n') +
        f'- {client._("Console")} : {mrkd_console_cmds}' + '\n'
        f'- {client._("Panel")  } : {mrkd_panel_cmds}' )\
    .add_field(name = client._('> Server Resources'), inline = True, value =
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
        f'Load::           '[:-len(disk_load)] + disk_load + '```')

    for i in range(len(client.servers)):
        if i%2 == 0 and i!= 0: embed.add_field(name = '', value = '', inline = False)

        state       = 'Running' if client.servers[i].is_running() else 'Closed'
        ram_usage   = client.servers[i].ram_usage()
        disk_usage  = client.servers[i].disk_usage()

        server_id = next(filter(lambda thread: client.servers[i].name in thread.name, client.panel.threads), None).id

        embed.add_field(
            inline = True, 
            name = f'> <#{server_id}>',
            value = 
                f'```asciidoc\n'
                f'Disk Usage::              '[:-len(disk_usage)] + disk_usage + '\n'
                f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '\n'
                f'State::                   '[:-len(state)] + state + '```')
        
    if len(client.servers)%2 == 1: embed.add_field(name = '', value = '', inline = True)
    embed.add_field(name = '', value = '', inline = False)
          
    for network in client.networks:
        ram_usage = network.ram_usage()
        network_id = next(filter(lambda thread: network.name in thread.name, client.panel.threads), None).id

        embed.add_field(
            inline = True, 
            name = f'> <#{network_id}>',
            value = 
                f'```asciidoc\n'
                f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '```')
    
    if len(client.networks)%2 == 0: embed.add_field(name = '', value = '', inline = False)

    embed.add_field(
        inline = True,
        name = '> McDis RCON',
        value =
                f'```asciidoc\n'
                f'RAM Usage::               '[:-len(mcdis_ram_used)] + mcdis_ram_used + '```')
    
    if len(client.networks)%2 == 0: embed.add_field(name = '', value = '', inline = True)

    if warnings: embed.add_field(name = client._('> Warnings'), inline = False, value = mrkd_warnings)
    
    return embed