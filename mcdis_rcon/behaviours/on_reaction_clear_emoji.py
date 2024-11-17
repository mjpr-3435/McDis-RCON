from ..modules import *
from ..classes import McDisClient

class on_reaction_clear_emoji(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_reaction_clear_emoji(self, reaction: discord.Reaction):
        await self.client.call_addons('on_reaction_clear_emoji', (self.client, reaction))

async def setup(client: McDisClient):
    await client.add_cog(on_reaction_clear_emoji(client))