from ..modules import *
from ..classes import *
from ..utils import *
    
class McDisManagerView      (discord.ui.View):
    def __init__(self, client: McDisClient):
        super().__init__(timeout = None)
        self.client = client
        self.index  = 0
        
        self.add_item(BackButton        (self.client))
        self.add_item(ProcessButton     (self.client))
        self.add_item(StartButton       (self.client))
        self.add_item(StopButton        (self.client))
        self.add_item(KillButton        (self.client))

class BackButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_arrow_left, style = discord.ButtonStyle.gray)
        self.view : McDisManagerView

    async def callback(self, interaction: discord.Interaction):
        from .Panel import PanelView

        await interaction.response.edit_message(
            view = PanelView(self.view.client))

class ProcessButton         (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label = self._get_label(client.processes[0])
        super().__init__(label = label, style = discord.ButtonStyle.gray)
        self.view : McDisManagerView

    async def callback(self, interaction: discord.Interaction):
        self.view.index = (self.view.index + 1) % len(self.view.client.processes)
        self.label = self._get_label(self.view.client.processes[self.view.index])

        await interaction.response.edit_message(view = self.view)

    def _get_label(self, process: Process):
        return f"Server {process.name}" if isinstance(process, Server) else process.name
   
class StartButton           (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Start', style = discord.ButtonStyle.gray)
        self.view : McDisManagerView

    async def callback(self, interaction: discord.Interaction):
        if self.view.client.processes[self.view.index].is_running():
            await interaction.response.send_message(
                self.view.client._('✖ `[{}]`: The process was already open.')
                                .format(self.view.client.processes[self.view.index].name), 
                ephemeral = True)
        
        else:
            self.view.client.processes[self.view.index].start()
            await interaction.response.send_message(
                self.view.client._('✔ `[{}]`: Initializing process.')
                                .format(self.view.client.processes[self.view.index].name), 
                ephemeral = True)

class StopButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Stop', style = discord.ButtonStyle.gray)
        self.view : McDisManagerView

    async def callback(self, interaction: discord.Interaction):
        if not self.view.client.processes[self.view.index].is_running():
            await interaction.response.send_message(
                self.view.client._('✖ `[{}]`: The process was not open.')
                                .format(self.view.client.processes[self.view.index].name), 
                ephemeral = True)
            
        else:
            self.view.client.processes[self.view.index].stop()
            await interaction.response.send_message(
                self.view.client._('✔ `[{}]`: Stopping process.')
                                .format(self.view.client.processes[self.view.index].name), 
                ephemeral = True)

class KillButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Kill', style = discord.ButtonStyle.red)
        self.view : McDisManagerView

    async def callback(self, interaction: discord.Interaction):
        async def on_confirmation(confirmation_interaction: discord.Interaction):
            await confirmation_interaction.response.edit_message(
                content = self.view.client._('✔ `[{}]`: Forcibly stopped process.')
                                        .format(self.view.client.processes[self.view.index].name),
                embed = None,
                view = None)
            
            self.view.client.processes[self.view.index].kill()

        await confirmation_request(
            self.view.client._('Are you sure about killing the `{}` process?')
                            .format(self.view.client.processes[self.view.index].name),
            on_confirmation = on_confirmation,
            interaction = interaction)