from ..modules import *
from ..classes import McDisClient

class on_raw_app_command_permissions_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()

    async def on_raw_app_command_permissions_update(self, payload: discord.RawAppCommandPermissionsUpdateEvent):
        await self.client.call_mdextras('on_raw_app_command_permissions_update', (payload,))

async def setup(client: McDisClient):
    await client.add_cog(on_raw_app_command_permissions_update(client))
