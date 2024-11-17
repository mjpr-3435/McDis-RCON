from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def processes_views(client: McDisClient, path: str, processes: list[psutil.Process], page: int = 1) -> discord.ui.View:
    options = []
    up_to_max = len(processes) > max_processes
    max_page = len(processes)//max_processes + 1

    for i in range( max_processes * (page-1), min( max_processes*page, len(processes))):
        name = processes[i].name()
        option_label = f'{emoji_file} {i + 1}. {truncate(name,50)}'
        cmd_1 = ' '.join([os.path.basename(cmd) if os.path.exists(cmd) else cmd for cmd in processes[i].cmdline()])
        cmd_1 = truncate(cmd_1,32)

        options.append(discord.SelectOption(label = option_label, value = i))

    class views(discord.ui.View):
        def __init__(self, processes: list[psutil.Process]):
            super().__init__(timeout = None)
            self.processes = processes
            self.page = page

        if len(options):
            @discord.ui.select( placeholder = client._('Processes'), 
                                options = options[:25])
            async def process_selection(self, interaction: discord.Interaction, selection: discord.ui.Select):
                selected_process = self.processes[int(selection.values[0])]

                async def on_confirmation(confirmation_interaction: discord.Interaction):
                    await confirmation_interaction.response.edit_message(delete_after = 0)

                    selected_process.kill()
                    processes = []
                    for process in psutil.process_iter():
                        try:
                            if os.path.abspath(path) in process.cwd():
                                processes.append(process)
                        except: pass

                    processes = sorted(processes, key = lambda p: p.cwd())
                    
                    await interaction.followup.edit_message(message_id = interaction.message.id, 
                                                            embed = processes_embed(path, processes), 
                                                            view = processes_views(path, processes))
                
                process_path = os.path.relpath(selected_process.cwd(), client.cwd)
                process_path = truncate(mcdis_path(process_path), 50)
                label = process_path + ' | ' + selected_process.name() 
                await confirmation_request(client._('Are you sure about killing the `{}` process?').format(label),
                                           on_confirmation = on_confirmation,
                                           interaction = interaction) 

        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .files_manager import files_manager_views
            await interaction.response.edit_message(embed = files_manager_embed(path), view=files_manager_views(path))

        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            processes = []
            for process in psutil.process_iter():
                try:
                    if os.path.abspath(path) in process.cwd():
                        processes.append(process)
                except: pass

            processes = sorted(processes, key=lambda p: p.cwd())

            await interaction.followup.edit_message(message_id = interaction.message.id,  embed = processes_embed(path, processes), view=processes_views(path, processes))
        
        if up_to_max:
            @discord.ui.button( label = '<',
                                style = discord.ButtonStyle.gray)
            async def previous_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.page = self.page - 1 if self.page > 1 else 1
                await interaction.response.edit_message(embed = processes_embed(path, processes, self.page), view=processes_views(path, processes, self.page))

            @discord.ui.button( label = '>',
                                style = discord.ButtonStyle.gray)
            async def next_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.page = self.page + 1 if self.page < max_page else max_page
                await interaction.response.edit_message(embed = processes_embed(path, processes, self.page), view=processes_views(path, processes, self.page))

            if max_page > 3:
                @discord.ui.button( label = '>>',
                                    style = discord.ButtonStyle.gray)
                async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.page = max_page
                    await interaction.response.edit_message(embed = processes_embed(path, processes, self.page), view=processes_views(path, processes, self.page))

    return views(processes)