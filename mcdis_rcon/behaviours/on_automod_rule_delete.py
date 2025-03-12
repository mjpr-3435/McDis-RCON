from ..modules import *
from ..classes import McDisClient

class on_automod_rule_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_automod_rule_delete(self, rule: discord.AutoModRule):
        await self.client.call_mdextras('on_automod_rule_delete', (rule,))
    
async def setup(client: McDisClient):
    await client.add_cog(on_automod_rule_delete(client))
