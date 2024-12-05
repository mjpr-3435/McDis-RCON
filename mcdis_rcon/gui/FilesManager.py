from ..modules import *
from ..classes import *
from ..utils import *

class FilesManagerView      (discord.ui.View):
    def __init__(self, client: McDisClient, path: str = '.'):
        super().__init__(timeout = None)
        self.max_rqst_size  = 5 * 1024**2
        self.client         = client
        self.path           = path
        self.page           = 1
        
        self.options        = self._get_options()
        self.file_count     = elements_on(path, include_dirs = False, recursive = False)
        self.dir_count      = elements_on(path, include_files = False, recursive = False)
        self.up_to_99       = self.file_count > 99 or self.dir_count > 99
        self.max_file_page  = math.ceil(self.file_count / 99)
        self.max_dir_page   = math.ceil(self.dir_count / 99)

        self.max_page       = max(self.max_file_page, self.max_dir_page)

        if self.options:
            self.add_item(FileSelect(self.client, self.options))
            
        self.add_item(BackButton(self.client))
        self.add_item(UpdateButton(self.client))
        self.add_item(PathButton(self.client))

        if os.path.isdir(self.path):
            self.add_item(TerminalButton(self.client))
            self.add_item(ProcessesButton(self.client))
            # if path != '.': self.add_item(DeleteDirButton(self.client))
        else:
            self.add_item(RequestButton(self.client))
            self.add_item(EditButton(self.client))
            # self.add_item(DeleteFileButton(self.client))

        if self.up_to_99:
            self._add_pagination_buttons()
    
    def         _add_pagination_buttons     (self):
        if self.max_page > 2:
            self.add_item(FirstPageButton(self.client))
        
        self.add_item(PreviousPageButton(self.client))
        self.add_item(NextPageButton(self.client))

        if self.max_page > 2:
            self.add_item(LastPageButton(self.client))
    
    def         _get_options                (self):
        options = []

        if os.path.isdir(self.path):
            dir_files = os.listdir(self.path)
            dir_files.sort()
            dirs = [file for file in dir_files if os.path.isdir(os.path.join(self.path,file))]
            files = [file for file in dir_files if os.path.isfile(os.path.join(self.path,file))]
            
            for dir in dirs:
                options.append(discord.SelectOption(
                    label = f'{emoji_dir} {truncate(dir,90)}', 
                    value = dir))

            for file in files:
                options.append(discord.SelectOption(
                    label = f'{emoji_file} {truncate(file,90)}', 
                    value = file))
                
            #options.insert(0, discord.SelectOption(
            #        label = f'{emoji_pin} Go to', 
            #        value = '__GO_TO__'))
            
        return options[:25]

    async def   _update_embed               (self, interaction : discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
            
        await interaction.followup.edit_message(
                message_id = interaction.message.id, 
                embed = FilesManagerEmbed(self.client, self.path, self.page))
        
    async def   _update_interface           (self, interaction : discord.Interaction, back: bool = False):
        if not interaction.response.is_done():
            await interaction.response.defer()
            
        process_cmd = next(filter(lambda process: self.path == process.path_commands, self.client.processes), None)
        process_bkp = next(filter(lambda process: self.path == process.path_bkps, self.client.processes), None)
        
        if process_cmd:
            from .FilesManagerCommands import CommandsEmbed, CommandsView

            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = CommandsEmbed(self.client, process_cmd),
                view = CommandsView(self.client, process_cmd))
            
        elif process_bkp:
            from .FilesManagerBackups import BackupsEmbed, BackupsView

            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = BackupsEmbed(self.client, process_bkp),
                view = BackupsView(self.client, process_bkp))
        else:
            if back:
                abs_parent_path = os.path.abspath(os.path.dirname(self.path))

                if abs_parent_path.startswith(self.client.cwd):
                    self.path = os.path.relpath(abs_parent_path) 
                else:
                    self.path = self.client.cwd

            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = FilesManagerEmbed(self.client, self.path),
                view = FilesManagerView(self.client, self.path))
    
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

class FileSelect            (discord.ui.Select):
    def __init__(self, client : McDisClient, options: list):
        super().__init__(placeholder = client._('Select a file'), options = options)
        self.view : FilesManagerView
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == '__GO_TO__' and False:
            await self.view._edit_path(interaction)

        else:
            self.view.path = os.path.join(self.view.path, self.values[0]) if self.view.path != '.' else self.values[0]

            await self.view._update_interface(interaction)

