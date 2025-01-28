import os
import importlib.util

from mcdis_rcon.classes import McDisClient

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client

    async def load(self):
        cogs = [os.path.join(self.client.path_addons, 'BotExtensions', dir) for dir in ['Commands', 'ContextMenus']]

        for cog in cogs:
            scripts = [file for file in os.listdir(cog) if file.endswith('.py')]

            for script in scripts:
                module_path = os.path.join(cog, script)
                
                spec = importlib.util.spec_from_file_location(script, module_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                await self.client.load_extension(mod)

    """spec = importlib.util.find_spec(module_path)
    if spec is None:
        raise ImportError(f"No se pudo encontrar el módulo: {module_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    await self.client.load_extension(module_path)"""

        