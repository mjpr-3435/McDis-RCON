from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def uploader_views(client: McDisClient) -> discord.ui.View:

    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)

        @discord.ui.button( label = emoji_pin,
                            style = discord.ButtonStyle.gray)
        async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            class edit_path(discord.ui.Modal, title = 'Edit path to upload'):
                name = discord.ui.TextInput(label = 'Path to upload', style = discord.TextStyle.short, default = mcdis_path(client.uploader.path_to_upload))
                
                async def on_submit(modal, interaction: discord.Interaction):
                    if client.is_valid_mcdis_path(modal.name.value):
                        client.uploader.path_to_upload = modal.name.value
                        await interaction.response.edit_message(embed = uploader_embed(client))

            await interaction.response.send_modal(edit_path())
        
        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if client.uploader.is_running == 'Closed':
                client.uploader.is_running = 'Running'
            else:
                client.uploader.is_running = 'Closed'

            await interaction.response.edit_message(embed = uploader_embed(client))

        @discord.ui.button( label = emoji_writing,
                            style = discord.ButtonStyle.gray)
        async def overwrite_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if client.uploader.overwrite:
                client.uploader.overwrite = False
            else:
                client.uploader.overwrite = True

            await interaction.response.edit_message(embed = uploader_embed(client))

    return views()