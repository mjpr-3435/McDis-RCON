import json
import os

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import json_to_dict, dict_to_json

async def on_player_command(server: Server, player: str, message: str):
    if not player in server.admins:
        return
    
    elif server.is_command(message, 'help'):
        server.show_command(player, f"pm help", "Muestra los comandos del processes manager.")

    elif server.is_command(message, 'pm help'):
        server.show_command(player, f"status", "Muestra el estado de los procesos.")
        server.show_command(player, f"start <process>", "Abrir el proceso.")
        server.show_command(player, f"stop <process | default : {server.name}>", "Detener el proceso.")
        server.show_command(player, f"restart <process | default : {server.name}>", "Reiniciar el proceso.")
        server.show_command(player, f"mdreload <process | default : {server.name}>", "Recargar los mdplugins del proceso.")

    elif server.is_command(message, 'status'):
        msgs = []
        for process in server.client.processes:
            msgs.append(f'[{process.name}]: {"Abierto" if process.is_running() else "Cerrado"}')

        server.send_response(player, msgs)

    elif server.is_command(message, 'start'):
        arg = message.removeprefix(server.prefix + 'start').strip().lower()
        
        if not arg:
            server.send_response(player, "✖ Debes proveer un argumento.")
        else:
            if arg in [ x.name.lower() for x in server.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), server.client.processes), None)

                if process.is_running():
                    server.send_response(player, f"✖ El proceso ya estaba abierto...")
                    return
                
                server.send_response(player, f"[{process.name}] Abriendo proceso...")
                process.start()
            else:
                server.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif server.is_command(message, 'stop'):
        arg = message.removeprefix(server.prefix + 'stop').strip().lower()

        if not arg:
            server.send_response(player, "✔ Cerrando proceso...")
            server.stop()
        else:
            if arg in [ x.name.lower() for x in server.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), server.client.processes), None)

                if not process.is_running():
                    server.send_response(player, f"✖ El proceso no estaba abierto...")
                    return
                
                server.send_response(player, f"[{process.name}] Cerrando proceso...")
                process.stop()
            else:
                server.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif server.is_command(message, 'mdreload'):
        arg = message.removeprefix(server.prefix + 'mdreload').strip().lower()

        if not arg:
            server.send_response(player, "✔ mdplugins recargados. Importados:")
            server.load_plugins(reload = True)
            server.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in server.plugins])
        else:
            if arg in [ x.name.lower() for x in server.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), server.client.processes), None)
                
                if not process.is_running():
                    server.send_response(player, f"✖ El proceso no estaba abierto...")
                    return
                
                server.send_response(player, f"[{process.name}] mdplugins recargados.")
                process.load_plugins(reload = True)
                process.send_response(player, [f'   • {os.path.basename(str(x.__file__))}' for x in server.plugins])
            else:
                server.send_response(player, "✖ No hay un proceso con ese nombre.")

    elif server.is_command(message, 'restart'):
        arg = message.removeprefix(server.prefix + 'restart').strip().lower()

        if not arg:
            server.send_response(player, "✔ Reiniciando proceso...")
            await server.restart()
        else:
            if arg in [ x.name.lower() for x in server.client.processes]:
                process = next(filter(lambda x: arg == x.name.lower(), server.client.processes), None)
                if not process.is_running():
                    server.send_response(player, f"✖ El proceso no estaba abierto...")
                    return
                
                server.send_response(player, f"[{process.name}] Reiniciando proceso...")
                await process.restart()
            else:
                server.send_response(player, "✖ No hay un proceso con ese nombre.")