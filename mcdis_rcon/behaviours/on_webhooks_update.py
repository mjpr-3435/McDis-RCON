from ..modules import *
from ..classes import McDisClient

class on_webhooks_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_webhooks_update', (channel,))

async def setup(client: McDisClient):
    await client.add_cog(on_webhooks_update(client))