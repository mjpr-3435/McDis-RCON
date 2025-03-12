from ..modules import *
from ..classes import McDisClient

class on_guild_channel_create(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_guild_channel_create', (channel,))

async def setup(client: McDisClient):
    await client.add_cog(on_guild_channel_create(client))
