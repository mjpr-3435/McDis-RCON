from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def banner_views(client: McDisClient) -> discord.ui.View:
    from .files_manager import files_manager_views
    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)

        @discord.ui.button( label = 'Processes',
                            style = discord.ButtonStyle.gray)
        async def processes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .banner_processes import banner_processes
            await interaction.response.edit_message(view = banner_processes())

        @discord.ui.button( label = 'Files',
                            style = discord.ButtonStyle.gray)
        async def files_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(embed = files_manager_embed(), view = files_manager_views(), ephemeral = True)

        @discord.ui.button( label = 'Uploader',
                            style = discord.ButtonStyle.gray)
        async def uploader_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .uploader import uploader_views
            await interaction.response.send_message(embed = uploader_embed(), view = uploader_views(), ephemeral = True)

        @discord.ui.button( label = 'Flask',
                            disabled = not client.config['Flask']['Allow'],
                            style = discord.ButtonStyle.gray)
        async def flask_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .flask import flask_views
            await interaction.response.send_message(embed = flask_embed(), view = flask_views(), ephemeral = True)
        
        @discord.ui.button( label = 'Restart',
                            style = discord.ButtonStyle.red)
        async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(embed = files_manager_embed(), view = files_manager_views(), ephemeral = True)
  
    return views()

async def restart(client: McDisClient, response: discord.Message):
    """elif message.content.lower() == f'{mcdis_prefix}restart mcdis':
    await message.delete()
    response = await message.channel.send(_('Checking if there are open processes...'))
    await asyncio.sleep(2)

    await restart(response)"""

    any_process_open = lambda: any([process.state() in ['Open','Initializing'] for process in processes])

    if any_process_open():
        await response.edit(content = client._('Closing processes...'))
        print(client._('Closing processes...'))
        await asyncio.sleep(2)

    for process in processes: process.stop()
    
    i = 60
    while i > 0 and any_process_open():
        await response.edit(content = client._('Processes will be forcibly closed in {} seconds...').format(i))
        print(client._('Processes will be forcibly closed in {} seconds...').format(i))
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        i -= 1
        await asyncio.sleep(1)
    
    if any_process_open():
        for process in processes:
            process.kill()
        
        print(client._('Processes forcibly closed.'))
    else:
        print(client._('Processes closed.'))

    print(client._('Restarting...'))

    await response.edit(content = client._('Restarting...'))
    await response.delete(delay = 2)

    await asyncio.sleep(3)

    command = sys.argv[0]
    os.execv(command, sys.argv)