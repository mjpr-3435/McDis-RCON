from discord.app_commands import describe, choices, check, Choice, AppCommandThread, AppCommandChannel
from discord.ext import commands
from translate_shell.translate import translate
import discord

class translate_to_chinese(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        @client.tree.context_menu(name = 'Translate to Chinese')
        async def translate_to_chinese(interaction: discord.Interaction, message: discord.Message):
            await interaction.response.defer(ephemeral = True)
            
            if message.content != '':
                translation = translate(message.content, "zh").results[0].paraphrase
                emb_translation = discord.Embed(colour = discord.Colour(0x2f3136), description = f'{message.author.mention}: {translation}')
                await interaction.followup.send(embed = emb_translation)
            else:
                await interaction.followup.send('✖ 没有什么可翻译的.')

async def setup(client: commands.Bot):
    await client.add_cog(translate_to_chinese(client))