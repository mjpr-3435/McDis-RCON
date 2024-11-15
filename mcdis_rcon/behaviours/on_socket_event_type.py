from ..modules import *
from ..classes import McDisClient

class on_socket_event_type(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_socket_event_type(self, event_type: str):
        await self.client.call_addons('on_socket_event_type', (self.client, event_type))

async def setup(client: commands.Bot):
    await client.add_cog(on_socket_event_type(client))