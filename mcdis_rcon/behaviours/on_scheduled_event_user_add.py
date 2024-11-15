from ..modules import *
from ..classes import McDisClient

class on_scheduled_event_user_add(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_scheduled_event_user_add(self, event: discord.ScheduledEvent, user: discord.User):
        await self.client.call_addons('on_scheduled_event_user_add', (self.client, event, user))

async def setup(client: commands.Bot):
    await client.add_cog(on_scheduled_event_user_add(client))