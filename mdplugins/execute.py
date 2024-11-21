import os
import ruamel.yaml
import discord
import json
import asyncio

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import extras, hover_and_suggest

config = dict()

async def load(self: Server):
    global config
    
    path_file = os.path.join(self.path_plugins_config,'execute.json')
    dictionary = {}
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

async def on_already_started(self: Server):
    global config
    
    keys = list(config.keys())

    for key in keys:
        with open(os.path.join(self.path_commands, f'{key}.yml'), "r+") as file:
            yaml = ruamel.yaml.YAML()
            yaml.indent(mapping = 2, sequence = 4, offset = 2)
            yaml.preserve_quotes = True

            data = yaml.load(file)

        commands = data[config[key]]   
        
        for command in commands:
            if 'await' in command:
                await asyncio.sleep(int(command.replace('await','').strip()))
                continue
            self.execute(command.strip())
            await asyncio.sleep(1)

async def on_player_command(self: Server, player: str, message: str):
    commands = [file.removesuffix('.yml') for file in os.listdir(self.path_commands) if file.endswith('.yml')]
    commands.sort()
    message = message.replace(' ', '').lower()

    if self.is_command(message, 'help'):
        self.show_command(player, 
                          "commands", 
                          "Lista de comandos predifinidos del servidor.")
        
    elif self.is_command(message, 'commands'):
        self.send_response(player, "Comandos disponibles:")
        for i in range(len(commands)):
            text = f'{i} • {commands[i]}'
            
            with open(os.path.join(self.path_commands, f'{commands[i]}.yml'), "r+") as file:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping = 2, sequence = 4, offset = 2)
                yaml.preserve_quotes = True

                data = yaml.load(file)
                keys = list(data.keys())
            
            placeholder = 'Acciones: ' + ', '.join(keys[1:])
            ext = extras([hover_and_suggest(text, suggest = self.prefix + commands[i] + ' ', hoover = placeholder)])
            self.execute(f'tellraw {player} {ext}')

    elif any(message.startswith(self.prefix + command.replace(' ', '').lower()) for command in commands):
        command = next(filter(lambda command: message.startswith(self.prefix + command.replace(' ', '').lower()), commands), None)
        action = message.removeprefix(self.prefix + command.replace(' ', '').lower())

        if not command: return
        
        with open(os.path.join(self.path_commands, f'{command}.yml'), "r+") as file:
            yaml = ruamel.yaml.YAML()
            yaml.indent(mapping = 2, sequence = 4, offset = 2)
            yaml.preserve_quotes = True

            data = yaml.load(file)
            keys = list(data.keys())

        if not action:
            messages = ["Descripción:", data[keys[0]], " ", "Acciones disponibles:"]
            self.send_response(player, messages)

            for i in range(1, len(keys)):
                commands = ', '.join(data[keys[i]])
                suggestion = self.prefix + command + ' ' + keys[i]
                ext = extras([hover_and_suggest(f'{i} • {keys[i]}', suggest =  suggestion, hoover = commands)])
                self.execute(f'tellraw {player} {ext}')
            return
        
        if action.lower().replace(' ','') in [action.lower().replace(' ','') for action in keys]:
            action = next(filter(lambda x: x.lower().replace(' ','') == action.lower().replace(' ',''), keys))
            commands = data[action]   
            self.send_response(player, 'Ejecutando comandos...')
            
            for cmd in commands:
                if 'await' in cmd:
                    await asyncio.sleep(int(cmd.replace('await','').strip()))
                    continue
                self.execute(cmd.strip())
                await asyncio.sleep(1)

            self.send_response(player, f'✔ {command}: Comandos ejecutados.')

        else:
            self.send_response(player, "✖ No hay una acción con ese nombre.")