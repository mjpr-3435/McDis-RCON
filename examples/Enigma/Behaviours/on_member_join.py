import discord
from discord.ext import commands

class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(1328523808763805728)
        if channel:
            allowed_mentions = discord.AllowedMentions(users=False)
            await channel.send(
                f'¡Hi {member.mention}, welcome to Enigma, enjoy.',
                allowed_mentions=allowed_mentions
            )

        role = member.guild.get_role(1330258855870988429)
        if role:
            try:
                await member.add_roles(role)
            except Exception as e:
                pass


async def setup(client: commands.Bot):
    await client.add_cog(OnMemberJoin(client))