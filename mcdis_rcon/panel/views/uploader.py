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
                    response = client.is_valid_mcdis_path(modal.name.value, check_if_dir = True)

                    if response == True:
                        client.uploader.path_to_upload = un_mcdis_path(modal.name.value)
                        await interaction.response.edit_message(embed = uploader_embed(client))
                    else:
                        await interaction.response.send_message(response, ephemeral = True)

            await interaction.response.send_modal(edit_path())
        
        @discord.ui.button( label = 'Close' if client.uploader.is_running else 'Run',
                            style = discord.ButtonStyle.gray)
        async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if client.uploader.is_running:
                client.uploader.is_running = False
            else:
                client.uploader.is_running = True

            button.label = 'Close' if client.uploader.is_running else 'Run'
            await interaction.response.edit_message(embed = uploader_embed(client), view = self)

        @discord.ui.button( label = 'Do Not Overwrite' if client.uploader.overwrite else 'Overwrite',
                            style = discord.ButtonStyle.gray)
        async def overwrite_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if client.uploader.overwrite:
                client.uploader.overwrite = False
            else:
                client.uploader.overwrite = True

            button.label = 'Do Not Overwrite' if client.uploader.overwrite else 'Overwrite'
            await interaction.response.edit_message(embed = uploader_embed(client), view = self)

    return views()