from ..modules import *
from ..classes import McDisClient

class on_member_ban(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        await self.client.call_addons('on_member_ban', (guild, user))

async def setup(client: McDisClient):
    await client.add_cog(on_member_ban(client))