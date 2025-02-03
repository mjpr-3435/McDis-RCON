from discord.ext import commands
import discord

class send_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
        @client.tree.command(
            name            = 'send')
        
        async def send_command(interaction: discord.Interaction):
            class send_message_modal(discord.ui.Modal, title = 'Enviar mensaje'):
                message = discord.ui.TextInput(label = 'Mensaje', style = discord.TextStyle.paragraph)
                
                async def on_submit(self, interaction: discord.Interaction):
                    await interaction.channel.send(self.message)  
                    await interaction.response.send_message('✔', ephemeral = True, delete_after = 1)                
                
            await interaction.response.send_modal(send_message_modal())

async def setup(client: commands.Bot):
    await client.add_cog(send_command(client))