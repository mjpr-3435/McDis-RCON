import json
import os

from mcdis_rcon.classes import Server
admins = []

async def load(self: Server):
    global admins

    path_file = os.path.join(self.path_plugins_config, 'processes_manager.json')
    dictionary = {
        'Admins' : []
        }
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    admins = config['Admins']

async def on_player_command(self: Server, player: str, message: str):
    global admins

    if not player in admins:
        return
    

    if self.is_command(message, 'help'):
        self.show_command(player, f"pm help", "Muestra los comandos del processes manager.")

    elif self.is_command(message, 'pm help'):
        self.show_command(player, f"status", "Muestra el estado de los procesos.")
        self.show_command(player, f"start <process>", "Abrir el proceso.")
        self.show_command(player, f"stop <process | default : {self.name}>", "Detener el proceso.")
        self.show_command(player, f"restart <process | default : {self.name}>", "Reiniciar el proceso.")
        self.show_command(player, f"reload mdplugins <process | default : {self.name}>", "Recargar los mdplugins del proceso.")

    elif self.is_command(message, 'status'):
        msgs = []
        for process in self.processes:
            msgs.append(f'[{process.name}]: {process.state()}')

        self.send_response(player, msgs)

    elif self.is_command(message, 'start'):
        arg = message.removeprefix(self.prefix + 'start').strip().lower()
        
        if not arg:
            self.send_response(player, "✖ Debes proveer un argumento.")
        else:
            if arg in [ x.name.lower() for x in self.servers]:
                process = next(filter(lambda x: arg == x.name.lower(), self.servers), None)

                if process.state() != 'Closed':
                    self.send_response(player, f"✖ El servidor ya estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] Abriendo servidor...")
                process.start()
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif self.is_command(message, 'stop'):
        arg = message.removeprefix(self.prefix + 'stop').strip().lower()

        if not arg:
            self.send_response(player, "✔ Cerrando servidor...")
            self.stop()
        else:
            if arg in [ x.name.lower() for x in self.servers]:
                process = next(filter(lambda x: arg == x.name.lower(), self.servers), None)

                if process.state() == 'Closed':
                    self.send_response(player, f"✖ El servidor no estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] Cerrando servidor...")
                process.stop()
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif self.is_command(message, 'reload mdplugins'):
        arg = message.removeprefix(self.prefix + 'reload mdplugins').strip().lower()

        if not arg:
            self.send_response(player, "✔ mdplugins recargados. Importados:")
            self.load_plugins(reload = True)
            self.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in self.plugins])
        else:
            if arg in [ x.name.lower() for x in self.servers]:
                process = next(filter(lambda x: arg == x.name.lower(), self.servers), None)
                
                if process.state() == 'Closed':
                    self.send_response(player, f"✖ El servidor no estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] mdplugins recargados.")
                process.load_plugins(reload = True)
                process.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in self.plugins])
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif self.is_command(message, 'restart'):
        arg = message.removeprefix(self.prefix + 'restart').strip().lower()

        if not arg:
            self.send_response(player, "✔ Reiniciando servidor...")
            await self.restart()
        else:
            if arg in [ x.name.lower() for x in self.servers]:
                process = next(filter(lambda x: arg == x.name.lower(), self.servers), None)
                if process.state() == 'Closed':
                    self.send_response(player, f"✖ El servidor no estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] Reiniciando servidor...")
                await process.restart()
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")