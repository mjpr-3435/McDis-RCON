from ..modules import *
from ..classes import *
from ..utils import *

class ProcessesView(discord.ui.View):
    def __init__(self, client: McDisClient, processes: list[psutil.Process], path: str = '.', page: int = 1):
        super().__init__(timeout=None)
        self.client         = client
        self.path           = path
        self.page           = page
        self.max_processes  = 5
        self.processes      = processes
        self.max_page       = math.ceil(len(self.processes) / self.max_processes)
        self.up_to_max      = len(self.processes) > self.max_processes
        self.options        = self._get_options()
        self._add_buttons()
        
    def         _add_buttons            (self):
        if self.options:
            self.add_item(ProcessSelection(self.client, self.options))

        # self.add_item(BackButton(self.client))
        self.add_item(UpdateButton(self.client))
        self.add_item(PathButton(self.client))

        if self.up_to_max:
            self._add_pagination_buttons()
    
    def         _add_pagination_buttons (self):
        if self.max_page > 2:
            self.add_item(FirstPageButton(self.client))
        
        self.add_item(PreviousPageButton(self.client))
        self.add_item(NextPageButton(self.client))

        if self.max_page > 2:
            self.add_item(LastPageButton(self.client))

    def         _get_options            (self):
        options = []
        min_process    = (self.page-1) * self.max_processes
        max_process    = (self.page) * self.max_processes

        for i in range(min_process, min(max_process, len(self.processes))):
            name = self.processes[i].name()
            option_label = f'{emoji_file} {i + 1}. {truncate(name, 50)}'
            cmd_1 = ' '.join([os.path.basename(cmd) if os.path.exists(cmd) else cmd for cmd in self.processes[i].cmdline()])
            cmd_1 = truncate(cmd_1, 32)

            options.append(discord.SelectOption(label = option_label, value = i))

        return options
    
    def         _update_processes       (self):
        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.path) in process.cwd():
                    processes.append(process)
            except:
                pass

        self.processes = sorted(processes, key=lambda p: p.cwd())

    async def   _update_page            (self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        
        self.options = self._get_options()
        self.clear_items()
        self._add_buttons()
        
        await interaction.followup.edit_message(
            message_id = interaction.message.id,
            embed = ProcessesEmbed(self.client, self.path, self.processes, self.page),
            view = self
        )
        
    async def   _update_interface       (self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        self._update_processes()

        await interaction.followup.edit_message(
            message_id = interaction.message.id,
            embed = ProcessesEmbed(self.client, self.processes, self.path),
            view = ProcessesView(self.client, self.processes, self.path)
        )
    
    async def   _edit_path                  (self, interaction : discord.Interaction):
        class EditPath(discord.ui.Modal, title = self.client._('Go to path')):
            name = discord.ui.TextInput(
                label = self.client._('Path'),
                style = discord.TextStyle.short,
                default = mcdis_path(self.path)
            )

            async def on_submit(modal, interaction: discord.Interaction):
                response = self.client.is_valid_mcdis_path(modal.name.value)

                if response is True:
                    self.path = un_mcdis_path(modal.name.value)
                    await self._update_interface(interaction)
                else:
                    await interaction.response.send_message(response, ephemeral = True)

        await interaction.response.send_modal(EditPath())
        
class ProcessSelection      (discord.ui.Select):
    def __init__(self, client: McDisClient, options: list):
        super().__init__(placeholder = client._('Processes'), options = options)
        self.view: ProcessesView

    async def callback(self, interaction: discord.Interaction):
        selected_process = self.view.processes[int(self.values[0])]

        async def on_confirmation(confirmation_interaction: discord.Interaction):
            await confirmation_interaction.response.edit_message(delete_after = 0)

            selected_process.kill()
            await asyncio.sleep(1)

            await self.view._update_interface(interaction)

        process_path = os.path.relpath(selected_process.cwd(), self.view.client.cwd)
        process_path = truncate(mcdis_path(process_path), 50)
        label = f'{process_path} | {selected_process.name()}'

        await confirmation_request(
            self.view.client._('Are you sure you want to kill the `{}` process?').format(label),
            on_confirmation = on_confirmation,
            interaction = interaction
        )

class FirstPageButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '<<', style = discord.ButtonStyle.gray, row = 2)
        self.view : ProcessesView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = 1

        await self.view._update_page(interaction)

class LastPageButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '>>', style = discord.ButtonStyle.gray, row = 2)
        self.view : ProcessesView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = self.view.max_page

        await self.view._update_page(interaction)
        
