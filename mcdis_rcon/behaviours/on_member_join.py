from ..modules import *
from ..classes import McDisClient

class on_member_join(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_member_join(self, member: discord.Member):
        await self.client.call_addons('on_member_join', (self.client, member))

async def setup(client: commands.Bot):
    await client.add_cog(on_member_join(client))