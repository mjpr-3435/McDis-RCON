# McDis-RCON  

McDis-RCON es una aplicación escrita en Python que permite retransmitir la consola de un servidor de Minecraft a Discord, facilitando su administración de manera remota y eficiente a través de un bot de Discord.  

## ✨ Características  

- **Soporte para inglés y español**
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
- **No modifica el servidor de Minecraft**: McDis-RCON ejecuta procesos con `Popen`, de manera similar a **MCDReforged**.  
- **Sistema de eventos**: A diferencia de **MCDReforged**, McDis-RCON no incluye un sistema de eventos por defecto. Sin embargo, este puede ser añadido por medio de un plugin. 
- **Compatible con MCDReforgedeforged**.  


### 📌 Ejemplo de configuración  
McDis-RCON puede administrar múltiples servidores simultáneamente. Ejemplo con tres servidores (`smp`, `cmp`, `mmp`) y una network (`velocity`).  

![McDis-RCON Panel](https://i.imgur.com/lE4GRIV.png)


## 🚀 Cómo instalar  

Para instalar **McDis-RCON**, simplemente ejecuta el siguiente comando:  

```sh
pip install mcdis_rcon
```


## ⚙️ Cómo configurar  

Después de instalar **McDis-RCON**, ejecuta el siguiente comando en la carpeta donde vayas a tener los archivos de tu servidor:  

```sh
mcdis init
```

Esto creará el archivo md_config.yml con el cual podrás establecer la configuración. Hecho eso utiliza 

```sh
mcdis run
```

En este repositorio, dentro de la carpeta **`examples/my_setup`**, se encuentra un ejemplo de cómo tengo configurado **McDis-RCON** para mi uso personal.  

Dentro de esta carpeta, los archivos dentro de **`.mdaddons`**  o **`*/.mdplugins`** no tienen contenido. Sin embargo, en **`examples/mdplugins`** encontrarás la última versión de los plugins que utilizo. En cuanto al **mdplugin**: **`events`**, que añade un sistema de eventos basado en la salida de la consola, puedes modificarlo o crear el tuyo según tus necesidades. 

📌 **Próximamente**: Publicaré una documentación más completa y también integraré la guía completa en el panel de McDis.  

## 🚧 Problemas conocidos  

McDis-RCON ha sido probado durante varios meses en seis servidores. Aunque es estable, existen algunos problemas menores conocidos:  

- En casos muy raros, una de las consolas puede congelarse. Este problema solo se ha reportado en uno de los seis servidores y ocurre de forma muy poco frecuente. Actualmente, estoy investigando la causa para solucionarlo.  
- En algunas ocasiones, el módulo `ruamel.yaml` puede no instalarse correctamente.  

Si experimentas problemas con `ruamel.yaml`, puedes intentar reinstalarlo con el siguiente comando:  

```sh
# En Linux
python3 -m pip install --force-reinstall ruamel.yaml

# En Windows
python -m pip install --force-reinstall ruamel.yaml
```

Esto suele solucionar el problema en la mayoría de los casos.  

McDis-RCON sigue en desarrollo, pero sus funcionalidades principales ya están bien implementadas.  

## 🤝 Colaboración  

McDis-RCON es un proyecto que he desarrollado de forma autodidacta, sin estudios formales en programación. A pesar de ello, ha resultado ser una herramienta útil para muchas personas, por lo que he decidido publicarlo y seguir mejorándolo con el tiempo.  

Si te gustaría contribuir agregando nuevas funciones, optimizando el código o colaborando de cualquier otra manera, estaré encantado de recibir tu ayuda.  

Únete a mi servidor de Discord:  
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/xB9N38HBJY)  

También puedes contactarme directamente en Discord: **kassiulo**  