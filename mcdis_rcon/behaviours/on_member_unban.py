from ..modules import *
from ..classes import McDisClient

class on_member_unban(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        await self.client.call_mdextras('on_member_unban', (guild, user))

async def setup(client: McDisClient):
    await client.add_cog(on_member_unban(client))