from ..modules import *
from ..classes import McDisClient

class on_scheduled_event_user_remove(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_scheduled_event_user_remove(self, event: discord.ScheduledEvent, user: discord.User):
        await self.client.call_addons('on_scheduled_event_user_remove', (event, user))

async def setup(client: McDisClient):
    await client.add_cog(on_scheduled_event_user_remove(client))