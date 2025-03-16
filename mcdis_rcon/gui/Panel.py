from ..modules import *
from ..classes import *
from ..utils import *
    
class PanelView             (discord.ui.View):
    def __init__(self, client: McDisClient):
        super().__init__(timeout = None)
        self.client = client

        self.add_item(ManagerButton     (self.client))
        self.add_item(FilesButton       (self.client))
        self.add_item(ToolsButton       (self.client))
        self.add_item(GuideButton       (self.client))
        self.add_item(RestartButton     (self.client))

class ManagerButton         (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Processes', style = discord.ButtonStyle.gray)
        self.view : PanelView

    async def callback(self, interaction: discord.Interaction):
        from .PanelManager import McDisManagerView

        await interaction.response.edit_message(
            view = McDisManagerView(self.view.client))

class FilesButton           (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Files', style = discord.ButtonStyle.gray)
        self.view : PanelView

    async def callback(self, interaction: discord.Interaction):
        from .FileManager import FileManagerView, FileManagerEmbed

        await interaction.response.send_message(
            embed = FileManagerEmbed(self.view.client),
            view = FileManagerView(self.view.client),
            ephemeral = True)

class ToolsButton           (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Tools', style = discord.ButtonStyle.gray)
        self.view : PanelView

    async def callback(self, interaction: discord.Interaction):
        from .PanelTools import ToolsView

        await interaction.response.edit_message(
            view = ToolsView(self.view.client))

class GuideButton           (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Guide', style = discord.ButtonStyle.gray)
        self.view : PanelView

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = f'> McDis RCON v{mcdis_vers}',
            colour = embed_colour,
            description = 
            'The guide will be implemented soon, but in the meantime, you can find it on GitHub.'
            '\n\nCoded by KassiuLo.\n[[Kassius\' Discord]](https://discord.gg/xB9N38HBJY)')
        embed.set_image(url = 'https://i.imgur.com/phe4JAf.png')
        embed.set_footer()
        embed.url = 'https://github.com/mjpr-3435/McDis-RCON'

        await interaction.response.send_message(embed = embed, ephemeral = True)
        
class RestartButton         (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Restart', style = discord.ButtonStyle.red)
        self.view : PanelView

    async def callback(self, interaction: discord.Interaction):
        async def on_confirmation(confirmation_interaction: discord.Interaction):
            await self.view.client.restart(confirmation_interaction)

        await confirmation_request(
            self.view.client._('Are you sure you want to restart McDis?'), 
            on_confirmation = on_confirmation, 
            interaction = interaction)

class PanelEmbed            (discord.Embed):
    def __init__(self, client: McDisClient):
        super().__init__(title = client._('Server Panel'), colour=embed_colour)
        self.client = client
        self.warnings = []
        
        self._add_description()
        self._add_resource_fields()
        self._add_servers_fields()
        self._add_networks_fields()
        self._add_mcdis_field()
        self._add_warnings_field()

        self.client.display_panel = False

    def _add_description(self):
        console_cmds = " ".join([f"`{command}`" for command in console_commands])
        panel_cmds = " ".join([f"`{self.client.prefix}{command}`" for command in panel_commands])

        description = (
            self.client._(
                'Here you will find an overview of the server resource usage. '
                'Additionally, McDis RCON recognizes the following commands in the following instances:\n'
            ) +
            f'- {self.client._("Console")} : {console_cmds}\n'
            f'- {self.client._("Panel")} : {panel_cmds}'
        )
        self.description = description

    def _add_resource_fields(self):
        cpu_info = psutil.cpu_freq(), psutil.cpu_percent(interval=1)
        cpu_freq = f'{int(cpu_info[0].current)} MHz'
        cpu_load = f'{cpu_info[1]} %'
        cpu_temp = get_cpu_temp()

        ram_info = psutil.virtual_memory()
        ram_total = f'{ram_info.total / (1024 ** 3):.1f} GB'
        ram_used = f'{ram_info.used / (1024 ** 3):.1f} GB'
        ram_load = f'{ram_info.percent:.1f} %'

        disk_info = psutil.disk_usage("/")
        disk_total = f'{disk_info.total / (1024 ** 3):.1f} GB'
        disk_used = f'{disk_info.used / (1024 ** 3):.1f} GB'
        disk_load = f'{disk_info.percent:.1f} %'

        if disk_info.percent > 90:
            self._add_warning(self.client._('[Disk Usage]: Disk usage is over 90%.'))
        
        if self.client.uploader.is_running: 
            self._add_warning(self.client._('[Uploader]: Uploader is currently running.'))

        if self.client.config['Flask']['Allow'] and self.client.flask.is_running == True: 
            self._add_warning(self.client._('[Flask]: Flask is currently running.'))

        self.add_field(inline = True, name = self.client._('> Server Resources'), value =
            f'```asciidoc\n'
            f'CPU\n'
            f'Freq::           '[:-len(cpu_freq)] + cpu_freq + '\n'
            f'Load::           '[:-len(cpu_load)] + cpu_load + '\n'
            f'Temp::           '[:-len(cpu_temp)] + cpu_temp + '```')
        
        self.add_field(inline = True, name = omit_space, value =
            f'```asciidoc\n'
            f'RAM\n'
            f'Total::          '[:-len(ram_total)] + ram_total + '\n'
            f'Used::           '[:-len(ram_used)] + ram_used + '\n'
            f'Load::           '[:-len(ram_load)] + ram_load + '```')
        
        self.add_field(inline = True, name = omit_space, value =
            f'```asciidoc\n'
            f'Storage\n'
            f'Total::          '[:-len(disk_total)] + disk_total + '\n'
            f'Used::           '[:-len(disk_used)] + disk_used + '\n'
            f'Load::           '[:-len(disk_load)] + disk_load + '```')
        
        if self.client.display_panel:
            print(
                f'CPU\n'
                f'Freq::           '[:-len(cpu_freq)] + cpu_freq + '\n'
                f'Load::           '[:-len(cpu_load)] + cpu_load + '\n'
                f'Temp::           '[:-len(cpu_temp)] + cpu_temp + '\n')
            print(
                f'RAM\n'
                f'Total::          '[:-len(ram_total)] + ram_total + '\n'
                f'Used::           '[:-len(ram_used)] + ram_used + '\n'
                f'Load::           '[:-len(ram_load)] + ram_load + '\n')
            print(
                f'Storage\n'
                f'Total::          '[:-len(disk_total)] + disk_total + '\n'
                f'Used::           '[:-len(disk_used)] + disk_used + '\n'
                f'Load::           '[:-len(disk_load)] + disk_load + '\n')

    def _add_servers_fields(self):
        for i, server in enumerate(self.client.servers):
            state = 'Running' if server.is_running() else 'Closed'
            ram_usage = server.ram_usage()
            disk_usage = server.disk_usage()

            server_id = next(
                filter(lambda thread: thread.name.endswith(server.name), self.client.panel.threads),
                None
            ).id

            self.add_field(inline = True, name = f'> <#{server_id}>', value = 
                f'```asciidoc\n'
                f'Disk Usage::              '[:-len(disk_usage)] + disk_usage + '\n'
                f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '\n'
                f'State::                   '[:-len(state)] + state + '```')
        
            if self.client.display_panel:
                print(
                    f'{server.name}\n'
                    f'Disk Usage::              '[:-len(disk_usage)] + disk_usage + '\n'
                    f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '\n'
                    f'State::                   '[:-len(state)] + state + '\n')
            
            if (i + 1) % 2 == 0:
                self.add_field(inline = False, name = '', value = '')

        if len(self.client.servers) % 2 == 1:
            self.add_field(inline = True, name = '', value = '')
            
        self.add_field(inline = False, name = '', value = '')

    def _add_networks_fields(self):
        for i, network in enumerate(self.client.networks):
            ram_usage = network.ram_usage()
            network_id = next(
                filter(lambda thread: thread.name.endswith(network.name), self.client.panel.threads),
                None
            ).id

            self.add_field(inline = True, name = f'> <#{network_id}>', value = 
                f'```asciidoc\n'
                f'RAM Usage::               '[:-len(ram_usage)] + ram_usage + '```')
        
            if self.client.display_panel:
                print(
                    f'{network.name}\n'
                    f'RAM Usage::               '[:-len(ram_usage)] + ram_usage  + '\n')
        
            if (i + 1) % 2 == 0:
                self.add_field(inline = False, name = '', value = '')

    def _add_mcdis_field(self):
        mcdis_ram_used = f'{psutil.Process().memory_info().rss / (1024 ** 2):.1f} MB'
        self.add_field(inline = True, name = f'> McDis RCON', value =
            f'```asciidoc\n'
            f'RAM Usage::               '[:-len(mcdis_ram_used)] + mcdis_ram_used + '```')
        
        if len(self.client.networks) % 2 == 0:
            self.add_field(inline = True, name = '', value = '')

    def _add_warnings_field(self):
        if self.warnings:
            mrkd_warnings = '\n'.join([f'`{warning}`' for warning in self.warnings])
            self.add_field(inline = False, name = self.client._('> Warnings'), value = mrkd_warnings)

    def _add_warning(self, message):
        warning = f'{emoji_pin} {self.client._(message)}'
        warning += (66 - len(warning)) * blank_space
        self.warnings.append(warning)