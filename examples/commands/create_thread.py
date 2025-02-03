from discord.app_commands import describe, choices, check, Choice, AppCommandThread, AppCommandChannel
from discord.ext import commands
import discord

class create_thread_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
        @client.tree.command(
            name            = 'create_thread')
        
        @choices (public        = [Choice(name = 'True', value = 1)])

        async def create_thread_command(interaction: discord.Interaction, name : str, public: int = 0):
            if not public:
                await interaction.channel.create_thread(name = name.strip(), auto_archive_duration = 60)

            else:
                message = await interaction.channel.send(f'Hilo público creado.')
                await interaction.channel.create_thread(name = name.strip(), message = message, auto_archive_duration = 60)
                await message.delete()
            
            await interaction.response.send_message('✔', ephemeral = True, delete_after = 1)

async def setup(client: commands.Bot):
    await client.add_cog(create_thread_command(client))