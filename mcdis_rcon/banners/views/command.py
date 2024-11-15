from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *

def command_views(client: McDisClient, process: Process, file_name: str) -> discord.ui.View:
    class views(discord.ui.View):
        def __init__(self, process: Process, file_name: str):
            super().__init__(timeout = None)
            self.file_name = file_name
            self.process = process
            self.action = 0
            
            with open(os.path.join(self.process.path_commands, file_name), 'r') as file:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping = 2, sequence = 4, offset = 2)
                yaml.preserve_quotes = True

                data = yaml.load(file)
            
            self.len = len(list(data.keys())) - 1

        @discord.ui.button( label = emoji_arrow_left,
                        style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            from .commands import commands_views
            await interaction.response.edit_message(embed = commands_embed(self.process), view = commands_views(self.process))
        
        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.action = (self.action + 1) % self.len 
            await interaction.response.edit_message(embed = command_embed(self.process, self.file_name, self.action), view = self)

        @discord.ui.button( label = 'Execute',
                            style = discord.ButtonStyle.gray)
        async def execute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.process.state() != 'Open':
                await interaction.response.send_message(client._('✖ The server isn\'t open.'), ephemeral=True)
                return

            await interaction.response.send_message(client._('✔ Executing commands...'), ephemeral=True)
            
            with open(os.path.join(self.process.path_commands, self.file_name), 'r') as file:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping = 2, sequence = 4, offset = 2)
                yaml.preserve_quotes = True

                data = yaml.load(file)
            
            commands = data[list(data.keys())[self.action + 1]]   
            
            for command in commands:
                if 'await' in command:
                    await asyncio.sleep(int(command.replace('await','').strip()))
                    continue
                self.process.execute(command.replace('/','').replace('\n',''))
                await asyncio.sleep(1)
        
        @discord.ui.button( label = 'Edit',
                            style = discord.ButtonStyle.gray)
        async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            with open(os.path.join(self.process.path_commands, self.file_name), 'r') as file:
                lines = file.readlines()

            commands = "".join(lines)

            class edit_command(discord.ui.Modal, title = client._('Edit the command')):
                name = discord.ui.TextInput(label = client._('Name'), style = discord.TextStyle.short, default = self.file_name[:-4])
                content = discord.ui.TextInput(label = self.file_name, style = discord.TextStyle.paragraph, default = commands)

                async def on_submit(modal, interaction: discord.Interaction):
                    path_file = os.path.join(self.process.path_commands, self.file_name)
                    new_path_file = os.path.join(self.process.path_commands, f'{str(modal.name)[:40]}.yml')

                    with open(path_file, 'w') as file:
                        for line in str(modal.content).split('\n'):
                            file.write(line + '\n')

                    os.rename(path_file, new_path_file)
                    self.file_name = f'{str(modal.name)[:40]}.yml'
                    await interaction.response.edit_message(embed = command_embed(self.process, self.file_name, 0), view = command_views(self.process, self.file_name))
                        
            await interaction.response.send_modal(edit_command())

        @discord.ui.button( label = 'Delete',
                            style = discord.ButtonStyle.red)
        async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                from .commands import commands_views
                try: os.remove(os.path.join(self.process.path_commands,self.file_name))
                except Exception as error: 
                    await confirmation_interaction.response.edit_message(content = client._('Error: {}').format(error), embed = None, view = None)
                else:
                    await confirmation_interaction.response.edit_message(delete_after = 0)
                    await interaction.followup.edit_message(message_id = interaction.message.id, 
                                                            embed = commands_embed(self.process), 
                                                            view = commands_views(self.process))

            await confirmation_request(client._('Are you sure about deleting the `{}` command?').format(file_name[:-4]),
                                       on_confirmation = on_confirmation,
                                       interaction = interaction)
    
    return views(process, file_name)