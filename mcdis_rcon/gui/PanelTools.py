from ..modules import *
from ..classes import *
from ..utils import *

class ToolsView      (discord.ui.View):
    def __init__(self, client: McDisClient):
        super().__init__(timeout = None)
        self.client = client
        
        self.add_item(BackButton        (self.client))
        self.add_item(ProcessesButton   (self.client))
        self.add_item(UploaderButton    (self.client))
        self.add_item(FlaskButton       (self.client))
        self.add_item(FilesManagerButton(self.client))
        # self.add_item(ReloadButton      (self.client))

class BackButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_arrow_left, style = discord.ButtonStyle.gray)
        self.view : ToolsView

    async def callback(self, interaction: discord.Interaction):
        from .Panel import PanelView

        await interaction.response.edit_message(
            view = PanelView(self.view.client))
        
class ProcessesButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Processes', style = discord.ButtonStyle.gray)
        self.view : ToolsView

    async def callback(self, interaction: discord.Interaction):
        from .PanelProcesses import ProcessesView, ProcessesEmbed
        await interaction.response.defer()
        
        processes = self._get_processes()

        await interaction.followup.send(
            embed = ProcessesEmbed(self.view.client, processes), 
            view = ProcessesView(self.view.client, processes),
            ephemeral = True)

    def _get_processes(self):
        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.view.client.cwd) in process.cwd():
                    processes.append(process)
            except:
                pass

        return sorted(processes, key=lambda p: p.cwd())

class UploaderButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Uploader', style = discord.ButtonStyle.gray)
        self.view : ToolsView

    async def callback(self, interaction: discord.Interaction):
        from .PanelUploader import UploaderView, UploaderEmbed

        await interaction.response.send_message(
            embed = UploaderEmbed(self.view.client),
            view = UploaderView(self.view.client),
            ephemeral = True)

class FlaskButton           (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Flask', style = discord.ButtonStyle.gray)
        self.view : ToolsView

    async def callback(self, interaction: discord.Interaction):
        from .PanelFlask import FlaskView, FlaskEmbed

        await interaction.response.send_message(
            embed = FlaskEmbed(self.view.client),
            view = FlaskView(self.view.client),
            ephemeral = True)
        
class FilesManagerButton           (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Files Manager', style = discord.ButtonStyle.gray)
        self.view : ToolsView

    async def callback(self, interaction: discord.Interaction):
        from .PanelFiles import FilesView, FilesEmbed

        await interaction.response.send_message(
            embed = FilesEmbed(self.view.client),
            view = FilesView(self.view.client),
            ephemeral = True)

class ReloadButton      (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Reload Addons', style = discord.ButtonStyle.gray)
        self.view: ToolsView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        await self.view.client._load_addons(reload = True)
        addons = [addon for addon in self.view.client.addons.keys()]
        extra = '\n • '.join([''] + addons) if addons else self.view.client._('No addons were found.')
        msg = self.view.client._('✔ Addons reloaded: ') + extra
        
        await interaction.followup.send(msg)