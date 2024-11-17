from ..modules import *
from ..classes import McDisClient

class on_automod_rule_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_automod_rule_update(self, rule: discord.AutoModRule):
        await self.client.call_addons('on_automod_rule_update', (self.client, rule))
    
async def setup(client: McDisClient):
    await client.add_cog(on_automod_rule_update(client))
