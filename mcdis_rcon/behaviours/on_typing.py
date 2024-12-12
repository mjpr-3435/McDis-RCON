from ..modules import *
from ..classes import McDisClient

class on_typing(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_typing(self, channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime):
        await self.client.call_addons('on_typing', (channel, user, when))
    
async def setup(client: McDisClient):
    await client.add_cog(on_typing(client))
