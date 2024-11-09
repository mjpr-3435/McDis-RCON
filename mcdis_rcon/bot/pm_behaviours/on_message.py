from ..pm_functions import *
from ..pm_classes import *
from ..modules import *

from ..loader import _, panel, config
from ..pm_loader import networks, servers, processes, flask_manager

async def pm_on_message(client: commands.Bot, message: discord.Message):
    from ..pm_banner import banner_creator

    if message.author.bot: return

    for process in processes: await process.discord_listener(message)

    if message.channel.id == panel.id:
        if message.content.lower() == f'{mcdis_prefix}start-all':
            await message.delete()
            for process in processes: process.start()

            await asyncio.sleep(1)
            asyncio.create_task(banner_creator(client, loop = False, views = False))
                
        elif message.content.lower() == f'{mcdis_prefix}stop-all':
            await message.delete()
            for process in processes: process.stop()
                            
        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}make-bkp':
            process_name = message.content.removeprefix(f'{mcdis_prefix}make-bkp').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()

            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}make-bkp <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            elif process.disk_usage(string = False) > psutil.disk_usage("/").free:
                response = await message.channel.send(content = _('✖ There\'s not enough space on the disk to create the backup.'))
                await response.delete(delay = 5)
                return

            elif process.state() != 'Closed':
                response = await message.channel.send(content = _('✖ The process must be closed to create the `.zip`.'))
                await response.delete(delay = 5)
                return
            
            response = await message.channel.send(_('`[{}]`: Compressing files...').format(process.name))
            
            counter = [0,0]
            task = threading.Thread(target = process.make_bkp, kwargs = {'counter' : counter})
            task.start()

            while task.is_alive():
                if counter[1] == 0: 
                    await asyncio.sleep(0.1)
                else:
                    show = _('`[{}]`: `[{}/{}]` files have been compressed...').format(process.name, counter[0], counter[1])
                    await response.edit(content = show)
                    await asyncio.sleep(0.5)

            await response.edit(content = _('✔ The files have been successfully compressed.'))
            await response.delete(delay = 5)

            await message.author.send(_('✔ The files have been successfully compressed.'))
        
        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}upload':
            path = message.content.removeprefix(f'{mcdis_prefix}upload').strip()

            if not path:
                response = await message.channel.send(_('✖ Specify the dir path to upload the files. E.g.: `{}upload <mcdis_path>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            elif not message.attachments:
                response = await message.channel.send(_('✖ You must add the files to upload.'))
                await response.delete(delay = 5)
                return

            dummy = is_valid_mcdis_dir(path)

            if not dummy == True:
                response = await message.channel.send(dummy)
                await response.delete(delay = 5)
            else:
                overwrite = config['Booleans']['upload overwrite']
                path_to_upload = un_mcdis_path(path)

                if overwrite:
                    response = await message.channel.send(_('Saving files...'))
                    await asyncio.sleep(2)

                    i = 1
                    for attachment in message.attachments:
                        path_to_save = os.path.join(path_to_upload, attachment.filename)
                        await attachment.save(path_to_save)
                        response = await response.edit(content = _('`[{}/{}]` Uploaded files.').format(i, len(message.attachments)))
                        i += 1
                    
                    response = await response.edit(content = _('✔ Files have been uploaded.'))
                    await response.delete(delay = 2)
                else:
                    response = await message.channel.send(_('Processing files...'))
                    await asyncio.sleep(2)

                    for attachment in message.attachments:
                        path_to_save = os.path.join(path_to_upload, attachment.filename)
                        path_to_show = mcdis_path(path_to_save)
                    
                        if not os.path.exists(path_to_save):
                            await attachment.save(path_to_save)
                            response = await response.edit(content = response.content + _('\n • `{}` uploaded.').format(attachment.filename))
                    
                        else:
                            response = await response.edit(content = response.content + _('\n • McDis will not overwrite the file `{}`.').format(path_to_show))
                        await asyncio.sleep(2)

                    response = await response.edit(content = response.content + _('\n ✔ Files have been processed.'))
                    await response.delete(delay = 2)
            
            await message.delete()
        
        elif message.content.lower() == f'{mcdis_prefix}restart':
            await message.delete()
            response = await message.channel.send(_('Checking if there are open processes...'))
            await asyncio.sleep(2)

            await restart(response)
    
async def restart(response: discord.Message):
    from ..pm_loader import processes

    any_process_open = lambda: any([process.state() in ['Open','Initializing'] for process in processes])

    if any_process_open():
        await response.edit(content = _('Closing processes...'))
        print(_('Closing processes...'))
        await asyncio.sleep(2)

    for process in processes: process.stop()
    
    i = 60
    while i > 0 and any_process_open():
        await response.edit(content = _('Processes will be forcibly closed in {} seconds...').format(i))
        print(_('Processes will be forcibly closed in {} seconds...').format(i))
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        i -= 1
        await asyncio.sleep(1)
    
    if any_process_open():
        for process in processes:
            process.kill()
        
        print(_('Processes forcibly closed.'))
    else:
        print(_('Processes closed.'))

    print(_('Restarting...'))

    await response.edit(content = _('Restarting...'))
    await response.delete(delay = 2)

    await asyncio.sleep(3)

    command = sys.argv[0]
    os.execv(command, sys.argv)
