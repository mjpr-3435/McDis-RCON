from ..modules import *
from ..classes import McDisClient

class on_scheduled_event_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_scheduled_event_delete(self, event: discord.ScheduledEvent):
        await self.client.call_addons('on_scheduled_event_delete', (self.client, event))

async def setup(client: McDisClient):
    await client.add_cog(on_scheduled_event_delete(client))