from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def flask_views(client: McDisClient) -> discord.ui.View:

    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.path = ''

        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .banner import banner_views

            await interaction.response.edit_message(view=banner_views())

        @discord.ui.button( label = 'Path',
                            style = discord.ButtonStyle.gray)
        async def server_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            class edit_path(discord.ui.Modal, title = client._('Path')):
                name = discord.ui.TextInput(label = client._('Edit'), style = discord.TextStyle.short, default = os.path.basename(self.path))
                
                async def on_submit(modal, interaction: discord.Interaction):
                    self.path = os.path.join(os.path.dirname(self.path), os.path.basename(str(modal.name)))
                     
                    await interaction.response.send_message('ga')

            await interaction.response.send_modal(edit_path())
  
    return views()