class PreviousPageButton    (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '<', style = discord.ButtonStyle.gray, row = 2)
        self.view : ProcessesView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = self.view.page - 1 if self.view.page > 1 else 1

        await self.view._update_page(interaction)
        
class NextPageButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '>', style = discord.ButtonStyle.gray, row = 2)
        self.view : ProcessesView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = self.view.page + 1 if self.view.page < self.view.max_page else self.view.max_page

        await self.view._update_page(interaction)

class PathButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_pin, style = discord.ButtonStyle.gray)
        self.view : ProcessesView

    async def callback(self, interaction: discord.Interaction):
        await self.view._edit_path(interaction)

class BackButton            (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_arrow_left, style=discord.ButtonStyle.gray)
        self.view: ProcessesView

    async def callback(self, interaction: discord.Interaction):
        from .FileManager import FileManagerEmbed, FileManagerView

        await interaction.response.edit_message(
            embed = FileManagerEmbed(self.view.client, self.view.path),
            view = FileManagerView(self.view.client, self.view.path)
        )

class UpdateButton          (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_update, style=discord.ButtonStyle.gray)
        self.view: ProcessesView

    async def callback(self, interaction: discord.Interaction):
        await self.view._update_interface(interaction)
    
class ProcessesEmbed        (discord.Embed):
    def __init__(self, client: McDisClient, processes: list[psutil.Process], path: str = '.', page: int = 1):
        super().__init__(
            title = client._('> Processes in `{}`').format(mcdis_path(path)),
            colour = embed_colour,
        )
        self.client         = client
        self.path           = path
        self.processes      = processes
        self.page           = page
        self.max_processes  = 5

        self._set_descritpion()
        self._set_footer()
    
    def         _set_descritpion    (self):
        mrkd_processes = ''
        for i in range(self.max_processes * (self.page - 1), min(self.max_processes * self.page, len(self.processes))):
            mrkd_processes += f'{self._mrkd(self.processes[i], i)}\n'

        if len(self.processes) != 0:
            self.description = f'```asciidoc\n{mrkd_processes}```'

        else:
            self.description = f'```{self.client._("There are no processes in this folder.")}```'

    def         _set_footer         (self):
        if len(self.processes) != 0:
            self.set_footer(
                text = f'{184 * blank_space}\n' +
                self.client._('If you want to close a process, select it from the dropdown below.'))
            
        else:
            self.set_footer(
                text = 185 * blank_space)

    def         _mrkd               (self, process: psutil.Process, index: int) -> str:
        name = process.name()
        ram = ram_usage(process)

        cwd = os.path.relpath(process.cwd(), os.getcwd())
        cwd = truncate(cwd, 32)

        cmd_1 = ' '.join([os.path.basename(cmd) if os.path.exists(cmd) else cmd for cmd in process.cmdline()])
        cmd_1 = truncate(cmd_1, 32)

        mrkd_string = f'{index + 1}. {name + blank_space * (20 - len(name))}\n'\
                      f'   ↳ Cwd:: {12 * blank_space} {mcdis_path(cwd)}\n'\
                      f'   ↳ Ram Usage:: {6 * blank_space} {ram}\n'\
                      f'   ↳ Command:: {8 * blank_space} {cmd_1}\n'\

        return mrkd_string
