import asyncio
import re

from mcdis_rcon.classes import Server

class mdplugin():
    def __init__(self, server: Server):
        self.server = server
        self.target = ''

    async def on_player_command(self, player: str, message: str):
        
        if self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, 'mk help', 'Muestra los comandos del marker')

        elif self.server.is_command(message, 'mk help'):
            self.server.show_command(player, 'mk pos1', 'Establece la posición 1.')
            self.server.show_command(player, 'mk pos2', 'Establece la posición 2.')

        elif self.server.is_command(message, 'mk pos1'):
            self.target = player
            self.server.execute(f'data get entity {player}')

        elif self.server.is_command(message, 'mk pos2'):
            self.target = player
            self.server.execute(f'data get entity {player}')


    async def listener_events(self, log : str):

        if not 'INFO]:' in log: 
            pass

        elif f'{self.target} has the following entity data' in log and self.target:
            match = re.search(r"has the following entity data: (.*)", log)
            data = match.group(1)
            raw_pos = data[data.find('Pos:'):]
            raw_pos = raw_pos[raw_pos.find('[') + 1 : raw_pos.find(']')].split(',')
            raw_dim = data[data.find('Dimension:'):]
            dim     = raw_dim[raw_dim.find('"') + 1 : raw_dim.find(',')-1].split(':')[1]
            
            x = int(float(raw_pos[0].strip()[:-1])) if float(raw_pos[0].strip()[:-1]) >= 0 else int(float(raw_pos[0].strip()[:-1]) - 1)
            y = int(float(raw_pos[1].strip()[:-1]))
            z = int(float(raw_pos[2].strip()[:-1])) if float(raw_pos[2].strip()[:-1]) >= 0 else int(float(raw_pos[2].strip()[:-1]) - 1)

            nbt = f'{{BlockState:{{Name:"minecraft:gray_stained_glass"}}, Glowing:1b, Invisible:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Time:1,DropItem:0b,HurtEntities:0b, Tags:["{self.target}p1"]}}'

            self.server.execute(f'summon minecraft:falling_block {x} {y} {z} {nbt}')
            await asyncio.sleep(10)
            self.server.execute(f'kill @e[tag={self.target}p1]')

            self.target = ''