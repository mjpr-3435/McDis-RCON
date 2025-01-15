from mcdis_rcon.classes import Server
from mcdis_rcon.utils import hover, extras

class mdplugin():
    def __init__(self, server: Server):
        self.server = server

    async def on_player_message(self, player: str, message: str):
        if self.server.is_command(message, 'help'):
            self.server.show_command(player, 
                            "online", 
                            "Muestra los jugadores en los servidores.")
            
        elif self.server.is_command(message, 'online'):
            msgs = []
            for server in self.server.client.servers:
                if hasattr(server, 'online_players') and hasattr(server, 'bots'):
                    players = ", ".join(self.server.online_players + self.server.bots)
                    msgs.append(hover(f'[{self.server.name}] ', color = 'gray', hover = players))

            self.server.execute(f'tellraw {player} {extras(msgs, text = "Jugadores: ")}')