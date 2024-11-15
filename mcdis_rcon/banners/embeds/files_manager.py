from ...modules import *
from ...classes import *
from ...utils import *

def files_manager_embed(client: McDisClient, path: str = '.', page = 1) -> discord.Embed:
    footer = f'Size: {get_path_size(path)}'

    _page = page - 1

    if os.path.isdir(path):
        files = os.listdir(path)
        files.sort()

        dirs = [file for file in files if os.path.isdir(os.path.join(path,file))]
        files = [file for file in files if os.path.isfile(os.path.join(path,file))]
        dirs_max_page = len(dirs)//99 + 1
        files_max_page = len(files)//99 + 1
        if page > dirs_max_page: dirs_footer = f'- (total: {len(dirs)})'
        else: dirs_footer = len(dirs) if len(dirs) < 99 else f"{1 + 99*_page} - {min(99*page, len(dirs))} (total: {len(dirs)})"
        if page > files_max_page: files_footer = f'- (total: {len(files)})'
        else: files_footer = len(files) if len(files) < 99 else f"{1 + 99*_page} - {min(99*page, len(files))} (total: {len(files)})"

        embed = discord.Embed(
                title = f"> **{mcdis_path(path)}**",
                color = embed_colour)\
        .add_field(name = '', inline = True , value = "\n\n".join([f'`{i+1 - 99*_page:02d} {emoji_dir } {dirs[i][:15] }`' for i in range(0, len(dirs ), 3)][33*_page:33*page]))\
        .add_field(name = '', inline = True , value = "\n\n".join([f'`{i+1 - 99*_page:02d} {emoji_dir } {dirs[i][:15] }`' for i in range(1, len(dirs ), 3)][33*_page:33*page]))\
        .add_field(name = '', inline = True , value = "\n\n".join([f'`{i+1 - 99*_page:02d} {emoji_dir } {dirs[i][:15] }`' for i in range(2, len(dirs ), 3)][33*_page:33*page]))\
        .add_field(name = '', inline = True , value = "\n\n".join([f'`{i+1 - 99*_page:02d} {emoji_file} {files[i][:15]}`' for i in range(0, len(files), 3)][33*_page:33*page]))\
        .add_field(name = '', inline = True , value = "\n\n".join([f'`{i+1 - 99*_page:02d} {emoji_file} {files[i][:15]}`' for i in range(1, len(files), 3)][33*_page:33*page]))\
        .add_field(name = '', inline = True , value = "\n\n".join([f'`{i+1 - 99*_page:02d} {emoji_file} {files[i][:15]}`' for i in range(2, len(files), 3)][33*_page:33*page]))\
        
        footer += f'     |     Dirs: {dirs_footer}     |     Files: {files_footer}'
    else:
        value = ''

        if not get_path_size(path, string = False) > request_size_limit:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    value =  file.read().replace("  ","")
            except: 
                pass
                
        embed = discord.Embed(
                title = f"> **{mcdis_path(path)}**",
                color = embed_colour,
                description = f'```\n{truncate(value,1990).replace("`","’")}```' if value else '')

        
        date = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d %H:%M:%S")
        local_timezone_offset = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone

        hours_offset = local_timezone_offset // 3600
        minutes_offset = (local_timezone_offset % 3600) // 60

        footer += f'     |     Date: {date} (UTC {hours_offset:03}:{minutes_offset:02})'
    embed.set_footer(text = (184)*blank_space + '\n' + f'{footer}')
    return embed