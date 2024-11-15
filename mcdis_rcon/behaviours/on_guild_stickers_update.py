from ..modules import *
from ..classes import McDisClient

class on_guild_stickers_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_guild_stickers_update(self, guild: discord.Guild, before: list[discord.GuildSticker], after: list[discord.GuildSticker]):
        await self.client.call_addons('on_guild_stickers_update', (self.client, guild, before, after))

async def setup(client: commands.Bot):
    await client.add_cog(on_guild_stickers_update(client))