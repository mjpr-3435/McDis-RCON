import json
import os

from datetime import datetime
from mcdis_rcon.classes import Server
foundation_date = ''

async def load(self: Server):
    global foundation_date

    path_file = os.path.join(self.path_plugins_config, 'join_motd.json')
    dictionary = {
        'Foundation Date' : '0-0-0'
        }
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    foundation_date = config['Foundation Date']

async def on_player_join(self: Server, player: str):
    join_messages = join_message()

    for message in join_messages:
        message = message.replace('\n','')
        self.execute(f'tellraw {player} {message}')

async def on_player_command(self: Server, player: str, message: str):
    
    if self.is_command(message, 'help'):
        self.show_command(player, "join-motd", "Muestra el banner de entrada.")
        
    elif self.is_command(message, 'join-motd'):
        join_messages = join_message()

        for message in join_messages:
            message = message.replace('\n','')
            self.execute(f'tellraw {player} {message}')

def join_message():
    years = int(((datetime.today()-datetime.strptime(foundation_date, "%Y-%m-%d")).days)//365.25)
    days = int((datetime.today()-datetime.strptime(foundation_date, "%Y-%m-%d")).days%365.25)
            
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
