from ..modules import *
from ..classes import *
from ..utils import *

class FilesView             (discord.ui.View):
    def __init__(self, client: McDisClient):
        super().__init__(timeout = None)
        self.client = client

        self.add_item(UpdateButton              (self.client))
        self.add_item(StateButton               (self.client))
        self.add_item(OverwriteButton           (self.client))

class UpdateButton          (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = emoji_update, style=discord.ButtonStyle.gray)
        self.view: FilesView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed = FilesEmbed(self.view.client),
            view = FilesView(self.view.client)
        )

class StateButton           (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label = 'Fast Mode' if client.files_manager.fast_mode else 'Full Mode'
        super().__init__(label = label, style=discord.ButtonStyle.gray)
        self.view : FilesView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.files_manager.fast_mode = not self.view.client.files_manager.fast_mode

        self.label = 'Fast Mode' if self.view.client.files_manager.fast_mode else 'Full Mode'
        await interaction.response.edit_message(
            embed = FilesEmbed(self.view.client),
            view = self.view)

class FilesEmbed         (discord.Embed):
    def __init__(self, client : McDisClient):
        super().__init__(title = f'> {client._("Files Manager")}', colour=embed_colour)
        self.client = client
        
        self._add_description()
        self._add_status_field()

    def _add_description(self):
        self.add_field(inline = True, name = '', value = 
            self.client._('This banner lets you configure the File Manager functions.')
        )

    def _add_status_field(self):
        state = 'Fast' if self.client.files_manager.fast_mode else 'Full'
        overwrite = 'True' if self.client.files_manager.overwrite else 'False'
        
        self.add_field(inline = True, name = '', value =
            '`• Mode:                   '[:-len(state)] + state + '`\n'
            '`• Overwrite:              '[:-len(overwrite)] + overwrite + '`\n'
        )

class OverwriteButton       (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label = 'Overwrite' if client.files_manager.overwrite else 'Do Not Overwrite'
        super().__init__(label = label, style=discord.ButtonStyle.gray)
        self.view : FilesView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.files_manager.overwrite = not self.view.client.files_manager.overwrite

        self.label = 'Overwrite' if self.view.client.files_manager.overwrite else 'Do Not Overwrite'
        await interaction.response.edit_message(
            embed = FilesEmbed(self.view.client),
            view = self.view)