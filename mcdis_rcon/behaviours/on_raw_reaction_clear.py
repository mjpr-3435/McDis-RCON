from ..modules import *
from ..classes import McDisClient

class on_raw_reaction_clear(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_raw_reaction_clear(self, payload: discord.RawReactionClearEvent):
        await self.client.call_addons('on_raw_reaction_clear', (self.client, payload))

async def setup(client: commands.Bot):
    await client.add_cog(on_raw_reaction_clear(client))