class PathButton            (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = emoji_pin, style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        await self.view._edit_path(interaction)

class FirstPageButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '<<', style = discord.ButtonStyle.gray, row = 2)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = 1

        await self.view._update_embed(interaction)

class LastPageButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '>>', style = discord.ButtonStyle.gray, row = 2)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = self.view.max_page

        await self.view._update_embed(interaction)
        
class PreviousPageButton    (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '<', style = discord.ButtonStyle.gray, row = 2)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = self.view.page - 1 if self.view.page > 1 else 1

        await self.view._update_embed(interaction)
        
class NextPageButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = '>', style = discord.ButtonStyle.gray, row = 2)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = self.view.page + 1 if self.view.page < self.view.max_page else self.view.max_page

        await self.view._update_embed(interaction)

class BackButton            (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = emoji_arrow_left, style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        await self.view._update_interface(interaction, back = True)

class UpdateButton          (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = emoji_update, style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        await self.view._update_interface(interaction)

class RequestButton         (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Request', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        if not self.view.client.config['Flask']['Allow']:
            await interaction.response.defer(ephemeral = True, thinking = True)

            if get_path_size(self.view.path, string = False) > self.view.max_rqst_size:
                await interaction.followup.send(
                    self.view.client._('✖ McDis only accepts file requests of up to 5MB.'))
            else:
                await interaction.followup.send(
                    f'> **{mcdis_path(self.view.path)}:**',
                    file = discord.File(self.view.path))
        else:
            if not self.view.client.flask.is_running:
                async def on_confirmation(confirmation_interaction: discord.Interaction):
                    await confirmation_interaction.response.edit_message(delete_after = 0)
                    self.view.client.flask.start()
                    await asyncio.sleep(1)
                    if not self.view.client.flask.is_running: return

                    download_link = self.view.client.flask.download_link(self.view.path, interaction.user.name)
                    view = self.view.remove_item(self).add_item(discord.ui.Button(label = 'Download', url = download_link))
                    embed = interaction.message.embeds[0]
                    embed.description = f'**Download Link:**\n```{download_link}```'

                    await interaction.followup.edit_message(
                        message_id = interaction.message.id,
                        embed = embed,
                        view = view
                    )

                await confirmation_request(
                    self.view.client._('Flask is currently close, do you want to run it?'),
                    on_confirmation = on_confirmation,
                    interaction = interaction
                )
            else:
                download_link = self.view.client.flask.download_link(self.view.path, interaction.user.name)
                view = self.view.remove_item(self).add_item(discord.ui.Button(label = 'Download', url = download_link))
                embed = interaction.message.embeds[0]
                embed.description = f'**Download Link:**\n```{download_link}```'
                await interaction.response.edit_message(embed = embed, view = view)

class EditButton            (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Edit', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        file_content = ''

        if get_path_size(self.view.path, string = False) < self.view.max_rqst_size:
            try:
                file_content = read_file(self.view.path)
                if len(file_content) >= 4000:
                    file_content = ''
            except:
                pass

        class edit_command(discord.ui.Modal, title = self.view.client._('Edit the file')):
            name = discord.ui.TextInput(
                label = self.view.client._('File'),
                style = discord.TextStyle.short,
                default = os.path.basename(self.view.path))
            
            if file_content:
                content = discord.ui.TextInput(
                    label = os.path.basename(self.view.path),
                    style = discord.TextStyle.paragraph,
                    default = file_content)

            async def on_submit(modal, interaction: discord.Interaction):
                new_path = os.path.join(os.path.dirname(self.view.path), os.path.basename(str(modal.name)))

                if file_content:
                    try:
                        write_in_file(self.view.path, str(modal.content))
                    except:
                        self.view.client.error_report(
                            title = 'Writing File in Files Manager',
                            error = traceback.format_exc())
                        return

                try:
                    os.rename(self.view.path, new_path)
                except:
                    self.view.client.error_report(
                        title = 'Renaming File in Files Manager',
                        error = traceback.format_exc())
                    return
                
                await interaction.response.edit_message(
                    embed = FilesManagerEmbed(self.view.client, new_path),
                    view = FilesManagerView(self.view.client, new_path))

        await interaction.response.send_modal(edit_command())

class DeleteFileButton      (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Delete', style = discord.ButtonStyle.red)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        async def on_confirmation(confirmation_interaction: discord.Interaction): 
            new_path = os.path.relpath(os.path.abspath(os.path.dirname(self.view.path)))

            try:
                os.remove(self.view.path)
            except: 
                await self.view.client.error_report(
                    title = 'Delete File in Files Manager',
                    error = traceback.format_exc()
                )

            else:
                await confirmation_interaction.response.edit_message(delete_after = 0)
                self.view.path = new_path

                await self.view._update_interface(interaction)
            
        await confirmation_request(
            self.view.client._('Are you sure you want to delete the file `{}`?').format(mcdis_path(self.view.path)), 
            on_confirmation = on_confirmation,
            interaction = interaction)

class ProcessesButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Processes', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        from .FilesManagerProcesses import ProcessesView, ProcessesEmbed
        await interaction.response.defer()
        
        processes = self._get_processes()

        await interaction.followup.edit_message(
            message_id = interaction.message.id, 
            embed = ProcessesEmbed(self.view.client, self.view.path, processes), 
            view = ProcessesView(self.view.client, self.view.path, processes))

    def _get_processes(self):
        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.view.path) in process.cwd():
                    processes.append(process)
            except:
                pass

        return sorted(processes, key=lambda p: p.cwd())

class TerminalButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Terminal', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

        self.names_convention = client._(
            '✖ The name of directories or files renamed with McDis can only contain letters, '
            'numbers, periods (.), hyphens (-), and underscores (_). Provided name: `{}`')

    async def callback(self, interaction: discord.Interaction):
        class message_modal(discord.ui.Modal, title = self.view.client._('Terminal')):
            command = discord.ui.TextInput(
                label = truncate('> ' + mcdis_path(self.view.path), 45),
                style = discord.TextStyle.paragraph)
            example = discord.ui.TextInput(
                label = self.view.client._('Commands'),
                style = discord.TextStyle.paragraph,
                default = "\n".join(terminal_commands))
        
            async def on_submit(modal, interaction: discord.Interaction):
                await self._cmd_interface(str(modal.command), interaction)

        await interaction.response.send_modal(message_modal())

    async def _cmd_interface(self, command: str, interaction: discord.Interaction):
        args = command.split(' ')
        command_name = args[0].lower()
        handler = getattr(self, f"_cmd_{command_name}", None)

        if handler:
            await handler(args[1:], interaction)
        else:
            await interaction.response.send_message(
                self.view.client._('✖ Invalid command `{}`.').format(command_name),
                ephemeral = True
            )
    
    async def _cmd_mkdir    (self, args: list[str], interaction: discord.Interaction):
        if not args: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide one argument. E.g.: `mkdir <name>`.'), 
                ephemeral = True)
            return
            
        name_provided = ' '.join(args)[:100]

        if not is_valid_path_name(name_provided):
            await interaction.response.send_message(
                self.names_convention.format(name_provided),
                ephemeral = True)
        else:
            dir_path = os.path.join(self.view.path, name_provided)
            os.makedirs(dir_path, exist_ok = True)

            await self.view._update_interface(interaction)
    
    async def _cmd_zip      (self, args: list[str], interaction: discord.Interaction):
        if not args: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide one argument. E.g.: `zip <dir:index>`.'), 
                ephemeral = True)
            return
        
        path_to_zip = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(path_to_zip, str): return

        elif not os.path.isdir(path_to_zip):
            await interaction.response.send_message(
                self.view.client._('✖ The path must be a directory.'),
                ephemeral = True)
            return
        
        await interaction.response.defer()

        zip_path = f'{path_to_zip}.zip'

        response : discord.Message = await interaction.followup.send(
            self.view.client._('`[{}]`: Compressing files...').format(zip_path), 
            ephemeral = True)
        
        counter = [0,0]
        reports = {'error' : None}

        make_zip_error = self.view.client.error_wrapper(
            error_title = 'make_zip() in Terminal',
            reports = reports
            )(make_zip)
        
        task = threading.Thread(
            target = make_zip_error, 
            args = (path_to_zip, zip_path, counter))
        task.start()

        while task.is_alive():
            if counter[1] == 0: 
                await asyncio.sleep(0.1)
            else:
                show = self.view.client._('`[{}]`: `[{}/{}]` files have been compressed...')\
                                .format(zip_path, counter[0], counter[1])
                
                await response.edit(content = show)
                await asyncio.sleep(0.5)

        await self.view._update_interface(interaction)

        if reports['error']:
            msg = self.view.client._('✖ An error occurred while compressing files.')
        else:
            msg = self.view.client._('✔ The files have been successfully compressed.')

        await response.edit(content = msg)
        
        await interaction.user.send(content = msg)

    async def _cmd_unzip    (self, args: list[str], interaction: discord.Interaction):
        if not args: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide one argument. E.g.: `unzip <file:index>`.'), 
                ephemeral = True)
            return
        
        path_to_unzip = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(path_to_unzip, str): return

        elif not os.path.isfile(path_to_unzip) or not path_to_unzip.endswith('.zip'):
            await interaction.response.send_message(
                self.view.client._('✖ The path must be a `.zip` file.'),
                ephemeral = True)
            return
        
        unzip_path = path_to_unzip.removesuffix('.zip')
        
        if os.path.exists(unzip_path):
            await interaction.response.send_message(
                self.view.client._('✖ A folder named `{}` already exists.')
                        .format(os.path.basename(unzip_path)), 
                ephemeral = True)
            return
        
        await interaction.response.defer()
        response : discord.Message = await interaction.followup.send(
            self.view.client._('Unpacking Backup...'), 
            ephemeral = True)
        counter = [0,0]
        reports = {'error': False}
        
        unpack_zip_error = self.view.client.error_wrapper(
            error_title = 'unpack_zip() in Terminal',
            reports = reports
            )(unpack_zip)

        task = threading.Thread(
            target = unpack_zip_error, 
            args = (path_to_unzip, unzip_path, counter))
        task.start()
        
        while task.is_alive():
            if counter[1] == 0: 
                await asyncio.sleep(0.1)
            else:
                show = self.view.client._('`[{}]`: `[{}/{}]` files have been unpacked...')\
                        .format(unzip_path, counter[0], counter[1])
                await response.edit(content = show)
                await asyncio.sleep(0.5)
        
        await self.view._update_interface(interaction)

        if reports['error']:
            msg = self.view.client._('✖ An error occurred while unpacking files.')
        else:
            msg = self.view.client._('✔ The files have been successfully unpacked.')

        await interaction.user.send(msg)
        await response.edit(content = msg)

    async def _cmd_cd       (self, args: list[str], interaction: discord.Interaction):
        if not args: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide one argument. E.g.: `cd <dir:index | file:index>`.'), 
                ephemeral = True)
            return
        
        new_path = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(new_path, str): return

        self.view.path = new_path
        await self.view._update_interface(interaction)

    async def _cmd_del      (self, args: list[str], interaction: discord.Interaction):
        if not args: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide one argument. E.g.: `del <dir:index | file:index>`.'),
                ephemeral = True)
            return
        
        path_to_remove = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(path_to_remove, str): return

        await interaction.response.defer()
        response : discord.Message = await interaction.followup.send(
            self.view.client._('This action might take some time...'),
            ephemeral = True)
        await asyncio.sleep(1)

        if os.path.isdir(path_to_remove): 
            function = shutil.rmtree
        else: 
            function = os.remove

        reports = {'error': False}
        function_error = self.view.client.error_wrapper(
            error_title = 'del() in Terminal',
            reports = reports
        )(function)
        
        await execute_and_wait(function_error, args = (path_to_remove, ))
        
        await self.view._update_interface(interaction)

        if reports['error']:
            msg = self.view.client._('✖ An error occurred while deleting `{}`.').format(mcdis_path(path_to_remove))
        else:
            msg = self.view.client._('✔ `{}` has been deleted.').format(mcdis_path(path_to_remove))

        await response.edit(content = msg)

    async def _cmd_copy     (self, args: list[str], interaction: discord.Interaction):
        if not args[1:]: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide two arguments. E.g.: `copy <dir:index | file:index> <mcdis_path>`.'),
                ephemeral = True)
            return
        
        path_to_copy = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(path_to_copy, str): return

        path_provided = ' '.join(args[1:])
        response = self.view.client.is_valid_mcdis_path(path_provided, check_if_dir = True)
        new_path = os.path.join(un_mcdis_path(path_provided), os.path.basename(path_to_copy))

        if not response is True:
            await interaction.response.send_message(response, ephemeral = True)
            return
        
        elif os.path.exists(new_path):
            if os.path.isdir(new_path): 
                msg = self.view.client._('✖ A folder with that name already exists at path.')
            elif os.path.exists(new_path): 
                msg = self.view.client._('✖ A file with that name already exists at path.')

            await interaction.response.send_message(msg, ephemeral = True)
            return
        
        await interaction.response.defer()
        response :discord.Message = await interaction.followup.send(
            self.view.client._('This action might take some time...'),
            ephemeral = True)
        await asyncio.sleep(1)

        if os.path.isdir(path_to_copy): 
            function = shutil.copytree
        else: 
            function = shutil.copy2

        reports = {'error': False}
        function_error = self.view.client.error_wrapper(
            error_title = 'copy() in Terminal',
            reports = reports
        )(function)

        await execute_and_wait(function_error, args = (path_to_copy, new_path))
        
        await self.view._update_interface(interaction)

        if reports['error']:
            msg = self.view.client._('✖ An error occurred while copying `{}` to `{}`.').format(mcdis_path(path_to_copy), path_provided)
        else:
            msg = self.view.client._('✔ `{}` has been copied to `{}`.').format(mcdis_path(path_to_copy), path_provided)

        await response.edit(
            content = msg)

    async def _cmd_move     (self, args: list[str], interaction: discord.Interaction):
        if not args[1:]: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide two arguments. E.g.: `move <dir:index | file:index> <mcdis_path>`.'),
                ephemeral = True)
            return
        
        path_to_move = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(path_to_move, str): return


        path_provided = ' '.join(args[1:])
        response = self.view.client.is_valid_mcdis_path(path_provided, check_if_dir = True)
        new_path = os.path.join(un_mcdis_path(path_provided), os.path.basename(path_to_move))

        if not response is True:
            await interaction.response.send_message(response, ephemeral = True)
            return
        
        elif os.path.exists(new_path):
            if os.path.isdir(new_path): 
                msg = self.view.client._('✖ A folder with that name already exists at path.')
            elif os.path.exists(new_path): 
                msg = self.view.client._('✖ A file with that name already exists at path.')

            await interaction.response.send_message(msg, ephemeral = True)
            return
        
        await interaction.response.defer()
        response : discord.Message = await interaction.followup.send(
            self.view.client._('This action might take some time...'),
            ephemeral = True)
        await asyncio.sleep(1)

        reports = {'error': False}
        move_error = self.view.client.error_wrapper(
            error_title = 'move() in Terminal',
            reports = reports
        )(shutil.move)

        await execute_and_wait(move_error, args = (path_to_move, new_path))
        
        await self.view._update_interface(interaction)
        if reports['error']:
            msg = self.view.client._('✖ An error occurred while moving `{}` to `{}`.').format(mcdis_path(path_to_move), path_provided)
        else:
            msg = self.view.client._('✔ `{}` has been moved to `{}`.').format(mcdis_path(path_to_move), path_provided)

        await response.edit(content = msg)

    async def _cmd_rename   (self, args: list[str], interaction: discord.Interaction):
        if not args[1:]: 
            await interaction.response.send_message(
                self.view.client._('✖ You must provide two arguments. E.g.: `rename <dir:index | file:index> <new_name>`.'),
                ephemeral = True)
            return
        
        name_provided = ' '.join(args[1:])[:100]

        if not is_valid_path_name(name_provided):
            await interaction.response.send_message(
                self.names_convention.format(name_provided),
                ephemeral = True)
            return
        
        path_to_rename = await self._file_or_dir_selection(args[0], interaction)
        if not isinstance(path_to_rename, str): return
    
        new_path = os.path.join(self.view.path, name_provided)

        try:
            os.rename(path_to_rename, new_path)
        except:
            self.view.client.error_report(
                title = 'rename() in Terminal',
                error = traceback.format_exc())
            return
            
        await self.view._update_interface(interaction)
        
    async def _file_or_dir_selection(self, arg : str, interaction: discord.Interaction) -> Union[str, None]:
        dir_files = os.listdir(self.view.path)
        dir_files.sort()
        dirs  = [file for file in dir_files if os.path.isdir (os.path.join(self.view.path, file))]
        files = [file for file in dir_files if os.path.isfile(os.path.join(self.view.path, file))]

        if not any([arg.lower().startswith(x) for x in ['dir:', 'file:']]):
            await interaction.response.send_message(
                self.view.client._('✖ Invalid argument `{}`. It should be `dir:index` or `file:index`.').format(arg),
                ephemeral = True)
            return
        
        prefix, index = arg.lower().split(':')

        if not index.isdigit():
            await interaction.response.send_message(
                self.view.client._('✖ The index must be an integer.'),
                ephemeral = True)

        elif int(index) < 1 or int(index) > min(len(dirs), 99):
            if prefix == 'dir': prefix = 'directory'
            
            await interaction.response.send_message(
                self.view.client._('✖ No {} exists with that index.').format(self.view.client._(prefix)),
                ephemeral = True)

        elif prefix == 'dir':
            dir_path = dirs[(self.view.page-1)*99 + int(index) - 1]

            return dir_path if self.view.path == '.' else os.path.join(self.view.path, dir_path)

        elif prefix == 'file':
            file_path = files[(self.view.page-1)*99 + int(index) - 1]
                
            return file_path if self.view.path == '.' else os.path.join(self.view.path, file_path)

class DeleteDirButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Delete Dir', style = discord.ButtonStyle.red)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        async def on_confirmation(confirmation_interaction: discord.Interaction): 
            new_path = os.path.relpath(os.path.abspath(os.path.dirname(self.view.path)))
            
            try: 
                shutil.rmtree(self.view.path)
            except: 
                await self.view.client.error_report(
                    title = 'Delete Dir in Files Manager',
                    error = traceback.format_exc()
                )

            else:
                await confirmation_interaction.response.edit_message(delete_after=0)

                self.view.path = new_path
                await self.view._update_interface(interaction)
                
        await confirmation_request(
            self.view.client._('Are you sure you want to delete the dir `{}`?').format(mcdis_path(self.view.path)), 
            on_confirmation = on_confirmation,
            interaction = interaction)

class FilesManagerEmbed     (discord.Embed):
    def __init__(self, client : McDisClient, path: str = '.', page : int = 1):
        super().__init__(color = embed_colour)
        self.max_rqst_size  = 5 * 1024**2
        self.client         = client
        self.path           = path
        self.page           = page

        self.file_count     = elements_on(path, include_dirs = False, recursive = False)
        self.dir_count      = elements_on(path, include_files = False, recursive = False)

        self.title = f"> **{mcdis_path(self.path)}**"
        footer = f"Size: {get_path_size(self.path)}"

        if os.path.isdir(self.path):
            self._add_directory_fields()
            footer += self._generate_footer_for_dirs_and_files()
        else:
            self._add_file_content()
            footer += self._generate_footer_for_file()

        self.set_footer(text = f"{blank_space * 184}\n{footer}")

    def _add_directory_fields                   (self):
        dirs, files = self._get_sorted_dirs_and_files()
        dirs_fields = self._generate_field_content(dirs, emoji_dir)
        files_fields = self._generate_field_content(files, emoji_file)

        for dir_col in dirs_fields:
            self.add_field(inline = True, name = "", value = dir_col)
        
        for file_col in files_fields:
            self.add_field(inline = True, name = "", value = file_col)

    def _add_file_content                       (self):
        try:
            if not get_path_size(self.path, string = False) > self.max_rqst_size:
                content = read_file(self.path)

                self.description = f"```\n{truncate(content, 1990).replace('`', '’')}```"
        except:
            self.description = ""

    def _generate_footer_for_dirs_and_files     (self) -> str:
        dirs_footer = self._generate_footer_pagination(self.dir_count)
        files_footer = self._generate_footer_pagination(self.file_count)
        return f"     |     Dirs: {dirs_footer}     |     Files: {files_footer}"

    def _generate_footer_for_file               (self) -> str:
        date = datetime.fromtimestamp(os.path.getctime(self.path)).strftime("%Y-%m-%d %H:%M:%S")
        local_timezone_offset = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone
        hours_offset = local_timezone_offset // 3600
        minutes_offset = (local_timezone_offset % 3600) // 60
        return f"     |     Date: {date} (UTC {hours_offset:+03}:{minutes_offset:02})"

    def _get_sorted_dirs_and_files              (self) -> tuple[list[str], list[str]]:
        files = sorted(os.listdir(self.path))
        dirs = [f for f in files if os.path.isdir(os.path.join(self.path, f))]
        files = [f for f in files if os.path.isfile(os.path.join(self.path, f))]
        return dirs, files

    def _generate_field_content                 (self, items: list[str], emoji: str) -> list[str]:
        page = self.page - 1
        items_paginated = items[page * 99: (page + 1) * 99]
        columns = [items_paginated[i::3] for i in range(3)]
        return [
            "\n\n".join(
                f"`{(idx)*3 + i + 1:02d} {emoji} {item[:15]}`" for idx, item in enumerate(col, start = 0)
            )
            for i, col in enumerate(columns)
        ]

    def _generate_footer_pagination             (self, total_items: int) -> str:
        if total_items < 99:
            return str(total_items)
        
        page = self.page
        max_page = (total_items // 99) + 1

        if page > max_page:
            return f"- (total: {total_items})"
        
        start = 1 + (page - 1) * 99
        end = min(page * 99, total_items)
        return f"{start} - {end} (total: {total_items})"