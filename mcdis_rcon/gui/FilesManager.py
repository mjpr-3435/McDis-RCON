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
        self.max_page       = max(self.file_count // 99 + 1, self.dir_count // 99 + 1)

        self.add_item(BackButton(self.client))
        self.add_item(UpdateButton(self.client))

        if self.options:
            self.add_item(FileSelect(self.client, self.options))

        if os.path.isdir(self.path):
            self.add_item(ProcessesButton(self.client))
            self.add_item(TerminalButton(self.client))
            if path != '.':
                self.add_item(DeleteDirButton(self.client))
        else:
            self.add_item(RequestButton(self.client))
            self.add_item(EditButton(self.client))
            self.add_item(DeleteFileButton(self.client))

        if self.up_to_99:
            self._add_pagination_buttons()
    
    def _add_pagination_buttons     (self):
        if self.max_page > 3:
            self.add_item(FirstPageButton(self.client))
        
        self.add_item(PreviousPageButton(self.client))
        self.add_item(NextPageButton(self.client))

        if self.max_page > 3:
            self.add_item(LastPageButton(self.client))
    
    def _get_options                (self):
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
                
        return options

    async def _update_embed         (self, interaction : discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
            
        await interaction.followup.edit_message(
                message_id = interaction.message.id, 
                embed = FilesManagerEmbed(self.client, self.path, self.page))
        
    async def _update_interface     (self, interaction : discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
            
        await interaction.followup.edit_message(
                message_id = interaction.message.id, 
                embed = FilesManagerEmbed(self.client, self.path), 
                view = FilesManagerView(self.client, self.path))
            
        return
    
        process_cmd = next(filter(lambda process: self.path == process.path_commands, self.client.processes), None)
        process_bkp = next(filter(lambda process: self.path == process.path_bkps, self.client.processes), None)

        if process_cmd:
            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = commands_embed(self.client, process_cmd),
                view = commands_views(self.client, process_cmd))
        elif process_bkp:
            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = backups_embed(self.client, process_bkp),
                view = backups_views(self.client, process_bkp))
        else:
            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = FilesManagerEmbed(self.client, new_path),
                view = FilesManagerView(self.client, new_path))
    
class FileSelect            (discord.ui.Select):
    def __init__(self, client : McDisClient, options: list):
        super().__init__(placeholder = client._('Select a file'), options = options[:25])
        self.view : FilesManagerView
    
    async def callback(self, interaction: discord.Interaction):
        self.view.path = os.path.join(self.view.path, self.values[0]) if self.view.path != '.' else self.values[0]
        
        await self.view._update_interface(interaction)

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
        parent_path = os.path.abspath(os.path.dirname(self.view.path))

        if parent_path.startswith(self.view.client.cwd):
            self.view.path = os.path.relpath(parent_path, self.view.client.cwd) 
        else:
            self.view.path = self.view.client.cwd

        await self.view._update_interface(interaction)

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
                await interaction.followup.send(self.view.client._('✖ McDis only accepts file requests of up to 5MB.'))
            else:
                await interaction.followup.send(f'> **{mcdis_path(self.view.path)}:**', file = discord.File(self.view.path))
        else:
            download_link = self.view.client.flask.download_link(self.view.path, interaction.user.name)
            view = self.view.remove_item(self).add_item(discord.ui.Button(label = 'Download', url = download_link))
            embed = interaction.message.embeds[0]
            embed.description = f'**Download Link:**\n```{download_link}```'
            await interaction.response.edit_message(embed=embed, view = view)

