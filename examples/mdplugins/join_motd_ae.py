import os

from datetime import datetime

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import hover_and_run, extras

class mdplugin():
    def __init__(self, server: Server):
        self.server                     = server
        self.foundation_date            = '2021-05-12'

    async def on_player_join(self, player: str):
        self.show_motd(player)

    async def on_player_command(self, player: str, message: str):
        if self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, 'join-motd', 'Muestra el banner de entrada.')
            
        elif self.server.is_command(message, 'join-motd'):
            self.show_motd(player)

    def show_motd(self, player: str):
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
        
        join_messages = [   '{"text" : "§f§lAeternum §9§lNetwork §f"}',

                            '{"text" : "--------------------------"}',

                            extras([hover_and_run('§l[SMP] ', color = 'white', command = '/server SMP', hover = '/server SMP'),
                                    hover_and_run('§l[CMP] ', color = 'white', command = '/server CMP', hover = '/server CMP'),
                                    hover_and_run('§l[MMP] ', color = 'white', command = '/server MMP', hover = '/server MMP')], 
                                    text= 'Servers: ', color = 'white'),

                            f'{{"text" : "{active_days}"}}',

                            '{"text" : "--------------------------"}',

                            f'{{"text" : "MCDIS: !!mdhelp       MCDR: !!help", "color" : "gray"}}']
        return join_messages

    
    
