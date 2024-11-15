from ..modules import *
from ..classes import McDisClient

class on_thread_remove(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_thread_remove(self, thread: discord.Thread):
        await self.client.call_addons('on_thread_remove', (self.client, thread))

async def setup(client: commands.Bot):
    await client.add_cog(on_thread_remove(client))