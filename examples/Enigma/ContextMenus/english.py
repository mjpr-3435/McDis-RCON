from discord.ext import commands
from translate_shell.translate import translate
import discord

class translate_to_english(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        @client.tree.context_menu(name = 'Translate to English')
        async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
            await interaction.response.defer(ephemeral = True)
            
            if message.content != '':
                translation = translate(message.content, "en").results[0].paraphrase
                emb_translation = discord.Embed(colour = discord.Colour(0x2f3136), description = f'{message.author.mention}: {translation}')
                await interaction.followup.send(embed = emb_translation)
            else:
                await interaction.followup.send('✖ There is nothing to translate.')

async def setup(client: commands.Bot):
    await client.add_cog(translate_to_english(client))