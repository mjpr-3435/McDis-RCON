from mcdis_rcon.classes import Server
from mcdis_rcon.utils import hover, extras

async def on_player_message(server: Server, player: str, message: str):
    if server.is_command(message, 'help'):
        server.show_command(player, 
                          "online", 
                          "Muestra los jugadores en los servidores.")
        
    elif server.is_command(message, 'online'):
        msgs = []
        for server in server.client.servers:
            if hasattr(server, 'online_players') and hasattr(server, 'bots'):
                players = ", ".join(server.online_players + server.bots)
                msgs.append(hover(f'[{server.name}] ', color = 'gray', hoover = players))

        server.execute(f'tellraw {player} {extras(msgs, text = "Jugadores: ")}')