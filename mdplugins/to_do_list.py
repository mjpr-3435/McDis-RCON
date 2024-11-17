import discord
import json
import os

from mcdis_rcon.bot.classes import Server

channel_id = 0

async def load(self : Server):
    global channel_id

    path_file = os.path.join(self.path_plugins_config, 'to_do_list.json')
    dictionary = {'Channel ID' : 0}
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
        
    channel_id = config['Channel ID']

    if not isinstance(self.client.get_channel(channel_id), discord.ForumChannel):
        self.add_log('Error en la configuración del plugin To Do List. El canal debe ser un foro.')
        channel_id = 0

async def on_player_command(self : Server, player: str, message: str):
    if self.is_command(message, 'help'):
        self.show_command(player, "to do list", "Solicita tu lista de tareas personales.")
        self.show_command(player, "add task <tarea>", "Añade una tarea.")
        self.show_command(player, "del task <index>", "Elimina la tarea de índice <index>.")
        return
    
    channel = self.client.get_channel(channel_id)
    if channel == None: return

    to_do_list = next(filter(lambda x: x.name == player, channel.threads), None)
    if to_do_list == None:
        to_do_list == await channel.create_thread(name = player)

    tasks = [task async for task in to_do_list.history(limit = None, oldest_first = True)]

    if self.is_command(message, 'to do list'):
        self.send_response(player, f'To do list ({player}):')

        for i in range(1, len(tasks)):
            self.send_response(player, f'{i} • {tasks[i].content.capitalize()}')
    
    elif self.is_command(message, 'add task'):
        new_task = message.replace(f'{self.prefix}add task','').strip()

        if new_task != '':
            await to_do_list.send(new_task)
            self.send_response(player, '✔ Tarea añadida.')
            tasks = [task async for task in to_do_list.history(limit = None, oldest_first = True)]
            
            self.send_response(player, f'To do list ({player}):')

            for i in range(1, len(tasks)):
                self.send_response(player, f'{i} • {tasks[i].content.capitalize()}')
        else:
            self.send_response(player, '✖ No enviaste nada para añadir.')
    
    elif self.is_command(message, 'del task'):
        
        try: 
            index_task = int(message.replace(f'{self.prefix}del task','').strip())
            if index_task < 0: raise(Exception)

        except: self.send_response(player, '✖ El indice no existe.')

        await tasks[index_task].delete()

        self.send_response(player, '✔ Tarea eliminada.')
        tasks = [task async for task in to_do_list.history(limit = None, oldest_first = True)]

        self.send_response(player, f'To do list ({player}):')

        for i in range(1, len(tasks)):
            self.send_response(player, f'{i} • {tasks[i].content.capitalize()}')
    