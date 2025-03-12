import discord
import asyncio
import sys
import os

from mcdis_rcon.classes import McDisClient

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client
        
        asyncio.create_task(self.load())

    async def load(self):
        sys.path.insert(0, self.client.path_addons)

        ### Commands, ContextMenus, Behaviours ###

        cogs = ['Commands', 'ContextMenus', 'Behaviours']

        for cog in cogs:
            cog_path = os.path.join(self.client.path_addons, cog)
            os.makedirs(cog_path, exist_ok = True)
            scripts = [file.removesuffix('.py') for file in os.listdir(cog_path) if file.endswith('.py')]

            for script in scripts:
                extension = f"{cog}.{script}"
    
                if extension in self.client.extensions:
                    await self.client.unload_extension(extension)
                
                await self.client.load_extension(extension)
        
        await self.client.tree.sync()


        ### Banners ###
        
        from Banners.Applications.creator import applications_creator
        from Banners.DiscordFriends.creator import friends_creator
        from Banners.Honeypot.creator import honey_creator
        from Banners.MemberInfo.creator import members_creator
        from Banners.ServerInfo.creator import server_creator

        await applications_creator(self.client)
        await friends_creator(self.client)
        await honey_creator(self.client)
        await members_creator(self.client)
        await server_creator(self.client)
        

        ### Status ###
        
        initial_status = discord.Activity(
            type = discord.ActivityType.playing,
            name = "Managing Enigma"
        )
        
        await self.client.change_presence(
            activity=initial_status,
            status=discord.Status.online
        )


        sys.path.pop(0)