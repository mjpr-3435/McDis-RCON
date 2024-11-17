from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def panel_views(client: McDisClient) -> discord.ui.View:
    
    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)

        @discord.ui.button( label = 'Processes',
                            style = discord.ButtonStyle.gray)
        async def processes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .manager import manager
            await interaction.response.edit_message(
                view = manager(client))

        @discord.ui.button( label = 'Files',
                            style = discord.ButtonStyle.gray)
        async def files_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .files_manager import files_manager_views
            await interaction.response.send_message(
                embed = files_manager_embed(client),
                view = files_manager_views(client),
                ephemeral = True)

        @discord.ui.button( label = 'Uploader',
                            style = discord.ButtonStyle.gray)
        async def uploader_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .uploader import uploader_views
            await interaction.response.send_message(
                embed = uploader_embed(client),
                view = uploader_views(client),
                ephemeral = True)

        @discord.ui.button( label = 'Flask',
                            disabled = not client.config['Flask']['Allow'],
                            style = discord.ButtonStyle.gray)
        async def flask_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .flask import flask_views
            await interaction.response.send_message(
                embed = flask_embed(client),
                view = flask_views(client),
                ephemeral = True)
        
        @discord.ui.button( label = 'Restart',
                            style = discord.ButtonStyle.red)
        async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                await client.restart(confirmation_interaction)

            await confirmation_request(
                client._('Are you sure about restarting McDis?'), 
                on_confirmation = on_confirmation, 
                interaction = interaction)
  
    return views()