# McDis-RCON  

McDis-RCON es una aplicación escrita en Python que permite retransmitir la consola de un servidor de Minecraft a Discord, facilitando su administración de manera remota y eficiente a través de un bot de Discord.  

## ✨ Características  

- **Control de procesos**: Inicia, detiene, reinicia y finaliza servidores con facilidad.  
- **Retransmisión de la consola**: Visualiza e interactúa con la consola del servidor directamente desde Discord.  
- **Sistema de backups**: Realiza copias de seguridad automáticas para mayor seguridad.  
- **Explorador de archivos**: Gestiona archivos del servidor con operaciones básicas integradas.  
- **Gestor de procesos**: Supervisa y administra procesos dentro de la carpeta de ejecución de McDis.  
- **Soporte para plugins**: Ejecuta plugins específicos para los procesos en ejecución.  
- **Sistema de addons**: Amplía las funcionalidades del bot sin depender de un proceso activo.  
- **Comandos predefinidos**: Ejecuta comandos personalizados en la consola cuando los necesites.
- **Reporte de errores avanzado**: Los errores del programa son detectados y notificados automáticamente en Discord, facilitando su monitoreo y resolución.  
- **Compatibilidad con múltiples launchers**: Funciona con Fabric, Paper, Vanilla y más (cualquier proceso en Java). 
- **No modifica el servidor de Minecraft**: McDis-RCON ejecuta procesos con `Popen`, similar a MCDR.   
- **Compatible con MCDReforged**.  

### 📌 Ejemplo de configuración  
McDis-RCON puede administrar múltiples servidores simultáneamente. Ejemplo con tres servidores (`smp`, `cmp`, `mmp`) y una network (`velocity`).  

![McDis-RCON Panel](https://i.imgur.com/lE4GRIV.png)

## 🚧 Problemas conocidos  

McDis-RCON ha sido probado durante varios meses en seis servidores. Aunque es estable, existen algunos problemas menores conocidos:  

- En casos muy raros, una de las consolas puede congelarse. Este problema solo se ha reportado en uno de los seis servidores y ocurre de forma muy poco frecuente. Actualmente, estoy trabajando en identificar la causa y solucionar el error.  
- En algunas ocasiones, el módulo `ruamel.yaml` no se instala correctamente.  

McDis-RCON sigue en desarrollo, pero sus funcionalidades principales ya están bien implementadas.  

## 🤝 Colaboración  

Si te gustaría colaborar en este repositorio agregando nuevas funciones, mejorando el código o contribuyendo de cualquier otra forma, no dudes en contactarme.  

Únete a mi servidor de Discord:  
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/xB9N38HBJY)  

También puedes contactarme directamente en Discord: **kassiulo**  
