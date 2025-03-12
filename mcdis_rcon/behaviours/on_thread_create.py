from ..modules import *
from ..classes import McDisClient

class on_thread_create(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_thread_create(self, thread: discord.Thread):
        await self.client.call_mdextras('on_thread_create', (thread,))

async def setup(client: McDisClient):
    await client.add_cog(on_thread_create(client))