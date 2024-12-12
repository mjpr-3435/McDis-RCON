from ..modules import *
from ..classes import McDisClient

class on_scheduled_event_create(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        await self.client.call_addons('on_scheduled_event_create', (event,))

async def setup(client: McDisClient):
    await client.add_cog(on_scheduled_event_create(client))