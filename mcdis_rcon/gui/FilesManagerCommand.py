from ..modules import *
from ..classes import *
from ..utils import *

class CommandView           (discord.ui.View):
    def __init__(self, client : McDisClient, process: Process, command: str, action: int = 1):
        super().__init__(timeout = None)
        self.client         = client
        self.process        = process
        self.command        = command
        self.command_path   = os.path.join(self.process.path_commands, self.command)
        self.action         = 1
        self.data : dict    = self._load_data()
        self.actions        = self._get_actions()
        self.options        = self._get_options()

        self.add_item(ActionSelect      (self.client, self.options))
        self.add_item(BackButton        (self.client))
        self.add_item(UpdateButton      (self.client))
        self.add_item(ExecuteButton     (self.client))
        self.add_item(EditButton        (self.client))
        self.add_item(DeleteButton      (self.client))
    
    def _load_data(self):
        return read_yml(self.command_path)
    
    def _get_actions(self):
        return list(self.data.keys())[1:]
    
    def _get_options(self):
        options = []

        for i, action in enumerate(self.actions):
            options.append(discord.SelectOption(
                label = action, 
                value = i + 1))
                
        return options

    def _get_commands(self) -> list[str]:
        return self.data[self.actions[self.action]]

class ActionSelect          (discord.ui.Select):
    def __init__(self, client: McDisClient, options: list):
        super().__init__(placeholder = client._('Select an action'), options = options[:25])
        self.view : CommandView
        
    async def callback(self, interaction: discord.Interaction):
        self.view.action = int(self.values[0])

        await interaction.response.edit_message(
            embed = CommandEmbed(self.view.client, self.view.process, self.view.command, self.view.action),
            view = self.view)

class BackButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_arrow_left, style = discord.ButtonStyle.gray)
        self.view : CommandView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManagerCommands import CommandsEmbed, CommandsView

        await interaction.response.edit_message(
            embed = CommandsEmbed(self.view.client, self.view.process),
            view = CommandsView(self.view.client, self.view.process)
        )

class UpdateButton          (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_update, style = discord.ButtonStyle.gray)
        self.view : CommandView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed = CommandEmbed(self.view.client, self.view.process, self.view.command),
            view = CommandView(self.view.client, self.view.process, self.view.command))

class ExecuteButton         (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Execute', style = discord.ButtonStyle.gray)
        self.view : CommandView

    async def callback(self, interaction: discord.Interaction):
        if self.view.process.is_running() != 'Open':
            await interaction.response.send_message(
                self.view.client._('✖ The server isn\'t open.'), 
                ephemeral = True)
            return

        await interaction.response.send_message(
            self.view.client._('✔ Executing commands...'),
            ephemeral = True)
        
        commands = self.view._get_commands()   
        
        for command in commands:
            if 'await' in command:
                seconds = int(command.replace('await', '').strip())
                await asyncio.sleep(seconds)
                continue

            self.view.process.execute(command.replace('/','').replace('\n',''))

            await asyncio.sleep(1)

class EditButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Edit', style = discord.ButtonStyle.gray)
        self.view : CommandView

    async def callback(self, interaction: discord.Interaction):
        yml_content = read_file(self.view.command_path)

        class edit_command(discord.ui.Modal, title = self.view.client._('Edit the command')):
            name = discord.ui.TextInput(
                label = self.view.client._('Name'),
                style = discord.TextStyle.short,
                default = self.view.command.removesuffix('.yml'))
            
            content = discord.ui.TextInput(
                label = self.view.command,
                style = discord.TextStyle.paragraph,
                default = yml_content)

            async def on_submit(modal, interaction: discord.Interaction):
                new_name = f'{str(modal.name)[:40]}.yml'
                new_path_file = os.path.join(self.view.process.path_commands, new_name)

                write_in_file(self.view.command_path, str(modal.content))

                os.rename(self.view.command_path, new_path_file)

                await interaction.response.edit_message(
                    embed = CommandEmbed(self.view.client, self.view.process, new_name),
                    view = CommandView(self.view.client, self.view.process, new_name)
                )
                    
        await interaction.response.send_modal(edit_command())

class DeleteButton          (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Delete', style = discord.ButtonStyle.red)
        self.view : CommandView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManagerCommands import CommandsEmbed, CommandsView
        async def on_confirmation(confirmation_interaction: discord.Interaction):
            try: 
                os.remove(self.view.command_path)
            except Exception as error: 
                await confirmation_interaction.response.edit_message(
                    content = self.view.client._('Error: {}').format(error), 
                    embed = None, 
                    view = None)
            else:
                await confirmation_interaction.response.edit_message(delete_after = 0)
                await interaction.followup.edit_message(
                    message_id = interaction.message.id,
                    embed = CommandsEmbed(self.view.client, self.view.process),
                    view = CommandsView(self.view.client, self.view.process))

        await confirmation_request(
            self.view.client._('Are you sure about deleting the `{}` command?')
                            .format(self.view.command.removesuffix('.yml')),
            on_confirmation = on_confirmation,
            interaction = interaction)

class CommandEmbed          (discord.Embed):
    def __init__(self, client : McDisClient, process: Process, command: str, action: int = 1):
        title = os.path.join(process.name, command.removesuffix('.yml'))
        super().__init__(title = title, colour = embed_colour)

        self.client         = client
        self.process        = process
        self.command        = command
        self.action         = action

        self.data : dict    = self._load_data()

        self._add_description_field()
        self._add_action_field()
        self._set_footer()

    def _load_data(self):
        file_path = os.path.join(self.process.path_commands, self.command)
        with open(file_path, 'r') as file:
            yaml = ruamel.yaml.YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.preserve_quotes = True
            return yaml.load(file)

    def _add_description_field(self):
        self.add_field(inline = False, 
            name = f'> {self.client._("Description")}:', 
            value = self.data.get('Description')
        )

    def _add_action_field(self):
        action_key = list(self.data.keys())[self.action]
        action_values = list(self.data.values())[self.action]
        value_text = ''.join([f'```{truncate(value, 56)}```' for value in action_values])

        self.add_field(inline = False, name = f'> {action_key}:', value = value_text)

    def _set_footer(self):
        self.set_footer(text = f'{185 * blank_space}')
