from ...pm_functions import *
from ...pm_classes import *
from ...modules import *
from ..embeds import *

from ...loader import _, config, panel
from ...pm_loader import servers, networks, processes, flask_manager

def files_manager_views(path: str = '.') -> discord.ui.View:
    options = []
    up_to_99 = False
    
    if os.path.isdir(path):
        dir_files = os.listdir(path)
        dir_files.sort()
        dirs = [file for file in dir_files if os.path.isdir(os.path.join(path,file))]
        files = [file for file in dir_files if os.path.isfile(os.path.join(path,file))]
        max_page = max(len(dirs)//99 + 1,len(files)//99 + 1)
        up_to_99 = len(dirs) > 99 or len(files) > 99
        
        for dir in dirs:
            options.append(discord.SelectOption(label = f'{emoji_dir} {truncate(dir,90)}', value = dir))

        for file in files:
            options.append(discord.SelectOption(label = f'{emoji_file} {truncate(file,90)}', value = file))

    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.page = 1

        if options:
            @discord.ui.select( placeholder = _('Select a file'), 
                                options = options[:25])
            async def path_selection(self, interaction: discord.Interaction, selection: discord.ui.Select):
                new_path = selection.values[0] if path == '.' else os.path.join(path, selection.values[0])
                
                await update_files_interface(interaction, new_path, path)
        if up_to_99:
            if max_page > 3:
                @discord.ui.button( label = '<<',
                                    style = discord.ButtonStyle.gray,
                                    row = 2)
                async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.page = 1
                    await interaction.response.edit_message(embed = files_manager_embed(path, self.page))

            @discord.ui.button( label = '<',
                                style = discord.ButtonStyle.gray,
                                row = 2)
            async def previous_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.page = self.page - 1 if self.page > 1 else 1
                await interaction.response.edit_message(embed = files_manager_embed(path, self.page))

            @discord.ui.button( label = '>',
                                style = discord.ButtonStyle.gray,
                                row = 2)
            async def next_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.page = self.page + 1 if self.page < max_page else max_page
                await interaction.response.edit_message(embed = files_manager_embed(path, self.page))

            if max_page > 3:
                @discord.ui.button( label = '>>',
                                    style = discord.ButtonStyle.gray,
                                    row = 2)
                async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.page = max_page
                    await interaction.response.edit_message(embed = files_manager_embed(path, self.page))

        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            new_path = os.path.abspath(os.path.dirname(path))
            if not cwd in new_path: new_path = cwd
            new_path = os.path.relpath(new_path, cwd)

            await update_files_interface(interaction, new_path, path)

        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await update_files_interface(interaction, path, path)
        
        if not os.path.isdir(path):
            @discord.ui.button( label = 'Request',
                        style = discord.ButtonStyle.gray)
            async def request_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                
                if not config['Booleans']['allow flask']:
                    await interaction.response.defer(ephemeral = True, thinking = True)

                    if get_path_size(path, string = False) > request_size_limit:
                        await interaction.followup.send(_('✖ McDis only accepts file requests of up to 5MB.'))
                    else:
                        await interaction.followup.send(f'> **{mcdis_path(path)}:**', file = discord.File(path))
                else:
                    download_link = flask_manager.download_link(path, interaction.user.name)
                    view = self.remove_item(button).add_item(discord.ui.Button(label = 'Download', url = download_link))
                    embed = interaction.message.embeds[0]
                    embed.description = f'**Download Link**:\n```{download_link}```'
                    await interaction.response.edit_message(embed=embed, view = view)
                        


            @discord.ui.button( label = 'Edit',
                        style = discord.ButtonStyle.gray)
            async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                file_content = None
                
                if not get_path_size(path, string = False) > request_size_limit:
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            file_content =  file.read()

                        if len(file_content) >= 4000: 
                            file_content = None
                    except:
                        file_content = None
                    
                class edit_command(discord.ui.Modal, title = _('Edit the file')):
                    name = discord.ui.TextInput(label = _('File'), style = discord.TextStyle.short, default = os.path.basename(path))
                    if file_content: content = discord.ui.TextInput(label = os.path.basename(path), style = discord.TextStyle.paragraph, default = file_content)

                    async def on_submit(modal, interaction: discord.Interaction):
                        new_path = os.path.join(os.path.dirname(path), os.path.basename(str(modal.name)))

                        try:
                            if file_content:
                                with open(path, 'w') as file:
                                    for line in str(modal.content).split('\n'):
                                        file.write(line + '\n')

                            os.rename(path, new_path)
                        except Exception as error:
                            await interaction.response.send_message(content = _('Error: {}').format(error), ephemeral=True)
                            return
                        
                        await interaction.response.edit_message(embed = files_manager_embed(new_path), view = files_manager_views(new_path))
    
                await interaction.response.send_modal(edit_command())

            @discord.ui.button( label = 'Delete',
                        style = discord.ButtonStyle.red)
            async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                async def on_confirmation(confirmation_interaction: discord.Interaction): 
                    new_path = os.path.relpath(os.path.abspath(os.path.dirname(path)))

                    try: os.remove(path)
                    except Exception as error: 
                        await confirmation_interaction.response.edit_message(content = _('Error: {}').format(error), embed = None, view = None)
                    else:
                        await confirmation_interaction.response.edit_message(delete_after = 0)
                        await interaction.followup.edit_message(message_id=interaction.message.id, 
                                                                embed = files_manager_embed(new_path), 
                                                                view = files_manager_views(new_path))
                        
                await confirmation_request(_('Are you sure about deleting the file `{}`?').format(mcdis_path(path)), 
                                           on_confirmation = on_confirmation,
                                           interaction = interaction)

        else:
            @discord.ui.button( label = 'Processes',
                                style = discord.ButtonStyle.gray)
            async def processes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                from .processes import processes_views
                await interaction.response.defer()

                processes = []
                for process in psutil.process_iter():
                    try:
                        if os.path.abspath(path) in process.cwd():
                            processes.append(process)
                    except: pass
                    
                processes = sorted(processes, key=lambda p: p.cwd())

                await interaction.followup.edit_message(message_id = interaction.message.id, 
                                                        embed = processes_embed(path, processes), 
                                                        view = processes_views(path, processes))

            @discord.ui.button( label = 'Terminal',
                                style = discord.ButtonStyle.gray)
            async def terminal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                class message_modal(discord.ui.Modal, title = _('Terminal')):
                    command = discord.ui.TextInput(label = truncate('> ' + mcdis_path(path), 45), style = discord.TextStyle.paragraph)
                    example = discord.ui.TextInput(label = _('Commands'), style = discord.TextStyle.paragraph, default = "\n".join(terminal_commands))
                
                    async def on_submit(modal, interaction: discord.Interaction):
                        await cmd_interface(str(modal.command), interaction, path, self)
                await interaction.response.send_modal(message_modal())

            if not path == '.': 

                @discord.ui.button( label = 'Delete Dir',
                                    style = discord.ButtonStyle.red)
                async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    async def on_confirmation(confirmation_interaction: discord.Interaction): 
                        new_path = os.path.relpath(os.path.abspath(os.path.dirname(path)))

                        try: shutil.rmtree(path)
                        except Exception as error: 
                            await confirmation_interaction.response.edit_message(content = _('Error: {}').format(error), embed = None, view = None)
                        else:
                            await confirmation_interaction.response.edit_message(delete_after=0)
                            await interaction.followup.edit_message(message_id = interaction.message.id, 
                                                                    embed = files_manager_embed(new_path), 
                                                                    view = files_manager_views(new_path))
                            
                    await confirmation_request(_('Are you sure about deleting the dir `{}`?').format(mcdis_path(path)), 
                                               on_confirmation = on_confirmation,
                                               interaction = interaction)
                    
    return views()

async def cmd_interface(command: str, interaction: discord.Interaction, path: str, view: discord.ui.View):
    args = command.split(' ')
    names_convention = _('✖ The names of directories created with McDis can only contain letters, '
                         'numbers, periods (.), hyphens (-), and underscores (_). Provided name: `{}`')
    
    dir_files = os.listdir(path)
    dir_files.sort()
    dirs = [file for file in dir_files if os.path.isdir(os.path.join(path,file))]
    files = [file for file in dir_files if os.path.isfile(os.path.join(path,file))]

    
    async def file_or_dir_selection(arg : str) -> Union[str, None]:
        if arg.lower().startswith('dir:'):
            try: index = int(arg[4:])
            except:
                await interaction.response.send_message( _('✖ The index must be an integer.'), ephemeral=True)
                return
            
            if index < 1 or index > min(len(dirs),99):
                await interaction.response.send_message( _('✖ No directory exists with that index.'), ephemeral=True)
                return

            return dirs[(view.page-1)*99 + index- 1] if path == '.' else os.path.join(path, dirs[(view.page-1)*99 + index- 1])

        elif arg.lower().startswith('file:'):
            try:
                index = int(arg[5:])
            except: 
                await interaction.response.send_message( _('✖ The index must be an integer.'), ephemeral=True)
                return
            
            if index < 1 or index > min(len(files),99):
                await interaction.response.send_message( _('✖ No file exists with that index.'), ephemeral=True)
                return

            return files[(view.page-1)*99 + index- 1] if path == '.' else os.path.join(path,files[(view.page-1)*99 + index- 1])
        
        else:
            await interaction.response.send_message(
                _('✖ Invalid argument `{}`. It should be `dir:index` or `file:index`.').format(arg),
                ephemeral=True)
            return

    if args[0].lower() == 'mkdir':
        if len(args) == 1: 
            await interaction.response.send_message(
                _('✖ You must provide one argument. E.g.: `mkdir <name>`.'), 
                ephemeral = True)
            
        elif not is_valid_path_name(args[1]):
            await interaction.response.send_message(names_convention.format(args[1]), ephemeral=True)
        else:
            os.makedirs(os.path.join(path, args[1]), exist_ok = True)
            await update_files_interface(interaction, path, path)
    
    elif args[0].lower() == 'zip':
        if len(args) == 1: 
            await interaction.response.send_message(
                _('✖ You must provide one argument. E.g.: `zip <dir:index>`.'), 
                ephemeral=True)
        else:
            path_to_zip = await file_or_dir_selection(args[1])
            if not path_to_zip: return

            elif not os.path.isdir(path_to_zip):
                await interaction.response.send_message(_('✖ The path must be a directory.'), ephemeral=True)
                return
            elif get_path_size(path_to_zip, string = False) > psutil.disk_usage("/").free:
                await interaction.response.send_message(_('✖ There\'s not enough space on the disk to create this `.zip`.'), ephemeral=True)
                return
            
            await interaction.response.defer(ephemeral = True, thinking = True)

            response = await interaction.followup.send(_('`[{}]`: Compressing files...').format(path_to_zip + '.zip'))
            
            counter = [0,0]
            task = threading.Thread(target = make_zip, args = (path_to_zip, path_to_zip + '.zip', counter))
            task.start()

            while task.is_alive():
                if counter[1] == 0: 
                    await asyncio.sleep(0.1)
                else:
                    show = _('`[{}]`: `[{}/{}]` files have been compressed...').format(path_to_zip + '.zip', counter[0], counter[1])
                    await response.edit(content = show)
                    await asyncio.sleep(0.5)

            await update_files_interface(interaction, path, path)
            await response.edit(content = _('✔ The files have been successfully compressed.'))
            await interaction.user.send(content = _('✔ The files have been successfully compressed.'))

    elif args[0].lower() == 'unzip':
        if len(args) == 1: 
            await interaction.response.send_message(
                _('✖ You must provide one argument. E.g.: `unzip <file:index>`.'), 
                ephemeral=True)
        else:
            path_to_unzip = await file_or_dir_selection(args[1])
            if not path_to_unzip: return

            elif not os.path.isfile(path_to_unzip) or not path_to_unzip.endswith('.zip'):
                await interaction.response.send_message(_('✖ The path must be a `.zip` file.'), ephemeral=True)
                return
            
            elif os.path.exists(path_to_unzip[:-4]):
                await interaction.response.send_message(_('✖ A folder named `{}` already exists.').format(os.path.basename(path_to_unzip[:-4])), ephemeral=True)
                return
            
            await interaction.response.defer()
            response : discord.Message = await interaction.followup.send(_('Unpacking Backup...'), ephemeral = True)
            counter = [0,0]
            
            task = threading.Thread(target = unpack_zip, args = (path_to_unzip, path_to_unzip[:-4], counter))
            task.start()
            
            while task.is_alive():
                if counter[1] == 0 or not isinstance(counter[1], int): 
                    await asyncio.sleep(0.1)
                else:
                    show = _('`[{}]`: `[{}/{}]` files have been unpacked...').format(path_to_unzip[:-4], counter[0], counter[1])
                    await response.edit(content = show)
                    await asyncio.sleep(0.5)
            
            if not isinstance(counter[1], int):
                msg = _('✖ There was an error while unpacking. Error: {}').format(counter[1])
                await interaction.user.send(msg)
                await response.edit(content = msg)
            else:
                await update_files_interface(interaction, path, path)
                msg = _('✔ The files have been successfully unpacked.')
                await interaction.user.send(msg)
                await response.edit(content = msg)


    elif args[0].lower() == 'cd':
        if len(args) == 1: 
            await interaction.response.send_message(
                _('✖ You must provide one argument. E.g.: `cd <dir:index | file:index>`.'), 
                ephemeral=True)
        else:
            new_path = await file_or_dir_selection(args[1])

            if new_path: await update_files_interface(interaction, new_path, path)

    elif args[0].lower() == 'del':
        if len(args) == 1: 
            await interaction.response.send_message(
                _('✖ You must provide one argument. E.g.: `del <dir:index | file:index>`.'),
                ephemeral = True)
        else:
            path_to_remove = await file_or_dir_selection(args[1])

            if path_to_remove:
                await interaction.response.defer()
                response : discord.Message = await interaction.followup.send(_('This action might take some time...'), ephemeral = True)
                await asyncio.sleep(1)
                try:
                    if os.path.isdir(path_to_remove): 
                        await excute_and_wait(shutil.rmtree, args = (path_to_remove, ))
                    elif os.path.isfile(path_to_remove): 
                        await excute_and_wait(os.remove, args = (path_to_remove, ))
                except Exception as error:
                    await response.edit(content = _('Error: {}').format(error))
                else:
                    await interaction.followup.edit_message(message_id = interaction.message.id,
                                                            embed = files_manager_embed(path),
                                                            view = files_manager_views(path))
                    await response.edit(content = _('✔ `{}` has been deleted.').format(mcdis_path(path_to_remove)))
                    
    elif args[0].lower() == 'copy':
        if len(args) < 3: 
            await interaction.response.send_message(
                _('✖ You must provide two arguments. E.g.: `move <dir:index | file:index> <mcdis_path>`.'),
                ephemeral = True)
        else:    
            path_to_copy = await file_or_dir_selection(args[1])
            if not path_to_copy: return

            path_provided = ' '.join(args[2:])
            new_path = os.path.join(un_mcdis_path(path_provided), os.path.basename(path_to_copy))
            dummy = is_valid_mcdis_dir(path_provided)

            if not dummy == True:
                await interaction.response.send_message(dummy, ephemeral = True)
                return
            
            elif os.path.exists(new_path):
                if os.path.isdir(new_path): msg = _('✖ A folder with that name already exists at path.')
                elif os.path.exists(new_path): msg = _('✖ A file with that name already exists at path.')
                await interaction.response.send_message(msg, ephemeral = True)
                return
            
            await interaction.response.defer()
            response = await interaction.followup.send(_('This action might take some time...'), ephemeral = True)
            await asyncio.sleep(1)

            if os.path.isdir(path_to_copy): 
                await excute_and_wait(shutil.copytree, args = (path_to_copy, new_path))
            elif os.path.isfile(path_to_copy): 
                await excute_and_wait(shutil.copy2, args = (path_to_copy, new_path))
            
            path_to_show = mcdis_path(os.path.relpath(un_mcdis_path(path_provided)))
            await interaction.followup.edit_message(message_id = interaction.message.id,
                                                    embed = files_manager_embed(path),
                                                    view = files_manager_views(path))
            await response.edit(content = _('✔ `{}` has been copied to `{}`.').format(mcdis_path(path_to_copy), path_to_show))

    elif args[0].lower() == 'move':
        if len(args) < 3: 
            await interaction.response.send_message(
                _('✖ You must provide two arguments. E.g.: `move <dir:index | file:index> <mcdis_path>`.'),
                ephemeral = True)
        else:
            path_to_move = await file_or_dir_selection(args[1])
            if not path_to_move: return

            path_provided = ' '.join(args[2:])
            new_path = os.path.join(un_mcdis_path(path_provided), os.path.basename(path_to_move))
            dummy = is_valid_mcdis_dir(path_provided)

            if not dummy == True:
                await interaction.response.send_message(dummy, ephemeral = True)
                return
            
            elif os.path.exists(new_path):
                if os.path.isdir(new_path): msg = _('✖ A folder with that name already exists at path.')
                elif os.path.exists(new_path): msg = _('✖ A file with that name already exists at path.')
                await interaction.response.send_message(msg, ephemeral = True)
                return
            
            await interaction.response.defer()
            response : discord.Message = await interaction.followup.send(_('This action might take some time...'), ephemeral = True)
            await asyncio.sleep(1)

            await excute_and_wait(shutil.move, args = (path_to_move, os.path.basename(path_provided)))
            
            path_to_show = mcdis_path(os.path.relpath(un_mcdis_path(path_provided)))
            await interaction.followup.edit_message(message_id = interaction.message.id,
                                                    embed = files_manager_embed(path),
                                                    view = files_manager_views(path))
            await response.edit(content = _('✔ `{}` has been moved to `{}`.').format(mcdis_path(path_to_move), path_to_show))

    elif args[0].lower() == 'rename':
        name_provided = ' '.join(args[2:])

        if len(args) < 3: 
            await interaction.response.send_message(
                _('✖ You must provide two arguments. E.g.: `rename <dir:index | file:index> <new_name>`.'),
                ephemeral = True)
            
        elif not is_valid_path_name(name_provided):
            await interaction.response.send_message(names_convention.format(name_provided), ephemeral = True)
        
        else:
            path_to_rename = await file_or_dir_selection(args[1])
        
            if path_to_rename:
                new_path = os.path.join(path, name_provided[:100])
                os.rename(path_to_rename, new_path)
                await update_files_interface(interaction, path, path)
 
    else:
        await interaction.response.send_message( _('✖ Invalid command`{}`.').format(args[0]), ephemeral=True)

      
async def update_files_interface(interaction : discord.Interaction, new_path : str, path : str):
    if not interaction.response.is_done():
        await interaction.response.defer()
    from .commands import commands_views
    from .backups import backups_views
    new_path = os.path.abspath(new_path)
    path = os.path.abspath(path)
    dummy_path = ''

    if new_path == path:
        new_path = os.path.relpath(new_path, cwd)
        await interaction.followup.edit_message(message_id = interaction.message.id, embed = files_manager_embed(new_path), view = files_manager_views(new_path))
        return
    elif path in new_path:
        dummy_path = new_path
    elif new_path in path:
        dummy_path = path

    dummy_path = os.path.relpath(dummy_path, cwd)
    process_cmd = next(filter(lambda process: dummy_path == process.path_commands, processes), None)
    process_bkp = next(filter(lambda process: dummy_path == process.path_bkps, processes), None)

    if process_cmd:
        await interaction.followup.edit_message(message_id = interaction.message.id, embed = commands_embed(process_cmd), view = commands_views(process_cmd))
    elif process_bkp:
        await interaction.followup.edit_message(message_id = interaction.message.id, embed = backups_embed(process_bkp), view = backups_views(process_bkp))
    else:
        new_path = os.path.relpath(new_path, cwd)
        await interaction.followup.edit_message(message_id = interaction.message.id, embed = files_manager_embed(new_path), view = files_manager_views(new_path))