from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def commands_views(client: McDisClient, process: Process) -> discord.ui.View:
    from .files_manager import files_manager_views
    from .command import command_views
    
    commands = os.listdir(process.path_commands)
    commands.sort()
    options = []

    options.append(discord.SelectOption(label = client._('[New Command]'), emoji= emoji_new_command,value = 'New Command'))

    for file in commands:
        if file.endswith('.yml'):
            options.append(discord.SelectOption(label = file[:-4], value = file) )
    
    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
        
        @discord.ui.select( placeholder = client._('Select a command'), 
                            options = options[:25])
        async def farm_command_selection(self, interaction: discord.Interaction, selection: discord.ui.Select):
            if selection.values[0] != 'New Command':
                await interaction.response.edit_message( embed = command_embed(process, selection.values[0], 0), view = command_views(process, selection.values[0]))
            else:
                if len(commands) == 24: 
                    await interaction.response.send_message(client._('✖ At the moment, only up to 24 commands are allowed.'), ephemeral = True)
                    return
                
                class message_modal(discord.ui.Modal, title = client._('New command')):
                    name = discord.ui.TextInput(label = client._('Command name'), style = discord.TextStyle.paragraph)
                
                    async def on_submit(modal, interaction: discord.Interaction):
                        file = f'{str(modal.name)[:40]}.yml'
                        if file in commands:
                            await interaction.response.send_message(client._('✖ There is already a command with that name.'), ephemeral = True)
                            return
                        
                        template = os.path.join(package_path, 'templates','md_command.yml')
                        new_command = os.path.join(process.path_commands, file)
                        shutil.copy(template, new_command)
                        await interaction.response.edit_message( embed = command_embed(process, file, 0), 
                                                                view = command_views(process, file))
        
                await interaction.response.send_modal(message_modal())
                
        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(embed = files_manager_embed(process.path_files), view = files_manager_views(process.path_files))

        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(embed = commands_embed(process), view = commands_views(process))
        
        @discord.ui.button( label = emoji_dir,
                            style = discord.ButtonStyle.gray)
        async def files_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(embed = files_manager_embed(process.path_commands), view = files_manager_views(process.path_commands))

    return views()
