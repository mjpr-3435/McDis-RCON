import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class skin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mojang_api_url = "https://api.mojang.com/users/profiles/minecraft/"
        self.skin_render_url = "https://starlightskins.lunareclipse.studio/render"
        self.valid_renders = [
            "default", "marching", "walking", "crossed", "criss_cross", "ultimate", "isometric", "head",
            "relaxing", "cowering", "lunging", "pointing", "facepalm", "sleeping", "archer", "kicking",
            "mojavatar", "reading", "bitzel", "pixel"
        ]

    @app_commands.command(name="skin", description="Get the skin of a Minecraft player")
    @app_commands.describe(
        username="The name of the Minecraft player",
        render="The type of skin rendering"
    )
    @app_commands.choices(
        render=[
            app_commands.Choice(name=render, value=render) for render in [
                "default", "marching", "walking", "crossed", "criss_cross", "ultimate", "isometric", "head",
                "relaxing", "cowering", "lunging", "pointing", "facepalm", "sleeping", "archer", "kicking",
                "mojavatar", "reading", "bitzel", "pixel"
            ]
        ]
    )
    async def skin(self, interaction: discord.Interaction, username: str, render: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.mojang_api_url}{username}", timeout=10) as uuid_response:
                    if uuid_response.status != 200:
                        await interaction.response.send_message(
                            f"Player could not be found `{username}`.", ephemeral=True
                        )
                        return

                    data = await uuid_response.json()
                    uuid = data.get("id")
                    if not uuid:
                        await interaction.response.send_message(
                            f"Player's UUID not found `{username}`.", ephemeral=True
                        )
                        return

            skin_url = f"{self.skin_render_url}/{render}/{uuid}/full"

            async with aiohttp.ClientSession() as session:
                async with session.get(skin_url, timeout=10) as skin_response:
                    if skin_response.status != 200:
                        await interaction.response.send_message(
                            f"Player skin could not be obtained `{username}`. "
                            f"{await skin_response.text()}",
                            ephemeral=True
                        )
                        return

            await interaction.response.send_message(skin_url)

        except aiohttp.ClientError as e:
            await interaction.response.send_message(
                f"API Error: {str(e)}", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Error: {str(e)}", ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(skin(bot))
