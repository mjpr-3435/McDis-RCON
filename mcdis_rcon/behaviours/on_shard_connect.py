from ..modules import *
from ..classes import McDisClient

class on_shard_connect(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_shard_connect(self, shard_id: int):
        await self.client.call_addons('on_shard_connect', (shard_id,))

async def setup(client: McDisClient):
    await client.add_cog(on_shard_connect(client))