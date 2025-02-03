# McDis-RCON  

McDis-RCON is a Python-based application that allows you to stream a Minecraft server console to Discord, enabling remote and efficient server management through a Discord bot.  

## ✨ Features  

- **Support for English and Spanish**  
- **Process control**: Start, stop, restart, and terminate servers with ease.  
- **Console streaming**: View and interact with the server console directly from Discord.  
- **Backup system**: Automatically create backups for increased security.  
- **File explorer**: Manage server files with built-in basic operations.  
- **Process manager**: Monitor and manage processes within the McDis execution folder.  
- **Plugin support**: Run plugins for active processes.  
- **Addon system**: Extend bot functionality without depending on an active process.  
- **Predefined commands**: Execute custom commands in the console whenever needed.  
- **Advanced error reporting**: Program errors are detected and automatically reported on Discord, making monitoring and troubleshooting easier.  
- **Compatibility with multiple launchers**: Works with Fabric, Paper, Vanilla, and more (any Java-based process).  
- **Does not modify the Minecraft server**: McDis-RCON runs processes using `Popen`, similar to MCDR.  
- **Compatible with MCDReforged**.  

### 📌 Configuration example  
McDis-RCON can manage multiple servers simultaneously. Example with three servers (`smp`, `cmp`, `mmp`) and a network (`velocity`).  

![McDis-RCON Panel](https://i.imgur.com/lE4GRIV.png)

## 🚧 Known Issues  

McDis-RCON has been tested for several months on six servers. Although it is stable, there are some minor known issues:  

- In very rare cases, one of the consoles may freeze. This issue has only been reported on one of the six servers and occurs very infrequently. I am currently working on identifying the cause and resolving it.  
- Occasionally, the `ruamel.yaml` module does not install correctly.  

McDis-RCON is still in development, but its core features are already well implemented.  

## 🤝 Collaboration  

If you would like to contribute to this repository by adding new features, improving the code, or helping in any other way, feel free to contact me.  

Join my Discord server:  
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/xB9N38HBJY)  

You can also reach me directly on Discord: **kassiulo**  
