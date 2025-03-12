import discord
from discord.ext import commands
from discord.app_commands import describe, choices, Choice

class ClearCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        @client.tree.command(name="clear", description="Elimina mensajes")
        @describe(amount="Cantidad de mensajes a borrar")
        @describe(all="Si deben borrarse todos los mensajes del canal")
        @choices(all=[Choice(name="True", value=1)])
        async def clear_command(interaction: discord.Interaction, amount: int = 0, all: Choice[int] = 0):
            if not isAdmin(interaction.user):
                await interaction.response.send_message("✖ No tienes permisos para borrar mensajes.", ephemeral=True)
                return

            await interaction.response.defer(ephemeral=True, thinking=True)

            if amount != 0:
                deleted = await interaction.channel.purge(limit=amount)
                await interaction.followup.send(f"✔ {len(deleted)} mensajes borrados.", ephemeral=True, delete_after=5)

            elif all != 0:
                deleted = await interaction.channel.purge()
                await interaction.followup.send(f"✔ Todos los mensajes han sido borrados.", ephemeral=True, delete_after=5)

            else:
                await interaction.followup.send("✖ Uso incorrecto. Usa '/clear all' o '/clear <cantidad>'", ephemeral=True)

async def setup(client: commands.Bot):
    await client.add_cog(ClearCommand(client))

def isAdmin(member: discord.Member) -> bool:
    return member.guild_permissions.administrator
