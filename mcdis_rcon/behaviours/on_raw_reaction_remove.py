from ..modules import *
from ..classes import McDisClient

class on_raw_reaction_remove(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await self.client.call_addons('on_raw_reaction_remove', (self.client, payload))

async def setup(client: commands.Bot):
    await client.add_cog(on_raw_reaction_remove(client))