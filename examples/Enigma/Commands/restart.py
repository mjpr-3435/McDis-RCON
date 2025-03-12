import os
import sys
import discord
from discord.ext import commands

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="restart", description="Reinicia el bot.")
    async def restart(self, interaction: discord.Interaction):
        await interaction.response.send_message("Reiniciando el bot...", ephemeral=True)
        
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="Restarting..."
            ),
            status=discord.Status.dnd
        )
        
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(Restart(bot))
