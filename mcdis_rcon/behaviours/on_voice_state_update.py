from ..modules import *
from ..classes import McDisClient

class on_voice_state_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        await self.client.call_addons('on_voice_state_update', (self.client, member, before, after))

async def setup(client: McDisClient):
    await client.add_cog(on_voice_state_update(client))