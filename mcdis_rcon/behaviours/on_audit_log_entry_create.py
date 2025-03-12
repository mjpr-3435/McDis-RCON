from ..modules import *
from ..classes import McDisClient

class on_audit_log_entry_create(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        await self.client.call_mdextras('on_audit_log_entry_create', (entry,))

async def setup(client: McDisClient):
    await client.add_cog(on_audit_log_entry_create(client))