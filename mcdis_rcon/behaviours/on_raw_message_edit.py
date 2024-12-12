from ..modules import *
from ..classes import McDisClient

class on_raw_message_edit(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        await self.client.call_addons('on_raw_message_edit', (payload,))

async def setup(client: McDisClient):
    await client.add_cog(on_raw_message_edit(client))