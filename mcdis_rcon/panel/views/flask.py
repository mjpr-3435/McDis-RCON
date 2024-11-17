from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def flask_views(client: McDisClient) -> discord.ui.View:

    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)

        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            pass

        @discord.ui.button( label = 'Stop',
                            style = discord.ButtonStyle.gray)
        async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            pass
  
    return views()