from ..modules import *
from ..classes import McDisClient

class on_automod_action(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_automod_action(self, execution: discord.AutoModAction):
        await self.client.call_mdextras('on_automod_action', (execution,))
    
async def setup(client: McDisClient):
    await client.add_cog(on_automod_action(client))
