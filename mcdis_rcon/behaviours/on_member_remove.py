from ..modules import *
from ..classes import McDisClient

class on_member_remove(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_member_remove(self, member: discord.Member):
        await self.client.call_mdextras('on_member_remove', (member,))

async def setup(client: McDisClient):
    await client.add_cog(on_member_remove(client))