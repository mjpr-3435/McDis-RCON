from discord.ext import commands

class OnMemberRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1328518237167685753)
        if channel:
            await channel.send(f'{member.mention} has left the server.')

async def setup(client: commands.Bot):
    await client.add_cog(OnMemberRemove(client))