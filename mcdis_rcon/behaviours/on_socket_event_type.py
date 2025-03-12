from ..modules import *
from ..classes import McDisClient

class on_socket_event_type(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_socket_event_type(self, event_type: str):
        await self.client.call_mdextras('on_socket_event_type', (event_type,))

async def setup(client: McDisClient):
    await client.add_cog(on_socket_event_type(client))