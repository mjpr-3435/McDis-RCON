# McDis-RCON
![McDis-RCON Banner]()

McDis-RCON es una aplicación basada en python diseñada para transmitir la consola de Minecraft a Discord, permitiendo la administración de servidores de forma remota y eficiente mediante un bot de Discord.

## Características

- Abrir, cerrar, reiniciar o killear procesos.
- Retransmisión de la consola a discord, puedes interactuar con ellas desde discord
- Sistema de backups implementado.
- Navegador de archivos implementado. Este te permite
    - Crear carpetas
    - Borrar archivos
    - Hacer comprimidos y descomprimir zips
    - Cambiar nombres
    - Editar archivos de texto (Ideal para cambios en el server.properties por ejemplo)
    - Copiar archivos
    - Mover archivos
    - Descargar archivos o subirlos.
    
    En el caso de la descarga y subida de archivos, la subida se ve limitada por discord, pues funcionan subiendo los archivos a un canal y el programa los descarga en el dedicado; en el caso de la descarga, por defecto también está limitado por discord, sin embargo también hay implementada una opción para poder descargar archivos grandes, pero tienes que abrir un puerto específico.

- Administrador de procesos dentro de la carpeta donde se ejecuta McDis.
- Sistema de plugins para los procesos, dependen de que esté abierto el proceso.
- Sistema de addons para el bot de discord, estos no dependen de que haya un proceso abierto.
- Sistema de comandos predefinidos para ser ejecutados en la consola cuando gustes.
- Reporte de errores personalizado, hay un hilo encargado de trackear los errores de McDis.
- Compatibilidad con multiples launchers (fabric, paper, vanilla, etc...), basta con que sea un proceso en java.
- Compatibilidad con MCDReforged.
- McDis-RCON **NO** modifica el servidor de minecraft, los procesos se abren con Popen, así como lo hace MCDR.

    Ejemplo configurado con 3 servidores: smp, cmp, mmp y una network: velocity.

![McDis-RCON Panel](https://i.imgur.com/0049CAU.png)

## How to use it

    Ejemplo configurado con 3 servidores: smp, cmp, mmp y una network: velocity.

## Collaboration

If you would like to collaborate with me on adding new features to this repositorie, improving the code, or contributing in any other way, feel free to leave me a message.

This is my personal Discord server:  
[Join my Discord server](https://discord.gg/xB9N38HBJY)

You can also reach me directly on Discord: **kassiulo**

## Colaboración

Si deseas colaborar conmigo en añadir nuevas funcionalidades a este repositorio, mejorar el código o contribuir de cualquier otra forma, no dudes en dejarme un mensaje.

Este es mi servidor personal de Discord:  
[Únete a mi servidor de Discord](https://discord.gg/xB9N38HBJY)

También puedes contactarme directamente en Discord: **kassiulo**
