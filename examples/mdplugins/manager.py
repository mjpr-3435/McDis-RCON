import psutil

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import hover, extras, hover

class mdplugin():
    def __init__(self, server: Server):
        self.server = server

    async def on_player_command(self, player: str, message: str):

        if self.server.is_command(message, 'online'):
            msgs = []
            for server in self.server.client.servers:
                if hasattr(server, 'online_players') and hasattr(server, 'bots'):
                    players = ", ".join(server.online_players + server.bots)
                    msgs.append(hover(f'[{server.name}] ', color = 'gray', hover = players))

            self.server.execute(f'tellraw {player} {extras(msgs, text = "Jugadores: ")}')

        if not player in self.server.admins:
            return
        
        elif self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, f"pm help", "Muestra los comandos del processes manager.")

        elif self.server.is_command(message, 'pm help'):
            self.server.show_command(player, f"online", "Muestra los jugadores en los servidores.")
            self.server.show_command(player, f"status", "Muestra el estado de los procesos.")
            self.server.show_command(player, f"start <process>", "Abrir el proceso.")
            self.server.show_command(player, f"stop <process | default : {self.server.name}>", "Detener el proceso.")
            self.server.show_command(player, f"restart <process | default : {self.server.name}>", "Reiniciar el proceso.")
            self.server.show_command(player, f"mdreload <process | default : {self.server.name}>", "Recargar los mdplugins del proceso.")

        elif self.server.is_command(message, 'status'):
            cpu_info = psutil.cpu_freq(), psutil.cpu_percent(interval=1)
            cpu_freq = f'{int(cpu_info[0].current)} MHz'
            cpu_load = f'{cpu_info[1]} %'

            ram_info = psutil.virtual_memory()
            ram_total = f'{ram_info.total / (1024 ** 3):.1f}'
            ram_used = f'{ram_info.used / (1024 ** 3):.1f}'
            ram_load = f'{ram_info.percent:.1f} %'

            disk_info = psutil.disk_usage("/")
            disk_total = f'{disk_info.total / (1024 ** 3):.1f}'
            disk_used = f'{disk_info.used / (1024 ** 3):.1f}'
            disk_load = f'{disk_info.percent:.1f} %'

            hover_hardware = [
                hover('§8[CPU] ', hover = f'Freq: {cpu_freq} | Load: {cpu_load}'),
                hover('§8[RAM] ', hover = f'Usage: {ram_used}/{ram_total} GB | Load: {ram_load}'),
                hover('§8[DISK] ', hover = f'Usage: {disk_used}/{disk_total} GB | Load: {disk_load}')]
            

            hover_servers = []
            for process in self.server.client.processes:
                hover_servers.append(
                    hover(f'{"§f" if process.is_running() else "§8"} [{process.name}]', 
                    hover = 'Abierto' if process.is_running() else 'Cerrado'))

            join_messages = [
                extras(hover_hardware, text = 'Recursos: ', color = 'gray'),
                '{"text" : "--------------------------"}',
                extras(hover_servers, text = 'Servers: ', color = 'gray')]

            for message in join_messages:
                message = message.replace('\n','')
                self.server.execute(f'tellraw {player} {message}')

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
                self.server.send_response(player, [f'   • {x}' for x in self.server.plugins])
            else:
                if arg in [ x.name.lower() for x in self.server.client.processes]:
                    process = next(filter(lambda x: arg == x.name.lower(), self.server.client.processes), None)
                    
                    if not process.is_running():
                        self.server.send_response(player, f"✖ El proceso no estaba abierto...")
                        return
                    
                    self.server.send_response(player, f"[{process.name}] mdplugins recargados.")
                    process.load_plugins(reload = True)
                    process.send_response(player, [f'   • {x}' for x in self.server.plugins])
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