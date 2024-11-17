from ...modules import *
from ...classes import *
from ...utils import *
from ..embeds import *


def backups_views(client: McDisClient, process: Process) -> discord.ui.View:
    from .files_manager import files_manager_views
    
    pattern = os.path.join(process.path_bkps, f'{process.name} [1-{client.config["Backups"]}].zip')
    bkps = glob.glob(pattern)
    bkps.sort()
    options = []

    for i in range(len(bkps)):
        options.append(discord.SelectOption(label = f'{i+1}. {os.path.basename(bkps[i])}', value = os.path.basename(bkps[i])) )
    
    class views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
        
        if len(options):
            @discord.ui.select( placeholder = client._('Select a backup'), 
                                options = options[:25])
            async def farm_command_selection(self, interaction: discord.Interaction, selection: discord.ui.Select):
                class message_modal(discord.ui.Modal, title = os.path.basename(str(selection.values[0]))):
                    action = discord.ui.TextInput(label = client._('Type \'unpack\' or \'delete\' here'), style = discord.TextStyle.short)
                    
                    async def on_submit(modal, interaction: discord.Interaction):
                        if str(modal.action).lower() == client._('unpack'):
                            if process.is_running() in ['Initializing','Open']: 
                                await interaction.response.send_message(content= client._('✖ The process must be closed.'), ephemeral=True,delete_after=5)
                                return

                            
                            await interaction.response.defer()
                            response : discord.Message = await interaction.followup.send(client._('Unpacking Backup...'), ephemeral = True)
                            counter = [0,0]
                            
                            task = threading.Thread(target = process.unpack_bkp, args = (str(selection.values[0]),), kwargs = {'counter' : counter})
                            task.start()
                            
                            while task.is_alive():
                                if counter[1] == 0 or not isinstance(counter[1], int): 
                                    await asyncio.sleep(0.1)
                                else:
                                    show = client._('`[{}]`: `[{}/{}]` files have been unpacked...').format(process.name, counter[0], counter[1])
                                    await response.edit(content = show)
                                    await asyncio.sleep(0.5)
                            
                            if not isinstance(counter[1], int):
                                msg = client._('✖ There was an error while unpacking. Error: {}').format(counter[1])
                                await interaction.user.send(msg)
                                await response.edit(content = msg)
                            else:
                                msg = client._('✔ The files have been successfully unpacked.')
                                await interaction.user.send(msg)
                                await response.edit(content = msg)

                        elif str(modal.action).lower() == client._('delete'):         
                            try: os.remove(os.path.join(process.path_bkps,str(selection.values[0])))
                            except Exception as error: 
                                await interaction.response.edit_message(content = client._('Error: {}').format(error), embed = None, view = None)
                            else:
                                await interaction.response.send_message(client._('✔ File deleted.'), ephemeral = True)
                        else:
                            await interaction.response.send_message(content = client._('✖ Action `{}` not recognized.').format(str(modal.action).lower()), ephemeral=True)
                        
                        await interaction.followup.edit_message(message_id=interaction.message.id, embed = backups_embed(process), view = backups_views(process))
                        
                await interaction.response.send_modal(message_modal())
                
        @discord.ui.button( label = emoji_arrow_left,
                            style = discord.ButtonStyle.gray)
        async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(embed = files_manager_embed('.mdbackups'), view = files_manager_views('.mdbackups'))

        @discord.ui.button( label = emoji_update,
                            style = discord.ButtonStyle.gray)
        async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(embed = backups_embed(process), view = backups_views(process))
        
        @discord.ui.button( label = emoji_dir,
                            style = discord.ButtonStyle.gray)
        async def files_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(embed = files_manager_embed(process.path_bkps), view = files_manager_views(process.path_bkps))

    return views()
