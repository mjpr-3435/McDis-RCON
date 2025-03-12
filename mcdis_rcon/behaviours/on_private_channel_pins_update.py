from ..modules import *
from ..classes import McDisClient

class on_private_channel_pins_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()

    async def on_private_channel_pins_update(self, channel: discord.abc.GuildChannel, last_pin: datetime):
        await self.client.call_mdextras('on_private_channel_pins_update', (channel, last_pin))

async def setup(client: McDisClient):
    await client.add_cog(on_private_channel_pins_update(client))
