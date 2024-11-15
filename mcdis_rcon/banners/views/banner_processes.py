from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def banner_processes(client: McDisClient) -> discord.ui.View:

    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.index = 0

        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .banner import banner_views

            await interaction.response.edit_message(view=banner_views())

        @discord.ui.button( label = f'Server {processes[0].name}' if isinstance(processes[0], Server) else processes[0].name,
                            style = discord.ButtonStyle.gray)
        async def server_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.index = (self.index + 1)%(len(processes))
            if isinstance(processes[self.index], Server):
                button.label = f'Server {processes[self.index].name}'
            else:
                button.label = processes[self.index].name

            await interaction.response.edit_message(view = self)
            
        @discord.ui.button( label = 'Start',
                            style = discord.ButtonStyle.gray)
        async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if processes[self.index].state() in ['Open','Initializing']:
                await interaction.response.send_message(
                    client._('✖ `[{}]`: The process was already open.').format(processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
                return
            else:
                processes[self.index].start()
                await interaction.response.send_message(
                    client._('✔ `[{}]`: Initializing process.').format(processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
        
        @discord.ui.button( label = 'Stop',
                            style = discord.ButtonStyle.gray)
        async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if processes[self.index].state() == 'Closed':
                await interaction.response.send_message(
                    client._('✖ `[{}]`: The process was not open.').format(processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
            else:
                processes[self.index].stop()
                await interaction.response.send_message(
                    client._('✔ `[{}]`: Stopping process.').format(processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
        
        @discord.ui.button( label = 'Kill',
                            style = discord.ButtonStyle.red)
        async def kill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                await confirmation_interaction.response.edit_message(
                    content = client._('✔ `[{}]`: Forcibly stopped process.').format(processes[self.index].name),
                    embed = None,
                    view = None,
                    delete_after = 2)
                
                processes[self.index].kill()
            await confirmation_request( client._('Are you sure about killing the `{}` process?').format(processes[self.index].name),
                                        on_confirmation = on_confirmation,
                                        interaction = interaction)
  
    return views()