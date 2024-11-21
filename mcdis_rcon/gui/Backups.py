from ..modules import *
from ..classes import *
from ..utils import *
from ..modules import *
from ..classes import *
from ..utils import *

class BackupView(discord.ui.View):
    def __init__(self, client: McDisClient, process: Process):
        super().__init__(timeout=None)
        self.client = client
        self.process = process
        self.backups = self._get_backups()

        self.add_item(BackupSelect(self.client, self.process, self.backups))
        self.add_item(BackButton(self.client))
        self.add_item(UpdateButton(self.client))
        self.add_item(FilesButton(self.client))

    def _get_backups(self):
        pattern = os.path.join(
            self.process.path_bkps,
            f'{self.process.name} [1-{self.client.config["Backups"]}].zip',
        )
        
        backups = glob.glob(pattern)
        backups.sort()
        return backups

class BackupSelect(discord.ui.Select):
    def __init__(self, client: McDisClient, process: Process, backups: list[str]):
        options = [
            discord.SelectOption(
                label=f'{i+1}. {os.path.basename(backup)}',
                value=os.path.basename(backup),
            )
            for i, backup in enumerate(backups[:25])
        ]
        super().__init__(placeholder=client._('Select a backup'), options=options)
        self.client = client
        self.process = process
        self.backups = backups
        self.view: BackupView

    async def callback(self, interaction: discord.Interaction):
        selected_backup = self.values[0]

        class BackupModal(discord.ui.Modal, title=selected_backup):
            action = discord.ui.TextInput(
                label=client._('Type "unpack" or "delete" here'),
                style=discord.TextStyle.short,
            )

            async def on_submit(modal, interaction: discord.Interaction):
                action = str(modal.action).lower()
                if action == client._('unpack'):
                    await self.unpack_backup(interaction, selected_backup)
                elif action == client._('delete'):
                    await self.delete_backup(interaction, selected_backup)
                else:
                    await interaction.response.send_message(
                        client._('✖ Action `{}` not recognized.').format(action),
                        ephemeral=True,
                    )

            async def unpack_backup(modal, interaction, backup_name):
                if process.is_running() in ['Initializing', 'Open']:
                    await interaction.response.send_message(
                        client._('✖ The process must be closed.'),
                        ephemeral=True,
                        delete_after=5,
                    )
                    return

                await interaction.response.defer()
                response = await interaction.followup.send(
                    client._('Unpacking Backup...'), ephemeral=True
                )

                counter = [0, 0]
                task = threading.Thread(
                    target=process.unpack_bkp,
                    args=(backup_name,),
                    kwargs={'counter': counter},
                )
                task.start()

                while task.is_alive():
                    if counter[1] == 0 or not isinstance(counter[1], int):
                        await asyncio.sleep(0.1)
                    else:
                        progress = client._(
                            '`[{}]`: `[{}/{}]` files have been unpacked...'
                        ).format(process.name, counter[0], counter[1])
                        await response.edit(content=progress)
                        await asyncio.sleep(0.5)

                if not isinstance(counter[1], int):
                    error_msg = client._(
                        '✖ There was an error while unpacking. Error: {}'
                    ).format(counter[1])
                    await interaction.user.send(error_msg)
                    await response.edit(content=error_msg)
                else:
                    success_msg = client._(
                        '✔ The files have been successfully unpacked.'
                    )
                    await interaction.user.send(success_msg)
                    await response.edit(content=success_msg)

            async def delete_backup(modal, interaction, backup_name):
                try:
                    os.remove(os.path.join(process.path_bkps, backup_name))
                except Exception as e:
                    await interaction.response.send_message(
                        client._('Error: {}').format(e),
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        client._('✔ File deleted.'), ephemeral=True
                    )
                    await interaction.message.edit(
                        embed=BackupEmbed(client, process),
                        view=BackupView(client, process),
                    )

        await interaction.response.send_modal(BackupModal())

class BackButton(discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_arrow_left, style=discord.ButtonStyle.gray)
        self.client = client
        self.view: BackupView

    async def callback(self, interaction: discord.Interaction):
        from ..FilesManager import FileManagerEmbed, files_manager_views

        await interaction.response.edit_message(
            embed=FileManagerEmbed('.mdbackups'),
            view=files_manager_views('.mdbackups'),
        )

class UpdateButton(discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_update, style=discord.ButtonStyle.gray)
        self.client = client
        self.view: BackupView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=BackupEmbed(self.client, self.view.process),
            view=BackupView(self.client, self.view.process),
        )

class FilesButton(discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label=emoji_dir, style=discord.ButtonStyle.gray)
        self.client = client
        self.view: BackupView

    async def callback(self, interaction: discord.Interaction):
        from ..FilesManager import FileManagerEmbed, files_manager_views

        await interaction.response.edit_message(
            embed=FileManagerEmbed(self.view.process.path_bkps),
            view=files_manager_views(self.view.process.path_bkps),
        )

class BackupEmbed(discord.Embed):
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
            entry = mrkd(backup, i) + '\n'
            if len(description + entry) > 1990:
                description += '\n...'
                break
            description += entry
        return description

    def _set_footer(self):
        footer_text = (
            f'{184 * blank_space}\n'
            f'{self.client._("If you want to load or delete a backup, select it from the dropdown below.")}'
            if self.backups
            else f'{185 * blank_space}'
        )
        self.set_footer(text=footer_text)

def mrkd(file: str, index: int) -> str:
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
