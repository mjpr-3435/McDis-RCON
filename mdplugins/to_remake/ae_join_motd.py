from datetime import datetime

from mcdis_rcon.classes import Server

class mdplugin():
    def __init__(self, server: Server):
        self.foundation_date = '2021-05-12'
        self.server = server

    async def on_player_join(self, player: str):
        join_messages = self.join_message()

        for message in join_messages:
            message = message.replace('\n','')
            self.server.execute(f'tellraw {player} {message}')

    async def on_player_command(self, player: str, message: str):
        
        if self.server.is_command(message, 'help'):
            self.server.show_command(player, "join-motd", "Muestra el banner de entrada.")
            
        elif self.server.is_command(message, 'join-motd'):
            join_messages = self.join_message()

            for message in join_messages:
                message = message.replace('\n','')
                self.server.execute(f'tellraw {player} {message}')

    def join_message(self):
        years = int(((datetime.today()-datetime.strptime(self.foundation_date, "%Y-%m-%d")).days)//365.25)
        days = int((datetime.today()-datetime.strptime(self.foundation_date, "%Y-%m-%d")).days%365.25)
                
        if years == 0:
            active_days = f'Tiempo activo: {days} días'
        elif days == 0:
            active_days = f'Tiempo activo: {years} años'
        else:
            active_days = f'Tiempo activo: {years} años {days} días'
        
        join_messages = [   '{"text" : "§f§lAeternum §9§lNetwork §f:"}',
                            '{"text" : "--------------------------"}',
                            """{"text": "Servers: ",
                                "extra": [  {"text": "§l[SMP] ",
                                            "clickEvent": {"action": "run_command" , "value": "/server SMP"},
                                            "hoverEvent": {"action": "show_text"   , "value": "/server SMP"}},
                                            {"text": "§l[CMP] ",
                                            "clickEvent": {"action": "run_command",
                                                        "value": "/server CMP"},
                                            "hoverEvent": {"action": "show_text",
                                                        "value": "/server CMP"}},
                                            {"text": "§l[MMP] ",
                                            "clickEvent": {"action": "run_command",
                                                        "value": "/server MMP"},
                                            "hoverEvent": {"action": "show_text",
                                                        "value": "/server MMP"}}]}""",
                            f'{{"text" : "{active_days}"}}']
        return join_messages
