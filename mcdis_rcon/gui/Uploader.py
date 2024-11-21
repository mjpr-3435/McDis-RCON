from ..modules import *
from ..classes import *
from ..utils import *

class UploaderView          (discord.ui.View):
    def __init__(self, client : McDisClient):
        super().__init__(timeout=None)
        self.client = client

        self.add_item(UpdateButton      (self.client))
        self.add_item(EditButton        (self.client))
        self.add_item(StateButton       (self.client))
        self.add_item(OverwriteButton   (self.client))
        
class UpdateButton          (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_update, style = discord.ButtonStyle.gray)
        self.view : UploaderView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed = UploaderEmbed(self.view.client),
            view = UploaderView(self.view.client)
        )

class EditButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_pin, style = discord.ButtonStyle.gray)
        self.view : UploaderView

    async def callback(self, interaction: discord.Interaction):
        class EditPath(discord.ui.Modal, title = self.view.client._('Edit the path to upload')):
            name = discord.ui.TextInput(
                label = self.view.client._('Path to upload'),
                style = discord.TextStyle.short,
                default = mcdis_path(self.view.client.uploader.path_to_upload)
            )

            async def on_submit(modal, interaction: discord.Interaction):
                response = self.view.client.is_valid_mcdis_path(modal.name.value, check_if_dir = True)

                if response is True:
                    self.view.client.uploader.path_to_upload = un_mcdis_path(modal.name.value)
                    await interaction.response.edit_message(embed = UploaderEmbed(self.view.client))
                else:
                    await interaction.response.send_message(response, ephemeral = True)

        await interaction.response.send_modal(EditPath())

class StateButton           (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label = 'Close' if client.uploader.is_running else 'Run'
        super().__init__(label = label, style=discord.ButtonStyle.gray)
        self.view : UploaderView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.uploader.is_running = not self.view.client.uploader.is_running

        self.label = 'Close' if self.view.client.uploader.is_running else 'Run'
        await interaction.response.edit_message(embed = UploaderEmbed(self.view.client), view = self.view)

class OverwriteButton       (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label = 'Do Not Overwrite' if client.uploader.overwrite else 'Overwrite'
        super().__init__(label = label, style=discord.ButtonStyle.gray)
        self.view : UploaderView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.uploader.overwrite = not self.view.client.uploader.overwrite

        self.label = 'Do Not Overwrite' if self.view.client.uploader.overwrite else 'Overwrite'
        await interaction.response.edit_message(embed = UploaderEmbed(self.view.client), view = self.view)

class UploaderEmbed         (discord.Embed):
    def __init__(self, client : McDisClient):
        super().__init__(title = f'> {client._("Uploader Manager")}', colour=embed_colour)
        self.client = client
        
        self._add_description()
        self._add_status_field()
        self._add_path_field()

    def _add_description(self):
        self.add_field(inline = True, name = '', value = 
            self.client._('If the uploader is active, all files uploaded to this channel will be sent to the specified destination.')
        )

    def _add_status_field(self):
        state = 'Running' if self.client.uploader.is_running else 'Closed'
        overwrite = str(self.client.uploader.overwrite)
        
        self.add_field(inline = True, name = '', value =
            f'`'
            f'• Overwrite:              '[:-len(overwrite)] + overwrite + '\n'
            f'• State:                  '[:-len(state)] + state + '\n'
            f'`'
        )

    def _add_path_field(self):
        path_to_upload = mcdis_path(self.client.uploader.path_to_upload)
        
        self.add_field(inline = False, name = '', value =
            f'**{self.client._("Path to upload")}:**\n```{emoji_pin} {path_to_upload}```'
        )
