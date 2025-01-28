from discord.ext import commands
import discord

class edit_message(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        @client.tree.context_menu(name = 'Edit Message')
        async def edit_message(interaction: discord.Interaction, message: discord.Message):            
            default = message.content

            class edit_message_modal(discord.ui.Modal, title = 'Editar mensaje'):
                new_message = discord.ui.TextInput(label = 'Mensaje', style = discord.TextStyle.paragraph, default = default)
                
                async def on_submit(self, interaction: discord.Interaction):    
                    await message.edit(content = self.new_message)
                    await interaction.response.send_message('✔', ephemeral = True, delete_after = 1)   
            await interaction.response.send_modal(edit_message_modal())

async def setup(client: commands.Bot):
    await client.add_cog(edit_message(client))