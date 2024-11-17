from ..modules import *
from ..classes import McDisClient

class on_raw_member_remove(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        await self.client.call_addons('on_raw_member_remove', (self.client, payload))

async def setup(client: McDisClient):
    await client.add_cog(on_raw_member_remove(client))