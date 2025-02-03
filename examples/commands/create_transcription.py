from discord.app_commands import AppCommandThread, AppCommandChannel
from discord.ext import commands
from typing import Union
import chat_exporter
import discord
import io

class create_transcription_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
        @client.tree.command(
            name            = 'create_transcription')
        
        async def create_transcription_command(interaction: discord.Interaction, send_transcription_to : Union[AppCommandThread,AppCommandChannel]):
            
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