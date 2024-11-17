from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def manager(client: McDisClient) -> discord.ui.View:
    if isinstance(client.processes[0], Server):
        process_button_label = f'Server {client.processes[0].name}' 
    else: 
        process_button_label = client.processes[0].name
    
    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.index = 0

        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .panel import panel_views

            await interaction.response.edit_message(
                view = panel_views(client))

        @discord.ui.button( label = process_button_label,
                            style = discord.ButtonStyle.gray)
        async def process_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.index = (self.index + 1)%(len(client.processes))
            
            if isinstance(client.processes[self.index], Server):
                button.label = f'Server {client.processes[self.index].name}'
            else:
                button.label = client.processes[self.index].name
            
            await interaction.response.edit_message(view = self)
            
        @discord.ui.button( label = 'Start',
                            style = discord.ButtonStyle.gray)
        async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if client.processes[self.index].is_running():
                await interaction.response.send_message(
                    client._('✖ `[{}]`: The process was already open.').format(client.processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
                return
            else:
                client.processes[self.index].start()
                await interaction.response.send_message(
                    client._('✔ `[{}]`: Initializing process.').format(client.processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
        
        @discord.ui.button( label = 'Stop',
                            style = discord.ButtonStyle.gray)
        async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not client.processes[self.index].is_running():
                await interaction.response.send_message(
                    client._('✖ `[{}]`: The process was not open.').format(client.processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
            else:
                client.processes[self.index].stop()
                await interaction.response.send_message(
                    client._('✔ `[{}]`: Stopping process.').format(client.processes[self.index].name), 
                    ephemeral = True, 
                    delete_after = 2)
        
        @discord.ui.button( label = 'Kill',
                            style = discord.ButtonStyle.red)
        async def kill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                await confirmation_interaction.response.edit_message(
                    content = client._('✔ `[{}]`: Forcibly stopped process.').format(client.processes[self.index].name),
                    embed = None,
                    view = None,
                    delete_after = 2)
                
                client.processes[self.index].kill()

            await confirmation_request(
                client._('Are you sure about killing the `{}` process?').format(client.processes[self.index].name),
                on_confirmation = on_confirmation,
                interaction = interaction)
  
    return views()