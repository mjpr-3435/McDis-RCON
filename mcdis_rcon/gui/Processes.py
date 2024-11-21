from ..modules import *
from ..classes import *
from ..utils import *

class ProcessesView(discord.ui.View):
    def __init__(self, client: McDisClient, path: str, processes: list[psutil.Process], page: int = 1):
        super().__init__(timeout=None)
        self.client = client
        self.path = path
        self.processes = processes
        self.page = page
        self.max_processes = 5
        self.max_page = len(processes) // self.max_processes + 1
        self.options = self._generate_options()

        self.add_item(BackButton(self.client))
        self.add_item(UpdateButton(self.client))
        self.add_item(PageNavigationButtons(self.client, self.processes, self.page, self.max_page))

        if self.options:
            self.add_item(ProcessSelection(self.client, self.processes, self.options))

    def _generate_options(self):
        options = []
        up_to_max = len(self.processes) > self.max_processes

        for i in range(self.max_processes * (self.page - 1), min(self.max_processes * self.page, len(self.processes))):
            name = self.processes[i].name()
            option_label = f'{emoji_file} {i + 1}. {truncate(name, 50)}'
            cmd_1 = ' '.join([os.path.basename(cmd) if os.path.exists(cmd) else cmd for cmd in self.processes[i].cmdline()])
            cmd_1 = truncate(cmd_1, 32)

            options.append(discord.SelectOption(label=option_label, value=i))

        return options


class ProcessSelection(discord.ui.Select):
    def __init__(self, client: McDisClient, processes: list[psutil.Process], options: list):
        super().__init__(placeholder=client._('Processes'), options=options[:25])
        self.view: ProcessesView
        self.processes = processes

    async def callback(self, interaction: discord.Interaction):
        selected_process = self.processes[int(self.values[0])]

        async def on_confirmation(confirmation_interaction: discord.Interaction):
            await confirmation_interaction.response.edit_message(delete_after=0)

            selected_process.kill()
            processes = self._get_updated_processes()

            await interaction.followup.edit_message(
                message_id=interaction.message.id,
                embed=ProcessesEmbed(self.view.client, self.view.path, processes),
                view=ProcessesView(self.view.client, self.view.path, processes)
            )

        process_path = os.path.relpath(selected_process.cwd(), self.view.client.cwd)
        process_path = truncate(mcdis_path(process_path), 50)
        label = process_path + ' | ' + selected_process.name()
        await confirmation_request(
            self.view.client._('Are you sure about killing the `{}` process?').format(label),
            on_confirmation=on_confirmation,
            interaction=interaction
        )

    def _get_updated_processes(self):
        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.view.path) in process.cwd():
                    processes.append(process)
            except:
                pass
        return sorted(processes, key=lambda p: p.cwd())


class PageNavigationButtons(discord.ui.View):
    def __init__(self, client: McDisClient, processes: list[psutil.Process], page: int, max_page: int):
        super().__init__(timeout=None)
        self.client = client
        self.processes = processes
        self.page = page
        self.max_page = max_page

    @discord.ui.button(label=emoji_arrow_left, style=discord.ButtonStyle.gray)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=ProcessesEmbed(self.client, self.view.path, self.processes, self.page),
            view=ProcessesView(self.client, self.view.path, self.processes, self.page - 1)
        )

    @discord.ui.button(label=emoji_update, style=discord.ButtonStyle.gray)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        processes = self._get_updated_processes()

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=ProcessesEmbed(self.client, self.view.path, processes),
            view=ProcessesView(self.client, self.view.path, processes, self.page)
        )

    def _get_updated_processes(self):
        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.view.path) in process.cwd():
                    processes.append(process)
            except:
                pass
        return sorted(processes, key=lambda p: p.cwd())

    @discord.ui.button(label='<', style=discord.ButtonStyle.gray)
    async def previous_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = self.page - 1 if self.page > 1 else 1
        await interaction.response.edit_message(embed=ProcessesEmbed(self.client, self.view.path, self.processes, self.page), view=ProcessesView(self.client, self.view.path, self.processes, self.page))

    @discord.ui.button(label='>', style=discord.ButtonStyle.gray)
    async def next_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = self.page + 1 if self.page < self.max_page else self.max_page
        await interaction.response.edit_message(embed=ProcessesEmbed(self.client, self.view.path, self.processes, self.page), view=ProcessesView(self.client, self.view.path, self.processes, self.page))

    @discord.ui.button(label='>>', style=discord.ButtonStyle.gray)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = self.max_page
        await interaction.response.edit_message(embed=ProcessesEmbed(self.client, self.view.path, self.processes, self.page), view=ProcessesView(self.client, self.view.path, self.processes, self.page))


class BackButton(discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_arrow_left, style=discord.ButtonStyle.gray)
        self.view: ProcessesView

    async def callback(self, interaction: discord.Interaction):
        from .Commands import CommandsEmbed, CommandsView
        await interaction.response.edit_message(
            embed=CommandsEmbed(self.view.client, self.view.process),
            view=CommandsView(self.view.client, self.view.process)
        )


class UpdateButton(discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_update, style=discord.ButtonStyle.gray)
        self.view: ProcessesView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        processes = self._get_updated_processes()
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=ProcessesEmbed(self.view.client, self.view.path, processes),
            view=ProcessesView(self.view.client, self.view.path, processes)
        )

    def _get_updated_processes(self):
        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.view.path) in process.cwd():
                    processes.append(process)
            except:
                pass
        return sorted(processes, key=lambda p: p.cwd())
    
class ProcessesEmbed(discord.Embed):
    def __init__(self, client: McDisClient, path: str, processes: list[psutil.Process], page: int = 1):
        super().__init__(
            title = client._('> Processes in `{}`').format(mcdis_path(path)),
            colour = embed_colour,
        )
        self.client = client
        self.path = path
        self.processes = processes
        self.page = page

        mrkd_processes = ''
        for i in range(max_processes * (page - 1), min(max_processes * page, len(processes))):
            mrkd_processes += self.mrkd(processes[i], i) + '\n'

        if len(mrkd_processes) != 0:
            self.description = f'```asciidoc\n{mrkd_processes}```'
            self.set_footer(text=f'{184 * blank_space}\n' + client._('If you want to close a process, select it from the dropdown below.'))
        else:
            self.description = f'```{client._("There are no processes in this folder.")}```'
            self.set_footer(text=f'{185 * blank_space}')

    def mrkd(self, process: psutil.Process, index: int) -> str:
        name = process.name()
        ram = ram_usage(process)

        cwd = os.path.relpath(process.cwd(), os.getcwd())
        cwd = truncate(cwd, 32)

        cmd_1 = ' '.join([os.path.basename(cmd) if os.path.exists(cmd) else cmd for cmd in process.cmdline()])
        cmd_1 = truncate(cmd_1, 32)

        mrkd_string = f"{index + 1}. {name + blank_space * (20 - len(name))}\n   ↳ Cwd:: {12 * blank_space} {mcdis_path(cwd)}\n   ↳ Ram Usage:: {6 * blank_space} {ram}\n   ↳ Command:: {8 * blank_space} {cmd_1}\n"

        return mrkd_string
