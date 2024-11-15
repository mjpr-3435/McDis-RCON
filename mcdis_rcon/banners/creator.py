from ..utils import *
from ..modules import *

from ..classes import McDisClient

async def banner_creator(client: McDisClient, *, loop: bool = True, view: bool = True):
    from .embeds import banner_embed
    from .views import banner_views
    file = None

    if os.path.exists('banner.png'): 
        file = discord.File('banner.png')

    try:
        messages =  [msg async for msg in client.panel.history(limit = None, oldest_first = True)]
        
        if not messages:
            await client.panel.send(embed = banner_embed(), view = banner_views(), file = file)

        elif not messages[0].author.id == client.user.id:
            while messages:
                await client.panel.purge(limit = 100)
                messages =  [msg async for msg in client.panel.history(limit = None, oldest_first = True)]

        elif not view:
            await messages[0].edit(embed = banner_embed(), attachments = [file] if file else [])

        else:
            await messages[0].edit(embed = banner_embed(), view = banner_views(), attachments = [file] if file else [])

    except Exception as error:
        print(client._('Error: {}').format(f'{error}\n{traceback.format_exc()}'))

    if loop:
        await asyncio.sleep(15)
        await asyncio.create_task(banner_creator(client, view = view))
