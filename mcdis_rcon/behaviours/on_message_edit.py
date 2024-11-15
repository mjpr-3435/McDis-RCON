from ..modules import *
from ..classes import McDisClient

class on_message_edit(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.client.call_addons('on_message_edit', (self.client, before, after))

async def setup(client: commands.Bot):
    await client.add_cog(on_message_edit(client))