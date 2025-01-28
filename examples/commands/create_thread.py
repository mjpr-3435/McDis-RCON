from discord.app_commands import describe, choices, check, Choice, AppCommandThread, AppCommandChannel
from discord.ext import commands
import discord

class create_thread_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
        @client.tree.command(
            name            = 'create_thread',
            description     = 'Crea un hilo en el canal',
            extras          = {'rank' : 3})

        @describe(name          = 'Nombre del hilo')
        @describe(public        = 'Si el hilo será público')
        @choices (public        = [Choice(name = 'True', value = 1)])

        async def create_thread_command(interaction: discord.Interaction, name : str, public: int = 0):
            if not isAdmin(interaction.user):
                await interaction.response.send_message('✖ No tienes permisos.', ephemeral = True, delete_after = 1)
                return
            
            if not public:
                await interaction.channel.create_thread(name = name.strip(), auto_archive_duration = 60)

            else:
                message = await interaction.channel.send(f'Hilo público creado.')
                await interaction.channel.create_thread(name = name.strip(), message = message, auto_archive_duration = 60)
                await message.delete()
            
            await interaction.response.send_message('✔', ephemeral = True, delete_after = 1)

async def setup(client: commands.Bot):
    await client.add_cog(create_thread_command(client))


def isAdmin(member: discord.Member) -> bool:
    return member.guild_permissions.administrator