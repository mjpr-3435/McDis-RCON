from ..modules import *
from ..classes import McDisClient

class on_app_command_completion(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_app_command_completion(self, interaction: discord.Interaction, command: Union[discord.app_commands.Command, discord.app_commands.ContextMenu]):
        await self.client.call_addons('on_app_command_completion', (interaction, command))
    
async def setup(client: McDisClient):
    await client.add_cog(on_app_command_completion(client))
