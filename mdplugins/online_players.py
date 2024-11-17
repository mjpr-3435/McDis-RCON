from mcdis_rcon.bot.classes import Server
from mcdis_rcon.utils import hover, extras

async def on_player_message(self: Server, player: str, message: str):
    if self.is_command(message, 'help'):
        self.show_command(player, 
                          "online", 
                          "Muestra los jugadores en los servidores.")
        
    elif self.is_command(message, 'online'):
        msgs = []
        for server in self.servers:
            if hasattr(server, 'online_players') and hasattr(server, 'bots'):
                players = ", ".join(server.online_players + server.bots)
                msgs.append(hover(f'[{server.name}] ', color = 'gray', hoover = players))

        self.execute(f'tellraw {player} {extras(msgs, text = "Jugadores: ")}')