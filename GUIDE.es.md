# McDis-RCON GUIDE

## 1. Configuración de McDis-RCON

Para utilizar McDis-RCON, necesitas el token de un bot de Discord. Si aún no tienes uno, puedes seguir este tutorial para crear un bot en Discord: [[Guía oficial]](https://discordpy.readthedocs.io/en/stable/discord.html).

Es recomendable otorgarle permisos de administrador al bot para evitar problemas al generar y administrar el panel de control.


## 2. Comandos de consola

### Inicialización

```sh
mcdis init
```
Genera el archivo `md_config.yml` necesario para configurar McDis-RCON.

### Ejecución

```sh
mcdis run
```
Inicia McDis-RCON si hay un archivo `md_config.yml` válido en la carpeta de ejecución.

#### Ejemplo de salida:

```bash
Initializing McDis RCON v0.4.19a...
Your configuration has been loaded successfully.
[2025-03-13 00:01:36] [INFO    ] discord.client: logging in using static token
[2025-03-13 00:01:38] [INFO    ] discord.gateway: Shard ID None has connected to Gateway (Session ID: 8974ae0bce7cc313e57a778b817e3507).
Logged in as Just Another Bot#6873!
   • Creating objects
     -> server 1
     -> server 2
     -> network 1
   • Loaded Discord events
   • Loaded server panel
Loading Complete

Commands: start, stop, restart, kill, mdreload, adreload, status, exit
>>
```

### Manejo de procesos

Una vez abierto McDis-RCON, este gestionará la señal `Ctrl + C`, intentando detener los procesos con los comandos definidos en `stop_cmd`.  
Si un proceso tarda más de 60 segundos en cerrarse, será terminado forzosamente antes de finalizar la ejecución del programa. También puedes administrar los procesos directamente desde la consola.


## 3. Estructura de archivos

A partir de este punto, nos referiremos a la carpeta donde se ejecuta McDis-RCON como `McDis`. Dentro del programa, McDis-RCON también usa este nombre para referirse a dicha carpeta.

### Carpetas de procesos

Al inicializar McDis-RCON, se crearán carpetas específicas para cada proceso definido. Por ejemplo:

- `McDis/server 1` → Contiene todos los archivos del proceso `server 1`.
- `McDis/server 2` → Contiene todos los archivos del proceso `server 2`.
- `McDis/network 1` → Contiene todos los archivos del proceso `network 1`.

Dentro de cada carpeta de proceso, se generarán subcarpetas adicionales para comandos y plugins:

- `McDis/<process>/.mdcommands` → Almacena comandos predefinidos para `<process>`.
- `McDis/<process>/.mdplugins` → Almacena los plugins asociados a `<process>`.

### Carpetas con funciones específicas

Además, McDis-RCON generará carpetas adicionales con propósitos específicos:

- `McDis/.mdbackups` → Almacena todos los backups generados con McDis-RCON.
- `McDis/.mdaddons` → Contiene los addons adicionales utilizados por McDis-RCON.


## 4. Panel

Considerando una configuración con tres servidores (`smp`, `cmp`, `mmp`) y una red (`velocity`), el panel generado se verá así:

![McDis-RCON Panel](https://i.imgur.com/lE4GRIV.png)

### Comandos

En los hilos que actúan como consola de los procesos, se pueden usar los siguientes comandos:

- `start` → Ejecuta el comando `start_cmd` configurado en `md_config.yml`.
- `stop` → Ejecuta el comando `stop_cmd` configurado en `md_config.yml`.
- `kill` → Cierra forzosamente el proceso.
- `restart` → Ejecuta `stop_cmd` y, una vez cerrado el proceso, ejecuta `start_cmd`.
- `mdreload` → Recarga los mdplugins dentro de `.mdplugins` del proceso correspondiente.

En el canal del panel de Discord, estos comandos deben ir precedidos por `!!` y especificar el proceso o agregar `-all` para aplicarlo a todos. Ejemplo:

- `!!start SMP` → Equivalente a escribir `start` en la consola de `SMP`. (No distingue mayúsculas: `!!start smp` hará lo mismo).
- `!!start-all` → Equivalente a escribir `start` en la consola de cada proceso.

También existe el comando `!!adreload`, que permite recargar los addons de McDis-RCON.

### Botones

- **`Processes`** → Despliega controles para administrar procesos con botones.  

  ![McDis-RCON Processes Panel](https://i.imgur.com/ZYtK5nO.png)

  - `⬅️` → Regresa a la interfaz por defecto.  
  - El segundo botón permite alternar entre procesos.  
  - Los demás botones corresponden a los comandos respectivos.  


- **`Files`** → Abre el gestor de archivos (detallado en otra sección).
- **`Tools`** → Despliega herramientas adicionales (detallado en otra sección).
- **`Guide`** → Muestra la guía de McDis-RCON (aún no implementado).
- **`Restart`** → Solicita confirmación para reiniciar el programa. Antes de cerrarse, intentará detener todos los procesos con `stop_cmd`. Si tardan más de 60 segundos en cerrarse, los terminará forzosamente y procederá con el reinicio.

### Personalización

Para agregar un banner al panel, coloca una imagen en `McDis/banner.png`. Se cargará automáticamente.  

📏 **Tamaño recomendado:** 515 × 131 px  

![Panel Banner](https://i.imgur.com/SgTT90z.png)


## 5. Sistema de Plugins y Addons

McDis-RCON permite ampliar sus funcionalidades mediante dos sistemas distintos:  
- **`mdaddons`** → Se ejecutan mientras McDis-RCON esté abierto.  
- **`mdplugins`** → Dependen de que el proceso correspondiente esté en ejecución.  

## Addons (`mdaddons`)
Estos se cargan apenas McDis-RCON se conecta a la API de Discord y pueden ser recargados usando el comando `!!adreload` en el canal del panel. 

Deben colocarse dentro de la carpeta `McDis/.mdaddons`.

<details>
  <summary>Creación de addons en McDis-RCON</summary>

McDis-RCON permite dos formas de crear addons:  
1. **Archivos individuales** (`.py`).  
2. **Carpetas** con un archivo `__init__.py` en su interior.  

</details>

<details>
  <summary>Cómo carga McDis-RCON los addons</summary>  

Cuando el sistema carga o recarga los addons, busca dentro de `McDis/.mdaddons` y sigue estas reglas:  

- **Archivos `.py`**: Si contienen una clase `mdaddon`, se crea una instancia de esta clase.  
- **Carpetas**: Si contienen un archivo `__init__.py` con una clase `mdaddon`, se crea una instancia de esta clase.  

En ambos casos, al instanciar la clase, se le pasa como argumento un objeto `McDisClient` de McDis-RCON.

</details>

<details>
  <summary>Cómo interactúan los addons con eventos de Discord</summary>  

Los addons pueden reaccionar a eventos de Discord. Para ello, McDis-RCON verifica si las instancias de `mdaddon` tienen métodos con el mismo nombre que los eventos de `discord.py`. Si existe una coincidencia, el evento se enviará al addon.  

</details>

<details>
  <summary>Ejemplo: Añadir una reacción a los mensajes del panel</summary>

Si queremos que el bot reaccione a todos los mensajes en el canal del panel, podemos crear un script en:  
`McDis/.mdaddons/reactor.py`  

```python
import discord
from mcdis_rcon.classes import McDisClient

class mdaddon:
    def __init__(self, client: McDisClient):
        self.client = client

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return  # Ignorar mensajes de bots

        if message.channel.id == self.client.panel.id:
            await message.add_reaction('✅')
```

El método `on_message` sigue la misma estructura que la documentada en `discord.py`.  
[Documentación de discord.py](https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events)  
</details>

<details>
  <summary>Descarga de addons</summary>

Antes de recargar los addons, McDis-RCON verifica si los addons cargados tienen un método `unload`. Este método no recibe argumentos y permite ejecutar acciones de limpieza antes de recargar.  

```python
from mcdis_rcon.classes import McDisClient

class mdaddon:
    def __init__(self, client: McDisClient):
        self.client = client

    def unload(self):
        # Acciones antes de la descarga
        return
```

</details>

## Plugins (`mdplugins`)
Estos se cargan al inicializar el proceso y pueden ser recargados con `!!mdreload` en el canal del panel o `mdreload` en la consola del proceso. 

Deben colocarse dentro de la carpeta `McDis/<process>/.mdplugins`.

<details>
  <summary>Creación de plugins en McDis-RCON</summary>

McDis-RCON permite crear plugins como archivos individuales (`.py`).  

</details>

<details>
  <summary>Cómo carga McDis-RCON los plugins</summary>

Cuando el proceso carga o recarga los plugins, busca dentro de `McDis/<process>/.mdplugins` y sigue estas reglas:

- **Archivos `.py`**: Si contienen una clase `mdplugin`, se crea una instancia de esta clase.  

Al instanciar la clase, se le pasa como argumento un objeto `Server` o `Network` de McDis-RCON.

</details>

<details>
  <summary>Cómo interactúan los plugins con eventos de Discord</summary>

Los plugins pueden reaccionar a eventos de Discord. Para ello, McDis-RCON verifica si las instancias de `mdplugin` tienen métodos con el nombre de los eventos de `discord.py`, pero con el prefijo `listener_`. Si existe una coincidencia, el evento se enviará al plugin.  

</details>

<details>
  <summary>Cómo interactúan los plugins con los logs de la consola</summary>  

Cada vez que McDis-RCON procesa un log de la consola, verifica si los plugins tienen un método `listener_events` que reciba el log como argumento (una cadena de texto). Si este método está definido, el log se enviará al plugin, permitiendo así la creación de un sistema de eventos basado en la salida del servidor.

</details>

<details>
  <summary>Ejemplo: Añadir una reacción a los mensajes del panel cuando el proceso SMP está abierto</summary>

Si queremos que el bot reaccione a todos los mensajes en el canal del panel cuando el proceso SMP esté abierto, podemos crear un script en:  
`McDis/SMP/.mdplugins/reactor.py`  

```python
import discord
from mcdis_rcon.classes import Server

class mdplugin:
    def __init__(self, server: Server):
        self.server = server

    async def listener_on_message(self, message: discord.Message):
        if message.author.bot:
            return  # Ignorar mensajes de bots

        if message.channel.id == self.server.client.panel.id:
            await message.add_reaction('✅')
```

El método `listener_on_message` sigue la misma estructura que la documentada en `discord.py`, salvo que el nombre del evento incluye el prefijo `listener_`.  
[Documentación de discord.py](https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events)  

</details>

<details>
  <summary>Ejemplo: Detectar jugadores que se conectan mediante logs</summary>

Si queremos que un plugin detecte cuando un jugador se conecta, podemos analizar los logs del servidor. Suponiendo que los mensajes de conexión tienen el formato `Player <nombre> joined the game`, podemos escribir un plugin en:  
`McDis/SMP/.mdplugins/player_tracker.py`

```python
from mcdis_rcon.classes import Server

class mdplugin:
    def __init__(self, server: Server):
        self.server = server

    def listener_events(self, log: str):
        if "joined the game" in log:
            player_name = log.split(" ")[1]  # Extraer el nombre del jugador
            print(f"El jugador {player_name} se ha conectado.")
```

</details>


<details>
  <summary>Descarga de plugins</summary>

Antes de recargar los plugins, McDis-RCON verifica si los plugins cargados tienen un método `unload`. Este método no recibe argumentos y permite ejecutar acciones de limpieza antes de recargar.  

```python
from mcdis_rcon.classes import Server

class mdplugin:
    def __init__(self, server: Server):
        self.server = server

    def unload(self):
        # Acciones antes de la descarga
        return
```

</details>

## Ejemplos Avanzados y Personalización  
Por defecto, los addons solo interactúan con los eventos de Discord, y los plugins con los eventos de Discord y los logs de la consola del proceso.

Sin embargo, en servidores como Aeternum y Enigma, mediante el uso de addons, se ha implementado un sistema de eventos más avanzado. Esto permite la integración de comandos en Minecraft y la detección de diversas acciones dentro del juego, ampliando las posibilidades de automatización y personalización en la gestión del servidor.

Para más detalles sobre estas implementaciones, consulta:
- [AeternumBot](https://github.com/mjpr-3435/AeternumBot)  
- EnigmaBot (Próximamente)  


## 6. Gestor de archivos

McDis-RCON incluye un gestor de archivos que permite navegar dentro de `McDis`. Al presionar el botón `Files` en el panel, se desplegará una interfaz como esta:  

![File Manager](https://i.imgur.com/PcJ5afz.png)  

### Controles de la Interfaz  

- **`⬅️`** → Regresa a la carpeta anterior.  
- **`🔄`** → Recarga la interfaz.  
- **`📌`** → Permite ingresar una ruta específica.  
- **`Terminal`** → Permite realizar operaciones avanzadas de gestión de archivos.  
- **`Desplegable`** → Muestra las primeras 25 opciones de la carpeta actual y facilita la navegación. En carpetas con más de 25 archivos, es recomendable usar la terminal.  

### Archivos  

Cuando se selecciona un archivo en lugar de una carpeta, aparecen los botones `Request`, `Edit` y `Delete`:  

![Files](https://i.imgur.com/5tPw9DQ.png)

- **`⬅️`** → Regresa a la carpeta anterior.  
- **`🔄`** → Recarga la interfaz.  
- **`Request`** → Solicita el archivo para descargarlo, con un límite de 5MB debido a las restricciones de Discord. 
- **`Edit`** → Permite modificar el nombre del archivo.  
- **`Delete`** → Elimina el archivo.  

Para solicitar archivos más grandes, se puede utilizar Flask (explicado más adelante).  

### Editor de Archivos de Texto  

Si el archivo es de texto, McDis-RCON mostrará una previsualización del contenido (hasta 1024 caracteres).  

![Text Preview](https://i.imgur.com/dSeIQg7.png)  

Si el archivo tiene menos de 4000 caracteres, también se podrá editar directamente.  

![Text Edit](https://i.imgur.com/ZV1NlQx.png)  

### Comandos  

Todas las carpetas de procesos contienen una subcarpeta `.mdcommands`, donde se almacenan los comandos predefinidos en formato `.yml`. Al acceder a esta carpeta, se mostrará una interfaz como la siguiente:  

![Commands](https://i.imgur.com/5r3AMUI.png)  

- **`⬅️`** → Regresa a la carpeta anterior.  
- **`🔄`** → Recarga la interfaz.  
- **`📦`** → Muestra la interfaz de archivos.  
- **`Desplegable`** → Muestra todos los comandos definidos y permite crear nuevos.  

En servidores como Aeternum SMP, se han definido comandos específicos para automatizar tareas como el MobSwitch. Cada comando puede tener varias acciones predefinidas, como `Reset`, `Over` y `Nether`.  

![Commands MobSwitch](https://i.imgur.com/5KCcmi2.png)  

- **`⬅️`** → Regresa a la interfaz de `.mdcommands`.   
- **`🔄`** → Recarga la interfaz.
- **`Execute`** → Ejecuta el comando en la consola del proceso.  
- **`Edit`** → Abre el archivo `.yml` para editarlo.  
- **`Delete`** → Elimina el comando.  
- **`Desplegable`** → Muestra todas las acciones definidas para el comando seleccionado.  

### Backups  

Al navegar hasta `McDis/.mdbackups`, se encontrarán carpetas con los nombres de los procesos configurados. Al entrar en una de ellas, se mostrará una interfaz similar a esta:  

![Backups](https://i.imgur.com/seit7kJ.png)  

- **`⬅️`** → Regresa a la carpeta anterior.  
- **`🔄`** → Recarga la interfaz.  
- **`📦`** → Muestra la interfaz de archivos.  

Si ya hay backups creados, aparecerán en la lista. Para crear un nuevo backup, se debe seleccionar la opción correspondiente en el desplegable. McDis-RCON solicitará cerrar el proceso antes de continuar para evitar problemas.  

El sistema de backups elimina automáticamente los más antiguos según el límite definido en `md_config.yml`.  

### Terminal  
Además de la interfaz gráfica, McDis-RCON cuenta con una terminal integrada que permite realizar operaciones avanzadas dentro del gestor de archivos, tales como navegar entre carpetas, editar archivos, renombrarlos, copiarlos, moverlos, crear nuevas carpetas, borrarlos, comprimir carpetas, etc. (todo dentro de `McDis`).

![Terminal](https://i.imgur.com/xgPt5hs.png)


## 7. Herramientas  
Al presionar el botón `Tools` en el panel, se desplegarán las siguientes opciones:  

![Tools](https://i.imgur.com/S3jAKbE.png)  

### Processes  
Permite visualizar todos los procesos en ejecución dentro de la carpeta `McDis`. Si seleccionas el proceso en el desplegable, McDis-RCON lo cerrará forzosamente.

![Processes](https://i.imgur.com/72K5lBN.png)  

- **`🔄`** → Recarga la interfaz.  
- **`📌`** → Permite ingresar una ruta específica.  

### Uploader  
El Uploader permite subir archivos a través del canal del panel. Cuando está activado, cualquier archivo enviado al canal se guardará en la ruta configurada. También ofrece la opción de decidir si se deben sobrescribir archivos existentes o no.  

![Uploader](https://i.imgur.com/hL2tnDv.png)  

- **`🔄`** → Recarga la interfaz.  
- **`📌`** → Permite ingresar una ruta específica para subir los archivos.
- **`Run/Close`** → Define el estado del Uploader.
- **`Do Not Overwrite/Overwrite`** → Define si el Uploader debe o no sobrescribir.

### Flask
McDis-RCON incorpora un pequeño servidor Flask para facilitar la descarga de archivos que superan el límite de 5 MB impuesto por Discord. Para utilizar esta función, es necesario abrir un puerto para permitir el tráfico.  

Para descargar un archivo, navega hasta él y pulsa `Request`. Si `Flask: Allow` está activado en la configuración, se generará un enlace de descarga. Puedes elegir si los enlaces deben ser de un solo uso y/o temporales. La IP configurada debe ser pública, no una interna. Además, en el hilo `Console Flask` se registrará quién solicita el archivo, cuándo se usa, si expira, entre otros detalles.  

![Flask](https://i.imgur.com/G1K8gP2.png)  

- **`🔄`** → Recarga la interfaz.
- **`Run/Close`** → Define el estado del servidor Flask.
- **`Single Use/Multi-Use`** → Define si los links generados deben ser de un solo uso o multi uso.
- **`Temporary/Persistent`** → Define si los links generados deben ser temporales o persistentes.

## 8. Errores  
Si ocurre un error durante la ejecución de eventos o funciones, McDis generará automáticamente un reporte en el hilo `Error reports` del canal del panel. Además, si el error está relacionado con un proceso en ejecución, se registrará una referencia en su consola.  

![Error Reports](https://i.imgur.com/ysDyQdU.png)  
