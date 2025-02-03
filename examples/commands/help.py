from discord.app_commands import describe, choices, check, Choice, AppCommandThread, AppCommandChannel
from discord.ext import commands
import discord

class create_transcription_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
        @client.tree.command(
            name            = 'help')

        async def help_command(interaction: discord.Interaction):
            await interaction.response.send_message(embed = embed(client), ephemeral = True)

async def setup(client: commands.Bot):
    await client.add_cog(create_transcription_command(client))

def embed(client: commands.Bot) -> discord.Embed:
    emoji_github                = '<:github:1220915589086707753>'
    emoji_discord               = '<:discord:1220915587669164182>'
    emoji_discord_py            = '<:DiscordPy:1226382985255850126>'
    emoji_emoji_list            = '📮'

    link_developer_portal       = 'https://discord.com/developers/applications'
    link_emoji_list             = 'https://es.piliapp.com/emoji/list/'
    link_ds_py_api              = 'https://discordpy.readthedocs.io/en/stable/api.html'
    link_ds_py_interactions_api = 'https://discordpy.readthedocs.io/en/stable/interactions/api.html'
    link_discord_markdown       = 'https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51'
    link_github                 = 'https://github.com'
    link_default_thumbnail      = 'https://i.postimg.cc/XqQx5rT5/logo.png'

    commands = '\n'.join([f'/{command.name}' for command in client.tree.get_commands(type = discord.AppCommandType.chat_input)])
    descriptions = '\n'.join([f'{command.description}' for command in client.tree.get_commands(type = discord.AppCommandType.chat_input)])

    embed = discord.Embed(
            title = f'> {client.user.display_name}',
            colour = 0x2f3136,
            description = 
            f'')\
        .add_field(name =            '', inline =  True, value = 
            f'{emoji_discord} DeveloperPortal\n'
            f'{emoji_github} Github\n'
            f'{emoji_github} Discord Markdown\n'
            f'{emoji_discord_py} Discord.py API\n'
            f'{emoji_discord_py} Discord.py Interactions API\n'
            f'{emoji_emoji_list} Emoji List\n')\
        .add_field(name =            '', inline =  True, value = 
            f'[[Developer Portal]]({link_developer_portal})\n'
            f'[[GitHub Link]]({link_github})\n'
            f'[[Markdown Link]]({link_discord_markdown})\n'
            f'[[Discord.py API]]({link_ds_py_api})\n'
            f'[[Discord.py Interactions API]]({link_ds_py_interactions_api})\n'
            f'[[Emoji List Link]]({link_emoji_list})\n')\
        .add_field(name =            '', inline =  False, value = '')\
        .add_field(name =     'Comando', inline =  True, value = commands)\
        .add_field(name = 'Descripción', inline =  True, value = descriptions)\
        .set_thumbnail(url = link_default_thumbnail)
    
    commands = '\n'.join([f'{command.name}' for command in client.tree.get_commands(type = discord.AppCommandType.message)])
   
    embed.add_field(name = 'Menus contextuales', inline =  False, value = commands)

    return embed