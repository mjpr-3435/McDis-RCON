import discord
from discord.ext import commands

def isAdmin(member: discord.Member) -> bool:
    return member.guild_permissions.administrator

class SendCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(
        name='send',
        description='Haz que el bot envíe un mensaje'
    )
    async def send_command(self, interaction: discord.Interaction):
        if not isAdmin(interaction.user):
            await interaction.response.send_message('✖ No tienes permisos.', ephemeral=True, delete_after=5)
            return

        class SendMessageModal(discord.ui.Modal, title='Enviar mensaje'):
            message = discord.ui.TextInput(label='Mensaje', style=discord.TextStyle.paragraph)

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.channel.send(self.message.value)
                await interaction.response.send_message('✔ Mensaje enviado.', ephemeral=True, delete_after=5)

        await interaction.response.send_modal(SendMessageModal())

async def setup(client: commands.Bot):
    await client.add_cog(SendCommand(client))
