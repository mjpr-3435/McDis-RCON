from ..modules import *
from ..classes import McDisClient

class on_socket_raw_receive(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_socket_raw_receive(self, message: str):
        await self.client.call_mdextras('on_socket_raw_receive', (message,))

async def setup(client: McDisClient):
    await client.add_cog(on_socket_raw_receive(client))