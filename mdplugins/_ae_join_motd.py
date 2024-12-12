import json
import os

from datetime import datetime
from mcdis_rcon.classes import Server
from mcdis_rcon.utils import json_to_dict, dict_to_json
foundation_date = ''

async def load(server: Server):
    global foundation_date

    path_file = os.path.join(server.path_plugins_configs, 'join_motd.json')
    dict = {
        'Foundation Date' : '0-0-0'
        }
    
    if not os.path.exists(path_file):
        dict_to_json(path_file, dict)
        
    config = json_to_dict(path_file)

    foundation_date = config['Foundation Date']

async def on_player_join(server: Server, player: str):
    join_messages = join_message()

    for message in join_messages:
        message = message.replace('\n','')
        server.execute(f'tellraw {player} {message}')

async def on_player_command(server: Server, player: str, message: str):
    
    if server.is_command(message, 'help'):
        server.show_command(player, "join-motd", "Muestra el banner de entrada.")
        
    elif server.is_command(message, 'join-motd'):
        join_messages = join_message()

        for message in join_messages:
            message = message.replace('\n','')
            server.execute(f'tellraw {player} {message}')

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
