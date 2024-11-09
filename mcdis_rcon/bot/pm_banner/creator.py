from ..pm_functions import *
from ..modules import *

from ..loader import _, panel, config

async def banner_creator(client: commands.Bot, *, loop: bool = True, views: bool = True):
    from .embeds import banner_embed
    from .views import banner_views
    first_iteration = True

    while loop or first_iteration:
        first_iteration = False
        file = None

        if os.path.exists('banner.png'):
            file = discord.File('banner.png')

        try:
            messages =  [msg async for msg in panel.history(limit = None, oldest_first = True)]
            
            if len(messages) == 0:
                await panel.send(embed = banner_embed(), view = banner_views(), file = file)

            elif messages[0].author.id == client.user.id:
                if views:
                    await messages[0].edit(embed = banner_embed(), view = banner_views(), attachments = [file] if file else [])
                else:
                    await messages[0].edit(embed = banner_embed(), attachments = [file] if file else [])  
            
            else:
                await panel.purge(limit = 100)
                await banner_creator(client, loop = False)

        except Exception as error:
            print(_('Error: {}').format(f'{error}\n{traceback.format_exc()}'))

        if loop:
            views = False
            await asyncio.sleep(15)
