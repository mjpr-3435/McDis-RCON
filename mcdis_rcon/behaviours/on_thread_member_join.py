from ..modules import *
from ..classes import McDisClient

class on_thread_member_join(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_thread_member_join(self, member: discord.ThreadMember):
        await self.client.call_addons('on_thread_member_join', (self.client, member))

async def setup(client: McDisClient):
    await client.add_cog(on_thread_member_join(client))