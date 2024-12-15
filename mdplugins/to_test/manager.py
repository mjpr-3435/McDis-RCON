import os

from mcdis_rcon.classes import Server

class mdplugin():
    def __init__(self, server: Server):
        self.server = server

    async def on_player_command(self, player: str, message: str):
        if not player in self.server.admins:
            return
        
        elif self.server.is_command(message, 'help'):
            self.server.show_command(player, f"pm help", "Muestra los comandos del processes manager.")

        elif self.server.is_command(message, 'pm help'):
            self.server.show_command(player, f"status", "Muestra el estado de los procesos.")
            self.server.show_command(player, f"start <process>", "Abrir el proceso.")
            self.server.show_command(player, f"stop <process | default : {self.server.name}>", "Detener el proceso.")
            self.server.show_command(player, f"restart <process | default : {self.server.name}>", "Reiniciar el proceso.")
            self.server.show_command(player, f"mdreload <process | default : {self.server.name}>", "Recargar los mdplugins del proceso.")

        elif self.server.is_command(message, 'status'):
            msgs = []
            for process in self.server.client.processes:
                msgs.append(f'[{process.name}]: {"Abierto" if process.is_running() else "Cerrado"}')

            self.server.send_response(player, msgs)

        elif self.server.is_command(message, 'start'):
            arg = message.removeprefix(self.server.prefix + 'start').strip().lower()
            
            if not arg:
                self.server.send_response(player, "✖ Debes proveer un argumento.")
            else:
                if arg in [ x.name.lower() for x in self.server.client.processes]:
                    process = next(filter(lambda x: arg == x.name.lower(), self.server.client.processes), None)

                    if process.is_running():
                        self.server.send_response(player, f"✖ El proceso ya estaba abierto...")
                        return
                    
                    self.server.send_response(player, f"[{process.name}] Abriendo proceso...")
                    process.start()
                else:
                    self.server.send_response(player, "✖ No hay un proceso con ese nombre.")

        elif self.server.is_command(message, 'stop'):
            arg = message.removeprefix(self.server.prefix + 'stop').strip().lower()

            if not arg:
                self.server.send_response(player, "✔ Cerrando proceso...")
                self.server.stop()
            else:
                if arg in [ x.name.lower() for x in self.server.client.processes]:
                    process = next(filter(lambda x: arg == x.name.lower(), self.server.client.processes), None)

                    if not process.is_running():
                        self.server.send_response(player, f"✖ El proceso no estaba abierto...")
                        return
                    
                    self.server.send_response(player, f"[{process.name}] Cerrando proceso...")
                    process.stop()
                else:
                    self.server.send_response(player, "✖ No hay un proceso con ese nombre.")

        elif self.server.is_command(message, 'mdreload'):
            arg = message.removeprefix(self.server.prefix + 'mdreload').strip().lower()

            if not arg:
                self.server.send_response(player, "✔ mdplugins recargados. Importados:")
                self.server.load_plugins(reload = True)
                self.server.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in self.server.plugins])
            else:
                if arg in [ x.name.lower() for x in self.server.client.processes]:
                    process = next(filter(lambda x: arg == x.name.lower(), self.server.client.processes), None)
                    
                    if not process.is_running():
                        self.server.send_response(player, f"✖ El proceso no estaba abierto...")
                        return
                    
                    self.server.send_response(player, f"[{process.name}] mdplugins recargados.")
                    process.load_plugins(reload = True)
                    process.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in self.server.plugins])
                else:
                    self.server.send_response(player, "✖ No hay un proceso con ese nombre.")

        elif self.server.is_command(message, 'restart'):
            arg = message.removeprefix(self.server.prefix + 'restart').strip().lower()

            if not arg:
                self.server.send_response(player, "✔ Reiniciando proceso...")
                await self.server.restart()
            else:
                if arg in [ x.name.lower() for x in self.server.client.processes]:
                    process = next(filter(lambda x: arg == x.name.lower(), self.server.client.processes), None)
                    if not process.is_running():
                        self.server.send_response(player, f"✖ El proceso no estaba abierto...")
                        return
                    
                    self.server.send_response(player, f"[{process.name}] Reiniciando proceso...")
                    await process.restart()
                else:
                    self.server.send_response(player, "✖ No hay un proceso con ese nombre.")