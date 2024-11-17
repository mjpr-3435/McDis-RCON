from ...modules import *
from ...classes import *
from ...utils import *

def processes_embed(client: McDisClient, path: str, processes: list[psutil.Process], page : int = 1) -> discord.Embed:
    mrkd_processes = ''

    for i in range( max_processes * (page-1), min( max_processes*page, len(processes))):
        mrkd_processes = mrkd_processes + mrkd(processes[i],i) + '\n'
        
    embed = discord.Embed(
        title = client._('> Processes in `{}`').format(mcdis_path(path)),
        colour = embed_colour,
        description = '```asciidoc\n' + mrkd_processes + '```' if len(mrkd_processes)!= 0 else f'```{client._("There are no processes in this folder.")}```')
    if len(mrkd_processes)!= 0: embed.set_footer(text = 184*blank_space + '\n' + client._('If you want to close a process, select it from the dropdown below.'))
    else: embed.set_footer(text = 185*blank_space)
    
    return embed

def         mrkd                (process: psutil.Process, index: int) -> str:
    name = process.name()
    ram = ram_usage(process)
    
    cwd = os.path.relpath(process.cwd(),os.getcwd())
    cwd = truncate(cwd, 32)

    cmd_1 = ' '.join([os.path.basename(cmd) if os.path.exists(cmd) else cmd for cmd in process.cmdline()])
    cmd_1 = truncate(cmd_1, 32)

    mrkd_string = f"{index + 1}. {name + blank_space*(20-len(name))}\n   ↳ Cwd:: {12*blank_space} {mcdis_path(cwd)}\n   ↳ Ram Usage:: {6*blank_space} {ram}\n   ↳ Command:: {8*blank_space} {cmd_1}\n"

    return mrkd_string