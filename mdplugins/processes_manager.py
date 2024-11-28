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
    
    elif self.is_command(message, 'help'):
        self.show_command(player, f"pm help", "Muestra los comandos del processes manager.")

    elif self.is_command(message, 'pm help'):
        self.show_command(player, f"status", "Muestra el estado de los procesos.")
        self.show_command(player, f"start <process>", "Abrir el proceso.")
        self.show_command(player, f"stop <process | default : {self.name}>", "Detener el proceso.")
        self.show_command(player, f"restart <process | default : {self.name}>", "Reiniciar el proceso.")
        self.show_command(player, f"mdreload <process | default : {self.name}>", "Recargar los mdplugins del proceso.")

    elif self.is_command(message, 'status'):
        msgs = []
        for process in self.client.processes:
            msgs.append(f'[{process.name}]: {"Abierto" if process.is_running() else "Cerrado"}')

        self.send_response(player, msgs)

    elif self.is_command(message, 'start'):
        arg = message.removeprefix(self.prefix + 'start').strip().lower()
        
        if not arg:
            self.send_response(player, "✖ Debes proveer un argumento.")
        else:
            if arg in [ x.name.lower() for x in self.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), self.client.processes), None)

                if process.is_running():
                    self.send_response(player, f"✖ El proceso ya estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] Abriendo proceso...")
                process.start()
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif self.is_command(message, 'stop'):
        arg = message.removeprefix(self.prefix + 'stop').strip().lower()

        if not arg:
            self.send_response(player, "✔ Cerrando proceso...")
            self.stop()
        else:
            if arg in [ x.name.lower() for x in self.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), self.client.processes), None)

                if not process.is_running():
                    self.send_response(player, f"✖ El proceso no estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] Cerrando proceso...")
                process.stop()
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif self.is_command(message, 'mdreload'):
        arg = message.removeprefix(self.prefix + 'mdreload').strip().lower()

        if not arg:
            self.send_response(player, "✔ mdplugins recargados. Importados:")
            self.load_plugins(reload = True)
            self.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in self.plugins])
        else:
            if arg in [ x.name.lower() for x in self.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), self.client.processes), None)
                
                if not process.is_running():
                    self.send_response(player, f"✖ El proceso no estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] mdplugins recargados.")
                process.load_plugins(reload = True)
                process.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in self.plugins])
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif self.is_command(message, 'restart'):
        arg = message.removeprefix(self.prefix + 'restart').strip().lower()

        if not arg:
            self.send_response(player, "✔ Reiniciando proceso...")
            await self.restart()
        else:
            if arg in [ x.name.lower() for x in self.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), self.client.processes), None)
                if not process.is_running():
                    self.send_response(player, f"✖ El proceso no estaba abierto...")
                    return
                
                self.send_response(player, f"[{process.name}] Reiniciando proceso...")
                await process.restart()
            else:
                self.send_response(player, "✖ No hay un proceso con ese nombre.")