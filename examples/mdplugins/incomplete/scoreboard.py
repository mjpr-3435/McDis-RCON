import os
import discord
import math

from mcdis_rcon.utils import read_dat_files
from mcdis_rcon.classes import Server


class mdplugin():
    def __init__(self, server: Server):
        self.server = server

    async def on_discord_message(self, message: discord.Message):
        if message.author.bot: return
        elif message.content.lower().strip() == '!!digs':
            await message.channel.send(embed = self.digs_embed())

    def format_value(self, value : int):
        magnitude = [ '', '🥝', '🍈', ]
        if not int(value/1000): i = 0
        elif not int(value/1000**2): i = 1
        else: i = 2

        return f'{f"{value/1000**i:.2f}":>8} {magnitude[i]}'

    def digs_embed(self):
        path = os.path.join(self.server.path_files, 'server', 'world', 'data', 'scoreboard.dat')
        data = read_dat_files(path)

        scores = []
        total = 0 
        n = 30

        for x in data['data']['PlayerScores']:
            if x['Objective'] == 'dig-all': 
                score = int(x['Score'])
                scores.append({"player" : x['Name'], "score" : score})
                total += score

        scores.sort(key = lambda x: x['score'], reverse = True)

        scores.insert(0, {"player" : 'Total', "score" : total})

        show_players = ''
        show_index   = ''
        for i in range(0, min(n + 1, len(scores))): 
            show_index += f'{i if i!= 0 else "":>2}\n'
            show_players += f'{scores[i]["player"].capitalize():>16}\n'
        
        embed = discord.Embed(
            color = 0x2f3136
        ).set_footer(icon_url = 'https://i.postimg.cc/XqQx5rT5/logo.png', text = f'Aeternum digs [Top {n}]')\
        .add_field(inline = True, name = '‎ ', value = f'```\n{show_index}\n```')\
        .add_field(inline = True, name = "**Player**", value = f'```\n{show_players}\n```')\
        .add_field(inline = True, name = "**Score**", value = '```yml\n' + "\n".join([self.format_value(item['score']) for item in scores][:n + 1])  + '```')

        return embed    
    
    