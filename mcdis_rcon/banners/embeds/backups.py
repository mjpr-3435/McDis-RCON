from ...modules import *
from ...classes import *
from ...utils import *

def backups_embed(client: McDisClient, process: Process) -> discord.Embed:
    pattern = os.path.join(process.path_bkps, f'{process.name} [1-{client.config["Backups"]}].zip')
    bkps = glob.glob(pattern)
    bkps.sort()
            
    mrkd_zips = ''

    for i in range(len(bkps)):
        dummy = mrkd_zips + mrkd(bkps[i],i) + '\n'
        if len(dummy) > 1990: 
            mrkd_zips = mrkd_zips + '\n...'
            break
        mrkd_zips = dummy

    embed = discord.Embed(
        title = f'> {mcdis_path(process.path_bkps)}',
        colour = embed_colour,
        description = mrkd_zips)\
        
    if len(mrkd_zips)!= 0: embed.set_footer(text = 184*blank_space + '\n' + client._('If you want to load or delete a backup, select it from the dropdown below.'))
    else: 
        embed.description = f'```{client._("No backups were found.")}```'
        embed.set_footer(text = 185*blank_space)

    return embed


def         mrkd                (file: str, index: int) -> str:
    date = datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y-%m-%d %H:%M:%S")
        
    size = get_path_size(file)
    local_timezone_offset = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone

    hours_offset = local_timezone_offset // 3600
    minutes_offset = (local_timezone_offset % 3600) // 60

    mrkd_string = f"```asciidoc\n{index + 1}. {os.path.basename(file)}\n   ↳ Disk Usage:: {5*blank_space} {size}\n   ↳ Date:: {11*blank_space} {date} (UTC {hours_offset:03}:{minutes_offset:02})```"

    return mrkd_string