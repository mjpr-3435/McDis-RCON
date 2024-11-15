from ..modules import *
from ..classes import McDisClient

class on_private_channel_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()

    async def on_private_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        await self.client.call_addons('on_private_channel_update', (self.client, before, after))

async def setup(client: commands.Bot):
    await client.add_cog(on_private_channel_update(client))
