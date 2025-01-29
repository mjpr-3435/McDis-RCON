from discord.app_commands import describe, choices, check, Choice, AppCommandThread, AppCommandChannel
from discord.ext import commands
from typing import Union
import chat_exporter
import discord
import io

class create_transcription_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
        @client.tree.command(
            name            = 'create_transcription',    
            description     = 'Transcribe un canal')

        @describe(send_transcription_to = 'Canal o hilo a donde quieres mandar la transcripción')
        
        async def create_transcription_command(interaction: discord.Interaction, send_transcription_to : Union[AppCommandThread,AppCommandChannel]):
            if not isAdmin(interaction.user):
                await interaction.response.send_message('✖ No tienes permisos.', ephemeral = True, delete_after = 1)
                return
            
            await interaction.response.defer(ephemeral = True)
            channel = await send_transcription_to.fetch() 

            transcript = await chat_exporter.export(interaction.channel)
            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename = f"transcripción-{interaction.channel.name}.html",)
            file_saved_online = await channel.send(file = transcript_file)

            file_link = await chat_exporter.link(file_saved_online)
            await channel.send(content = f'[[Click para ver la transcripción de #{interaction.channel.name}]]({file_link})')
            
            response = await interaction.followup.send('✔')
            await response.delete(delay = 1)

async def setup(client: commands.Bot):
    await client.add_cog(create_transcription_command(client))


def isAdmin(member: discord.Member) -> bool:
    return member.guild_permissions.administrator