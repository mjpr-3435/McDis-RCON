import discord
import os

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import json_to_dict, dict_to_json

channel_id = 0

async def load(server : Server):
    global channel_id

    path_file = os.path.join(server.path_plugins_configs, 'to_do_list.json')
    dict = {'Channel ID' : 0}
    
    if not os.path.exists(path_file):
        dict_to_json(path_file, dict)
        
    config = json_to_dict(path_file)
        
    channel_id = config['Channel ID']

    if not isinstance(server.client.get_channel(channel_id), discord.ForumChannel):
        server.add_log('Error en la configuración del plugin To Do List. El canal debe ser un foro.')
        channel_id = 0

async def on_player_command(server : Server, player: str, message: str):
    if server.is_command(message, 'mdhelp'):
        server.show_command(player, "to do list", "Solicita tu lista de tareas personales.")
        server.show_command(player, "add task <tarea>", "Añade una tarea.")
        server.show_command(player, "del task <index>", "Elimina la tarea de índice <index>.")
        return
    
    channel = server.client.get_channel(channel_id)
    if channel == None: return

    to_do_list = next(filter(lambda x: x.name == player, channel.threads), None)
    if to_do_list == None:
        to_do_list == await channel.create_thread(name = player)

    tasks = [task async for task in to_do_list.history(limit = None, oldest_first = True)]

    if server.is_command(message, 'to do list'):
        server.send_response(player, f'To do list ({player}):')

        for i in range(1, len(tasks)):
            server.send_response(player, f'{i} • {tasks[i].content.capitalize()}')
    
    elif server.is_command(message, 'add task'):
        new_task = message.replace(f'{server.prefix}add task','').strip()

        if new_task != '':
            await to_do_list.send(new_task)
            server.send_response(player, '✔ Tarea añadida.')
            tasks = [task async for task in to_do_list.history(limit = None, oldest_first = True)]
            
            server.send_response(player, f'To do list ({player}):')

            for i in range(1, len(tasks)):
                server.send_response(player, f'{i} • {tasks[i].content.capitalize()}')
        else:
            server.send_response(player, '✖ No enviaste nada para añadir.')
    
    elif server.is_command(message, 'del task'):
        
        try: 
            index_task = int(message.replace(f'{server.prefix}del task','').strip())
            if index_task < 0: raise(Exception)

        except: server.send_response(player, '✖ El indice no existe.')

        await tasks[index_task].delete()

        server.send_response(player, '✔ Tarea eliminada.')
        tasks = [task async for task in to_do_list.history(limit = None, oldest_first = True)]

        server.send_response(player, f'To do list ({player}):')

        for i in range(1, len(tasks)):
            server.send_response(player, f'{i} • {tasks[i].content.capitalize()}')
    