class EditButton            (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Edit', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        file_content = None
        
        if not get_path_size(self.view.path, string = False) > self.view.max_rqst_size:
            try:
                file_content =  read_file(self.view.path)

                if len(file_content) >= 4000: 
                    file_content = None
            except:
                file_content = None
            
        class edit_command(discord.ui.Modal, title = self.view.client._('Edit the file')):
            name = discord.ui.TextInput(label = self.view.client._('File'), style = discord.TextStyle.short, default = os.path.basename(self.view.path))
            if file_content: content = discord.ui.TextInput(label = os.path.basename(self.view.path), style = discord.TextStyle.paragraph, default = file_content)

            async def on_submit(modal, interaction: discord.Interaction):
                new_path = os.path.join(os.path.dirname(self.view.path), os.path.basename(str(modal.name)))

                try:
                    if file_content:
                        write_in_file(self.view.path, str(modal.content))

                    os.rename(self.view.path, new_path)
                except Exception as error:
                    await interaction.response.send_message(content = self.view.client._('Error: {}').format(error), ephemeral=True)
                    return
                
                await interaction.response.edit_message(embed = FilesManagerEmbed(new_path), view = FilesManagerView(new_path))

        await interaction.response.send_modal(edit_command())

class DeleteFileButton      (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Delete', style = discord.ButtonStyle.red)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        async def on_confirmation(confirmation_interaction: discord.Interaction): 
            new_path = os.path.relpath(os.path.abspath(os.path.dirname(self.view.path)))

            try: os.remove(self.view.path)
            except Exception as error: 
                await confirmation_interaction.response.edit_message(content = self.view.client._('Error: {}').format(error), embed = None, view = None)
            else:
                await confirmation_interaction.response.edit_message(delete_after = 0)
                await interaction.followup.edit_message(message_id=interaction.message.id, 
                                                        embed = FilesManagerEmbed(new_path), 
                                                        view = FilesManagerView(new_path))
            
        await confirmation_request(self.view.client._('Are you sure about deleting the file `{}`?').format(mcdis_path(self.view.path)), 
                                    on_confirmation = on_confirmation,
                                    interaction = interaction)

class ProcessesButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Processes', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        from .views.processes import processes_views
        await interaction.response.defer()

        processes = []
        for process in psutil.process_iter():
            try:
                if os.path.abspath(self.view.path) in process.cwd():
                    processes.append(process)
            except: pass
            
        processes = sorted(processes, key=lambda p: p.cwd())
        
        await interaction.followup.edit_message(message_id = interaction.message.id, 
                                                embed = processes_embed(self.view.path, processes), 
                                                view = processes_views(self.view.path, processes))

class TerminalButton        (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Terminal', style = discord.ButtonStyle.gray)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        class message_modal(discord.ui.Modal, title = self.view.client._('Terminal')):
            command = discord.ui.TextInput(label = truncate('> ' + mcdis_path(self.view.path), 45), style = discord.TextStyle.paragraph)
            example = discord.ui.TextInput(label = self.view.client._('Commands'), style = discord.TextStyle.paragraph, default = "\n".join(terminal_commands))
        
            async def on_submit(modal, interaction: discord.Interaction):
                await self.cmd_interface(str(modal.command), interaction, self.view.path, self)
        await interaction.response.send_modal(message_modal())

    async def cmd_interface(client: McDisClient, command: str, interaction: discord.Interaction, path: str, view: discord.ui.View):
        args = command.split(' ')
        names_convention = client._('✖ The names of directories created with McDis can only contain letters, '
                            'numbers, periods (.), hyphens (-), and underscores (_). Provided name: `{}`')
        
        dir_files = os.listdir(path)
        dir_files.sort()
        dirs = [file for file in dir_files if os.path.isdir(os.path.join(path,file))]
        files = [file for file in dir_files if os.path.isfile(os.path.join(path,file))]

        
        async def file_or_dir_selection(arg : str) -> Union[str, None]:
            if arg.lower().startswith('dir:'):
                try: index = int(arg[4:])
                except:
                    await interaction.response.send_message( client._('✖ The index must be an integer.'), ephemeral=True)
                    return
                
                if index < 1 or index > min(len(dirs),99):
                    await interaction.response.send_message( client._('✖ No directory exists with that index.'), ephemeral=True)
                    return

                return dirs[(view.page-1)*99 + index- 1] if path == '.' else os.path.join(path, dirs[(view.page-1)*99 + index- 1])

            elif arg.lower().startswith('file:'):
                try:
                    index = int(arg[5:])
                except: 
                    await interaction.response.send_message( client._('✖ The index must be an integer.'), ephemeral=True)
                    return
                
                if index < 1 or index > min(len(files),99):
                    await interaction.response.send_message( client._('✖ No file exists with that index.'), ephemeral=True)
                    return

                return files[(view.page-1)*99 + index- 1] if path == '.' else os.path.join(path,files[(view.page-1)*99 + index- 1])
            
            else:
                await interaction.response.send_message(
                    client._('✖ Invalid argument `{}`. It should be `dir:index` or `file:index`.').format(arg),
                    ephemeral=True)
                return

        if args[0].lower() == 'mkdir':
            if len(args) == 1: 
                await interaction.response.send_message(
                    client._('✖ You must provide one argument. E.g.: `mkdir <name>`.'), 
                    ephemeral = True)
                
            elif not is_valid_path_name(args[1]):
                await interaction.response.send_message(names_convention.format(args[1]), ephemeral=True)
            else:
                os.makedirs(os.path.join(path, args[1]), exist_ok = True)
                await update_files_interface(client, interaction, path, path)
        
        elif args[0].lower() == 'zip':
            if len(args) == 1: 
                await interaction.response.send_message(
                    client._('✖ You must provide one argument. E.g.: `zip <dir:index>`.'), 
                    ephemeral=True)
            else:
                path_to_zip = await file_or_dir_selection(args[1])
                if not path_to_zip: return

                elif not os.path.isdir(path_to_zip):
                    await interaction.response.send_message(client._('✖ The path must be a directory.'), ephemeral=True)
                    return
                elif get_path_size(path_to_zip, string = False) > psutil.disk_usage("/").free:
                    await interaction.response.send_message(client._('✖ There\'s not enough space on the disk to create this `.zip`.'), ephemeral=True)
                    return
                
                await interaction.response.defer(ephemeral = True, thinking = True)

                response = await interaction.followup.send(client._('`[{}]`: Compressing files...').format(path_to_zip + '.zip'))
                
                counter = [0,0]
                task = threading.Thread(target = make_zip, args = (path_to_zip, path_to_zip + '.zip', counter))
                task.start()

                while task.is_alive():
                    if counter[1] == 0: 
                        await asyncio.sleep(0.1)
                    else:
                        show = client._('`[{}]`: `[{}/{}]` files have been compressed...').format(path_to_zip + '.zip', counter[0], counter[1])
                        await response.edit(content = show)
                        await asyncio.sleep(0.5)

                await update_files_interface(client, interaction, path, path)
                await response.edit(content = client._('✔ The files have been successfully compressed.'))
                await interaction.user.send(content = client._('✔ The files have been successfully compressed.'))

        elif args[0].lower() == 'unzip':
            if len(args) == 1: 
                await interaction.response.send_message(
                    client._('✖ You must provide one argument. E.g.: `unzip <file:index>`.'), 
                    ephemeral=True)
            else:
                path_to_unzip = await file_or_dir_selection(args[1])
                if not path_to_unzip: return

                elif not os.path.isfile(path_to_unzip) or not path_to_unzip.endswith('.zip'):
                    await interaction.response.send_message(client._('✖ The path must be a `.zip` file.'), ephemeral=True)
                    return
                
                elif os.path.exists(path_to_unzip.removesuffix('.zip')):
                    await interaction.response.send_message(client._('✖ A folder named `{}` already exists.').format(os.path.basename(path_to_unzip.removesuffix('.zip'))), ephemeral=True)
                    return
                
                await interaction.response.defer()
                response : discord.Message = await interaction.followup.send(client._('Unpacking Backup...'), ephemeral = True)
                counter = [0,0]
                
                task = threading.Thread(target = unpack_zip, args = (path_to_unzip, path_to_unzip.removesuffix('.zip'), counter))
                task.start()
                
                while task.is_alive():
                    if counter[1] == 0 or not isinstance(counter[1], int): 
                        await asyncio.sleep(0.1)
                    else:
                        show = client._('`[{}]`: `[{}/{}]` files have been unpacked...').format(path_to_unzip.removesuffix('.zip'), counter[0], counter[1])
                        await response.edit(content = show)
                        await asyncio.sleep(0.5)
                
                if not isinstance(counter[1], int):
                    msg = client._('✖ There was an error while unpacking. Error: {}').format(counter[1])
                    await interaction.user.send(msg)
                    await response.edit(content = msg)
                else:
                    await update_files_interface(client, interaction, path, path)
                    msg = client._('✔ The files have been successfully unpacked.')
                    await interaction.user.send(msg)
                    await response.edit(content = msg)


        elif args[0].lower() == 'cd':
            if len(args) == 1: 
                await interaction.response.send_message(
                    client._('✖ You must provide one argument. E.g.: `cd <dir:index | file:index>`.'), 
                    ephemeral=True)
            else:
                new_path = await file_or_dir_selection(args[1])

                if new_path: await update_files_interface(client, interaction, new_path, path)

        elif args[0].lower() == 'del':
            if len(args) == 1: 
                await interaction.response.send_message(
                    client._('✖ You must provide one argument. E.g.: `del <dir:index | file:index>`.'),
                    ephemeral = True)
            else:
                path_to_remove = await file_or_dir_selection(args[1])

                if path_to_remove:
                    await interaction.response.defer()
                    response : discord.Message = await interaction.followup.send(client._('This action might take some time...'), ephemeral = True)
                    await asyncio.sleep(1)
                    try:
                        if os.path.isdir(path_to_remove): 
                            await execute_and_wait(shutil.rmtree, args = (path_to_remove, ))
                        elif os.path.isfile(path_to_remove): 
                            await execute_and_wait(os.remove, args = (path_to_remove, ))
                    except Exception as error:
                        await response.edit(content = client._('Error: {}').format(error))
                    else:
                        await interaction.followup.edit_message(message_id = interaction.message.id,
                                                                embed = FilesManagerEmbed(path),
                                                                view = FilesManagerView(path))
                        await response.edit(content = client._('✔ `{}` has been deleted.').format(mcdis_path(path_to_remove)))
                        
        elif args[0].lower() == 'copy':
            if len(args) < 3: 
                await interaction.response.send_message(
                    client._('✖ You must provide two arguments. E.g.: `move <dir:index | file:index> <mcdis_path>`.'),
                    ephemeral = True)
            else:    
                path_to_copy = await file_or_dir_selection(args[1])
                if not path_to_copy: return

                path_provided = ' '.join(args[2:])
                new_path = os.path.join(un_mcdis_path(path_provided), os.path.basename(path_to_copy))
                dummy = client.is_valid_mcdis_path(path_provided)

                if not dummy == True:
                    await interaction.response.send_message(dummy, ephemeral = True)
                    return
                
                elif os.path.exists(new_path):
                    if os.path.isdir(new_path): msg = client._('✖ A folder with that name already exists at path.')
                    elif os.path.exists(new_path): msg = client._('✖ A file with that name already exists at path.')
                    await interaction.response.send_message(msg, ephemeral = True)
                    return
                
                await interaction.response.defer()
                response = await interaction.followup.send(client._('This action might take some time...'), ephemeral = True)
                await asyncio.sleep(1)

                if os.path.isdir(path_to_copy): 
                    await execute_and_wait(shutil.copytree, args = (path_to_copy, new_path))
                elif os.path.isfile(path_to_copy): 
                    await execute_and_wait(shutil.copy2, args = (path_to_copy, new_path))
                
                path_to_show = mcdis_path(os.path.relpath(un_mcdis_path(path_provided)))
                await interaction.followup.edit_message(message_id = interaction.message.id,
                                                        embed = FilesManagerEmbed(path),
                                                        view = FilesManagerView(path))
                await response.edit(content = client._('✔ `{}` has been copied to `{}`.').format(mcdis_path(path_to_copy), path_to_show))

        elif args[0].lower() == 'move':
            if len(args) < 3: 
                await interaction.response.send_message(
                    client._('✖ You must provide two arguments. E.g.: `move <dir:index | file:index> <mcdis_path>`.'),
                    ephemeral = True)
            else:
                path_to_move = await file_or_dir_selection(args[1])
                if not path_to_move: return

                path_provided = ' '.join(args[2:])
                new_path = os.path.join(un_mcdis_path(path_provided), os.path.basename(path_to_move))
                dummy = client.is_valid_mcdis_path(path_provided)

                if not dummy == True:
                    await interaction.response.send_message(dummy, ephemeral = True)
                    return
                
                elif os.path.exists(new_path):
                    if os.path.isdir(new_path): msg = client._('✖ A folder with that name already exists at path.')
                    elif os.path.exists(new_path): msg = client._('✖ A file with that name already exists at path.')
                    await interaction.response.send_message(msg, ephemeral = True)
                    return
                
                await interaction.response.defer()
                response : discord.Message = await interaction.followup.send(client._('This action might take some time...'), ephemeral = True)
                await asyncio.sleep(1)

                await execute_and_wait(shutil.move, args = (path_to_move, os.path.basename(path_provided)))
                
                path_to_show = mcdis_path(os.path.relpath(un_mcdis_path(path_provided)))
                await interaction.followup.edit_message(message_id = interaction.message.id,
                                                        embed = FilesManagerEmbed(path),
                                                        view = FilesManagerView(path))
                await response.edit(content = client._('✔ `{}` has been moved to `{}`.').format(mcdis_path(path_to_move), path_to_show))

        elif args[0].lower() == 'rename':
            name_provided = ' '.join(args[2:])

            if len(args) < 3: 
                await interaction.response.send_message(
                    client._('✖ You must provide two arguments. E.g.: `rename <dir:index | file:index> <new_name>`.'),
                    ephemeral = True)
                
            elif not is_valid_path_name(name_provided):
                await interaction.response.send_message(names_convention.format(name_provided), ephemeral = True)
            
            else:
                path_to_rename = await file_or_dir_selection(args[1])
            
                if path_to_rename:
                    new_path = os.path.join(path, name_provided[:100])
                    os.rename(path_to_rename, new_path)
                    await update_files_interface(client, interaction, path, path)

        else:
            await interaction.response.send_message( client._('✖ Invalid command `{}`.').format(args[0]), ephemeral=True)

class DeleteDirButton       (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = 'Delete Dir', style = discord.ButtonStyle.red)
        self.view : FilesManagerView

    async def callback(self, interaction: discord.Interaction):
        async def on_confirmation(confirmation_interaction: discord.Interaction): 
            new_path = os.path.relpath(os.path.abspath(os.path.dirname(self.view.path)))

            try: shutil.rmtree(self.view.path)
            except Exception as error: 
                await confirmation_interaction.response.edit_message(content = self.view.client._('Error: {}').format(error), embed = None, view = None)
            else:
                await confirmation_interaction.response.edit_message(delete_after=0)
                await interaction.followup.edit_message(message_id = interaction.message.id, 
                                                        embed = FilesManagerEmbed(new_path), 
                                                        view = FilesManagerView(new_path))
                
        await confirmation_request(self.view.client._('Are you sure about deleting the dir `{}`?').format(mcdis_path(self.view.path)), 
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