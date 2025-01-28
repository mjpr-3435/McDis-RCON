import os
import asyncio
import sys

from mcdis_rcon.classes import McDisClient

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client
        
        asyncio.create_task(self.load())

    async def load(self):
        addon_path = os.path.dirname(__file__)

        sys.path.insert(0, os.path.dirname(__file__))

        cogs = ['Commands', 'ContextMenus']

        for cog in cogs:
            cog_path = os.path.join(addon_path, cog)
            scripts = [file.removesuffix('.py') for file in os.listdir(cog_path) if file.endswith('.py')]

            for script in scripts:
                await self.client.load_extension(f'{cog}.{script}')

        sys.path.pop(0)
        
        await self.client.tree.sync()