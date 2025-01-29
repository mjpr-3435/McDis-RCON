import os
import asyncio
import sys

from mcdis_rcon.classes import McDisClient

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client
        
        asyncio.create_task(self.load())

    async def load(self):
        sys.path.insert(0, self.client.path_addons)

        cogs = ['Commands', 'ContextMenus']

        for cog in cogs:
            cog_path = os.path.join(self.client.path_addons, cog)
            os.makedirs(cog_path, exist_ok = True)
            scripts = [file.removesuffix('.py') for file in os.listdir(cog_path) if file.endswith('.py')]

            for script in scripts:
                await self.client.load_extension(f'{cog}.{script}')

        sys.path.pop(0)
        
        await self.client.tree.sync()