from ..modules import *

async def thread(name: str, channel: discord.TextChannel, *, public: bool = False) -> discord.Thread:
    async for thread in channel.archived_threads():
        await thread.edit(archived = False)
    
    thread = next(filter(lambda x: x.name == name, channel.threads), None)

    if thread: 
        return thread
    
    if not public:
        thread = await channel.create_thread(name = name.strip())
        return thread

    else:
        message = await channel.send('_')
        thread = await channel.create_thread(name = name.strip(), message = message)
        await message.delete()
        return thread
    
async def confirmation_request( description     : str                              ,*,
                                on_confirmation : Callable                  = None ,
                                on_reject       : Callable                  = None , 
                                interaction     : discord.Interaction       = None ,
                                channel         : discord.TextChannel       = None ,
                                ephemeral       : bool                      = True  ):
    
    class confirmation_views(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)

        @discord.ui.button( label = '✔',
                            style = discord.ButtonStyle.gray)
        async def proceed_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not on_confirmation: 
                await interaction.response.edit_message(delete_after=0)
                return

            if inspect.iscoroutinefunction(on_confirmation):
                await on_confirmation(interaction)
            else:
                on_confirmation(interaction)
        
        @discord.ui.button( label = '✖',
                            style = discord.ButtonStyle.red)
        async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not on_reject:
                await interaction.response.edit_message(delete_after=0)
                return

            if inspect.iscoroutinefunction(on_confirmation):
                await on_reject(interaction)
            else:
                on_reject(interaction)
        
    if interaction:
        await interaction.response.send_message(embed       = discord.Embed(description = description), 
                                                view        = confirmation_views(),
                                                ephemeral   = ephemeral)
    elif channel:
        await channel.send(embed       = discord.Embed(description = description), 
                           view        = confirmation_views())