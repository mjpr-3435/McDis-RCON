from ..modules import *
from ..classes import McDisClient

class on_user_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_user_update(self, before: discord.User, after: discord.User):
        await self.client.call_addons('on_user_update', (self.client, before, after))

async def setup(client: commands.Bot):
    await client.add_cog(on_user_update(client))