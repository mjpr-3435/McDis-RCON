from ..modules import *
from ..classes import *
from ..utils import *

class CommandsView          (discord.ui.View):
    def __init__(self, client : McDisClient, process: Process):
        super().__init__(timeout = None)
        self.client = client
        self.process = process
        self.options = self._get_options()

        self.add_item(CommandSelect     (self.client, self.options))
        self.add_item(BackButton        (self.client))
        self.add_item(UpdateButton      (self.client))
        self.add_item(DirButton         (self.client))
    
    def _get_options(self):
        options = []
        commands = os.listdir(self.process.path_commands)
        commands.sort()

        options.append(discord.SelectOption(
            label = self.client._('[New Command]'), 
            emoji = emoji_new_command,
            value = '__NEW_COMMAND__'))

        for file in commands:
            if file.endswith('.yml'):
                options.append(discord.SelectOption(
                    label = file.removesuffix('.yml'), 
                    value = file))
                
        return options[:25]

class CommandSelect            (discord.ui.Select):
    def __init__(self, client: McDisClient, options: list):
        super().__init__(placeholder = client._('Select a command'), options = options)
        self.view : CommandsView
        
    async def callback(self, interaction: discord.Interaction):
        from .FilesManagerCommand import CommandEmbed, CommandView

        if self.values[0] != '__NEW_COMMAND__':
            await interaction.response.edit_message(
                embed = CommandEmbed(self.view.client, self.view.process, self.values[0]),
                view = CommandView(self.view.client, self.view.process, self.values[0]))
        
        elif len(self.view.options) == 25: 
            await interaction.response.send_message(
                self.view.client._('✖ At the moment, only up to 24 commands are allowed.'),
                ephemeral = True)
        
        else:
            class message_modal(discord.ui.Modal, title = self.view.client._('New command')):
                name = discord.ui.TextInput(
                    label = self.view.client._('Command name'), 
                    style = discord.TextStyle.paragraph)
            
                async def on_submit(modal, interaction: discord.Interaction):
                    file = f'{str(modal.name)[:40]}.yml'

                    if file in os.listdir(self.view.process.path_commands):
                        await interaction.response.send_message(
                            self.view.client._('✖ There is already a command with that name.'), 
                            ephemeral = True)
                        return
                    
                    template = os.path.join(package_path, 'templates','md_command.yml')
                    new_command = os.path.join(self.view.process.path_commands, file)
                    shutil.copy(template, new_command)
                    
                    await interaction.response.edit_message(
                        embed = CommandEmbed(self.view.client, self.view.process, file), 
                        view = CommandView(self.view.client, self.view.process, file))
    
            await interaction.response.send_modal(message_modal())

class BackButton                (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_arrow_left, style = discord.ButtonStyle.gray)
        self.view : CommandsView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManager import FilesManagerEmbed, FilesManagerView

        await interaction.response.edit_message(
            embed = FilesManagerEmbed(self.view.client, self.view.process.path_files),
            view = FilesManagerView(self.view.client, self.view.process.path_files)
        )

class UpdateButton              (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_update, style = discord.ButtonStyle.gray)
        self.view : CommandsView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed = CommandsEmbed(self.view.client, self.view.process),
            view = CommandsView(self.view.client, self.view.process)
        )

class DirButton                 (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_dir, style = discord.ButtonStyle.gray)
        self.view : CommandsView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManager import FilesManagerEmbed, FilesManagerView

        await interaction.response.edit_message(
            embed = FilesManagerEmbed(self.view.client, self.view.process.path_commands),
            view = FilesManagerView(self.view.client, self.view.process.path_commands)
        )

class CommandsEmbed             (discord.Embed):
    def __init__(self, client : McDisClient, process: Process):
        super().__init__(title = f'> {mcdis_path(process.path_commands)}', colour = embed_colour)
        self.client = client

        self.description = self.client._(
            'In the dropdown below, you will find various predefined commands.\n'
            'Select the one you wish to use.')

        self.set_footer(text = f'{184 * blank_space}\n{client._("Dropdown:")}')
