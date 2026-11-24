# McDis-RCON

> [!WARNING]
> **Este proyecto ya no se encuentra en mantenimiento.**
>
> **McDis-RCON** ha sido reemplazado por [**DisManager**](https://github.com/mjpr-3435/DisManager), su evolución y sucesor activo para administrar procesos y retransmitir sus consolas a través de Discord.
>
> - **GitHub:** https://github.com/mjpr-3435/DisManager
> - **PyPI:** https://pypi.org/project/dismanager/ (`pip install dismanager`)

[![Python Versions](https://img.shields.io/pypi/pyversions/mcdis_rcon.svg?maxAge=3600)](https://pypi.org/project/mcdis_rcon)
[![PyPI Version](https://img.shields.io/pypi/v/mcdis_rcon.svg)](https://pypi.org/project/mcdis_rcon)
[![License](https://img.shields.io/github/license/mjpr-3435/McDis-RCON.svg)](https://github.com/mjpr-3435/McDis-RCON/blob/master/LICENSE)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![English](https://img.shields.io/badge/Guide-English-blue)](GUIDE.en.md)
[![Español](https://img.shields.io/badge/README-Español-brightgreen)](README.es.md)
[![Español](https://img.shields.io/badge/Guía-Español-brightgreen)](GUIDE.es.md)

McDis-RCON es una aplicación escrita en Python que permite retransmitir la consola de un servidor de Minecraft a Discord, facilitando su administración de manera remota y eficiente a través de un bot de Discord.  

## ✨ Características  

- **Soporte para inglés y español**
- **Control de procesos**: Inicia, detiene, reinicia y finaliza servidores con facilidad.  
- **Retransmisión de la consola**: Visualiza e interactúa con la consola del servidor directamente desde Discord.  
- **Historial reciente de consola**: Recupera los últimos logs desde Discord o desde la API de cada proceso.
- **Sistema de backups**: Permite crear copias de seguridad de los archivos de los procesos.
- **Explorador de archivos**: Gestiona archivos del servidor con operaciones básicas integradas.  
- **Gestor de procesos**: Supervisa y administra procesos dentro de la carpeta de ejecución de McDis.  
- **Soporte para plugins**: Ejecuta plugins específicos para los procesos en ejecución.  
- **Sistema de addons**: Amplía las funcionalidades del bot sin depender de un proceso activo.  
- **Comandos predefinidos**: Ejecuta comandos personalizados en la consola cuando los necesites.
- **Reporte de errores avanzado**: Los errores del programa son detectados y notificados automáticamente en Discord, facilitando su monitoreo y resolución.  
- **Compatibilidad con múltiples launchers**: Funciona con Fabric, Paper, Vanilla y más (cualquier proceso en Java). 
- **No modifica el servidor de Minecraft**: McDis-RCON ejecuta procesos con `Popen`, de manera similar a **MCDReforged**.  
- **Hooks de ciclo de vida**: Addons y plugins pueden reaccionar al inicio, parada o fallo de procesos y a la carga o descarga de extensiones.
- **Compatible con MCDReforged**.  


### 📌 Ejemplo de configuración
McDis-RCON puede administrar múltiples servidores simultáneamente. Ejemplo con tres servidores (`smp`, `cmp`, `mmp`) y una network (`velocity`).  

![McDis-RCON Panel](https://i.imgur.com/lE4GRIV.png)


## 🚀 Cómo instalar  

Para instalar **McDis-RCON**, simplemente ejecuta el siguiente comando:  

```sh
pip install mcdis-rcon
```


## ⚙️ Guía de uso

[![English](https://img.shields.io/badge/Guide-English-blue)](GUIDE.en.md)
[![Español](https://img.shields.io/badge/Guía-Español-brightgreen)](GUIDE.es.md)

Después de instalar **McDis-RCON**, ejecuta el siguiente comando en la carpeta donde vayas a tener los archivos de tu servidor:  

```sh
mcdis init
```

Esto creará el archivo md_config.yml con el cual podrás establecer la configuración. Hecho eso utiliza 

```sh
mcdis run
```

En los siguientes repositorios se muestra cómo tienen configurado McDis-RCON: EnigmaTech SMP y Aeternum SMP.
- [AeternumBot](https://github.com/mjpr-3435/AeternumBot)
- EnigmaBot (Próximamente)

📌 **Próximamente**: Publicaré una documentación más completa y también integraré la guía completa en el panel de McDis.  

## 🚧 Problemas conocidos  

McDis-RCON ha sido probado durante varios meses en seis servidores. Aunque es estable, existen algunos problemas menores conocidos:  

- En casos muy raros, una de las consolas puede congelarse. Este problema solo se ha reportado en uno de los seis servidores y ocurre de forma muy poco frecuente. Actualmente, estoy investigando la causa para solucionarlo.  
- En algunas ocasiones, el módulo `ruamel.yaml` puede no instalarse correctamente.  

Si experimentas problemas con `ruamel.yaml`, puedes intentar reinstalarlo con el siguiente comando:  

```sh
# En Linux
python3 -m pip install --force ruamel.yaml

# En Windows
python -m pip install --force ruamel.yaml
```

Esto suele solucionar el problema en la mayoría de los casos.  

## 🤝 Colaboración  

McDis-RCON es un proyecto que he desarrollado de forma autodidacta, sin estudios formales en programación. A pesar de ello, ha resultado ser una herramienta útil para muchas personas, por lo que he decidido publicarlo y seguir mejorándolo con el tiempo.  

Si te gustaría contribuir agregando nuevas funciones, optimizando el código o colaborando de cualquier otra manera, estaré encantado de recibir tu ayuda.  

Únete a mi servidor de Discord:  
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/xB9N38HBJY)  

También puedes contactarme directamente en Discord: **kassiulo**
