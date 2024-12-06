from ..modules import *
from ..classes import *
from ..utils import *
from ..modules import *
from ..classes import *
from ..utils import *

class BackupsView       (discord.ui.View):
    def __init__(self, client: McDisClient, process: Process):
        super().__init__(timeout = None)
        self.client = client
        self.process = process
        self.backups = self._get_backups()
        self.options = self._get_options()

        self.add_item(BackupSelect      (self.client, self.options))
        self.add_item(BackButton        (self.client))
        self.add_item(UpdateButton      (self.client))
        self.add_item(FilesButton       (self.client))

    def _get_backups(self):
        pattern = os.path.join(
            self.process.path_bkps,
            f'{self.process.name} [1-{self.client.config["Backups"]}].zip',
        )
        
        backups = glob.glob(pattern)
        backups.sort()
        return backups

    def _get_options(self):
        options = [
            discord.SelectOption(
                label = f'{i+1}. {os.path.basename(backup)}',
                value = os.path.basename(backup),
            )
            for i, backup in enumerate(self.backups[:24])
        ]
        options.insert(0, discord.SelectOption(
                label = self.client._('[Make Backup]'),
                emoji = emoji_dir,
                value = '__MAKE_BACKUP__',
            ))
        return options

class BackupSelect      (discord.ui.Select):
    def __init__(self, client: McDisClient, options: list[discord.SelectOption]):
        super().__init__(placeholder = client._('Select a backup'), options = options)
        self.view: BackupsView

    async def callback(self, interaction: discord.Interaction):
        selected_backup = self.values[0]

        if self.view.process.is_running(): 
            await interaction.response.send_message(
                content = self.view.client._('✖ The process must be closed.'),
                ephemeral = True)
            
        elif selected_backup == '__MAKE_BACKUP__':
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                await confirmation_interaction.response.defer()
                await confirmation_interaction.followup.edit_message(
                    message_id = confirmation_interaction.message.id,
                    content = self.view.client._('Compressing files...'),
                    embed = None,
                    view = None)
                
                counter = [0,0]
                reports = {'error': False}
                
                make_bkp = self.view.client.error_wrapper(
                    error_title = f'{self.view.process.name}: make_bkp()',
                    reports = reports
                    )(self.view.process.make_bkp)

                task = threading.Thread(
                    target = make_bkp, 
                    kwargs = {'counter' : counter})
                task.start()
                
                while task.is_alive():
                    if counter[1] == 0: 
                        await asyncio.sleep(0.1)
                    else:
                        show = self.view.client._('`[{}]`: `[{}/{}]` files have been compressed...')\
                            .format(self.view.process.name, counter[0], counter[1])
                        await confirmation_interaction.followup.edit_message(
                            message_id = confirmation_interaction.message.id,
                            content = show)
                        await asyncio.sleep(0.5)
                
                if reports['error']:
                    msg = self.view.client._('✖ An error occurred while compressing files.')
                else:
                    msg = self.view.client._('✔ The files have been successfully compressed.')

                await interaction.user.send(msg)

                await confirmation_interaction.followup.edit_message(
                message_id = confirmation_interaction.message.id,
                content = msg)
                
                await confirmation_interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = BackupsEmbed(self.view.client, self.view.process),
                view = BackupsView(self.view.client, self.view.process))

            await confirmation_request(
                self.view.client._('Are you sure you want to make a backup?'),
                on_confirmation = on_confirmation,
                interaction = interaction
            )
        else:
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                await confirmation_interaction.response.defer()
                await confirmation_interaction.followup.edit_message(
                    message_id = confirmation_interaction.message.id,
                    content = self.view.client._('Unpacking backup...'),
                    embed = None,
                    view = None)
                
                counter = [0,0]
                reports = {'error': False}

                unpack_bkp = self.view.client.error_wrapper(
                    error_title = f'{self.view.process.name}: unpack_bkp()',
                    reports = reports
                    )(self.view.process.unpack_bkp)

                task = threading.Thread(
                    target = unpack_bkp, 
                    args = (selected_backup,), 
                    kwargs = {'counter' : counter})
                task.start()
            
                while task.is_alive():
                    if counter[1] == 0: 
                        await asyncio.sleep(0.1)
                    else:
                        show = self.view.client._('`[{}]`: `[{}/{}]` files have been unpacked...')\
                            .format(self.view.process.name, counter[0], counter[1])
                        await confirmation_interaction.followup.edit_message(
                            message_id = confirmation_interaction.message.id,
                            content = show)
                        await asyncio.sleep(0.5)
                        
                if reports['error']:
                    msg = self.view.client._('✖ An error occurred while unpacking files.')
                else:
                    msg = self.view.client._('✔ The files have been successfully unpacked.')

                await interaction.user.send(msg)

                await confirmation_interaction.followup.edit_message(
                message_id = confirmation_interaction.message.id,
                content = msg)
                
                await confirmation_interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = BackupsEmbed(self.view.client, self.view.process),
                view = BackupsView(self.view.client, self.view.process))

            await confirmation_request(
                self.view.client._('Are you sure you want to load the backup `{}`?')
                        .format(selected_backup),
                on_confirmation = on_confirmation,
                interaction = interaction
            )

class BackButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_arrow_left, style=discord.ButtonStyle.gray)
        self.view: BackupsView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManager import FilesManagerEmbed, FilesManagerView

        await interaction.response.edit_message(
            embed = FilesManagerEmbed(self.view.client, self.view.client.path_backups),
            view = FilesManagerView(self.view.client, self.view.client.path_backups),
        )

class UpdateButton      (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = emoji_update, style = discord.ButtonStyle.gray)
        self.view: BackupsView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed = BackupsEmbed(self.view.client, self.view.process),
            view = BackupsView(self.view.client, self.view.process),
        )

class FilesButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_dir, style=discord.ButtonStyle.gray)
        self.view: BackupsView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManager import FilesManagerEmbed, FilesManagerView

        await interaction.response.edit_message(
            embed = FilesManagerEmbed(self.view.client, self.view.process.path_bkps),
            view = FilesManagerView(self.view.client, self.view.process.path_bkps),
        )

class BackupsEmbed      (discord.Embed):
    def __init__(self, client: McDisClient, process: Process):
        super().__init__(
            title=f'> {mcdis_path(process.path_bkps)}',
            colour=embed_colour,
        )
        self.client = client
        self.process = process
        self.backups = self._get_backups()

        self.description = self._generate_description()
        self._set_footer()

    def _get_backups(self):
        pattern = os.path.join(
            self.process.path_bkps,
            f'{self.process.name} [1-{self.client.config["Backups"]}].zip',
        )
        backups = glob.glob(pattern)
        backups.sort()
        return backups

    def _generate_description(self):
        if not self.backups:
            return f'```{self.client._("No backups were found.")}```'

        description = ''
        for i, backup in enumerate(self.backups):
            description += self._mrkd(backup, i) + '\n'
        return description

    def _set_footer(self):
        footer_text = (
            f'{184 * blank_space}\n'
            f'{self.client._("If you want to load a backup or make one, select it from the dropdown below.")}'
            if self.backups
            else f'{185 * blank_space}'
        )
        self.set_footer(text=footer_text)

    def _mrkd(self, file: str, index: int) -> str:
        date = datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y-%m-%d %H:%M:%S")
        size = get_path_size(file)
        offset_hours, offset_minutes = divmod(
            time.timezone // 60 if time.localtime().tm_isdst == 0 else time.altzone // 60,
            60,
        )
        return (
            f"```asciidoc\n{index + 1}. {os.path.basename(file)}\n"
            f"   ↳ Disk Usage:: {5 * blank_space}{size}\n"
            f"   ↳ Date:: {11 * blank_space}{date} (UTC {offset_hours:+03}:{offset_minutes:02})```"
        )     