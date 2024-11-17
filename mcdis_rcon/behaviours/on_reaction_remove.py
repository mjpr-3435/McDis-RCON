from ..modules import *
from ..classes import McDisClient

class on_reaction_remove(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_reaction_remove(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        await self.client.call_addons('on_reaction_remove', (self.client, reaction, user))

async def setup(client: McDisClient):
    await client.add_cog(on_reaction_remove(client))