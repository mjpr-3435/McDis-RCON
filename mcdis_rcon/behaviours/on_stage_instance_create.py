from ..modules import *
from ..classes import McDisClient

class on_stage_instance_create(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_stage_instance_create(self, stage_instance: discord.StageInstance):
        await self.client.call_addons('on_stage_instance_create', (self.client, stage_instance))

async def setup(client: commands.Bot):
    await client.add_cog(on_stage_instance_create(client))