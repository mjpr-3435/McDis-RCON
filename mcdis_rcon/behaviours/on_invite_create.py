from ..modules import *
from ..classes import McDisClient

class on_invite_create(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_invite_create(self, invite: discord.Invite):
        await self.client.call_addons('on_invite_create', (invite,))

async def setup(client: McDisClient):
    await client.add_cog(on_invite_create(client))