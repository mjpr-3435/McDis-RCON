from ..modules import *
from ..classes import McDisClient

class on_interaction(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_interaction(self, interaction: discord.Interaction):
        await self.client.call_addons('on_interaction', (interaction,))

async def setup(client: McDisClient):
    await client.add_cog(on_interaction(client))