# McDis-RCON
[![Python Versions](https://img.shields.io/pypi/pyversions/mcdis_rcon.svg?maxAge=3600)](https://pypi.org/project/mcdis_rcon)
[![PyPI Version](https://img.shields.io/pypi/v/mcdis_rcon.svg)](https://pypi.org/project/mcdis_rcon)
[![License](https://img.shields.io/github/license/mjpr-3435/McDis-RCON.svg)](https://github.com/mjpr-3435/McDis-RCON/blob/master/LICENSE)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![English](https://img.shields.io/badge/Guide-English-blue)](GUIDE.en.md)
[![Español](https://img.shields.io/badge/README-Español-brightgreen)](README.es.md)
[![Español](https://img.shields.io/badge/Guía-Español-brightgreen)](GUIDE.es.md)

McDis-RCON is a Python application that allows you to relay the console of a Minecraft server to Discord, facilitating remote and efficient management through a Discord bot.

## ✨ Features

- **Support for English and Spanish**
- **Process Control**: Easily start, stop, restart, and terminate servers.
- **Console Relay**: View and interact with the server console directly from Discord.
- **Backup system**: Allows you to create backups of the process files.
- **File Explorer**: Manage server files with basic integrated operations.
- **Process Manager**: Monitor and manage processes within McDis's execution folder.
- **Plugin Support**: Run specific plugins for active processes.
- **Addon System**: Extend bot functionality without requiring an active process.
- **Predefined Commands**: Execute custom commands in the console whenever needed.
- **Advanced Error Reporting**: Program errors are automatically detected and notified on Discord, simplifying monitoring and resolution.
- **Multiple Launcher Compatibility**: Works with Fabric, Paper, Vanilla, and more (any Java process).
- **Does not modify the Minecraft server**: McDis-RCON runs processes with `Popen`, similar to **MCDReforged**.
- **Event System**: Unlike **MCDReforged**, McDis-RCON does not have an event system by default. However, this can be added via a plugin.
- **Compatible with MCDReforged**.

### 📌 Configuration Example
McDis-RCON can manage multiple servers simultaneously. Example with three servers (`smp`, `cmp`, `mmp`) and a network (`velocity`).

![McDis-RCON Panel](https://i.imgur.com/lE4GRIV.png)

## 🚀 Installation

To install **McDis-RCON**, simply run the following command:

```sh
pip install mcdis-rcon
```

## ⚙️ User Guide

[![English](https://img.shields.io/badge/Guide-English-blue)](GUIDE.en.md)
[![Español](https://img.shields.io/badge/Guía-Español-brightgreen)](GUIDE.es.md)

After installing **McDis-RCON**, run the following command in the folder where you want to store your server files:

```sh
mcdis init
```

This will create the `md_config.yml` file, which allows you to configure the settings. After that, use:

```sh
mcdis run
```

In the following repositories, you can see how McDis-RCON is configured in EnigmaTech SMP and Aeternum SMP.
- [AeternumBot](https://github.com/mjpr-3435/AeternumBot)
- EnigmaBot (Coming Soon)

📌 **Coming Soon**: I will publish a more comprehensive documentation and also integrate the full guide in McDis's panel.

## 🚧 Known Issues

McDis-RCON has been tested over several months on six servers. Although it is stable, there are a few known minor issues:

- In very rare cases, one of the consoles may freeze. This issue has only been reported on one of the six servers and occurs very infrequently. I am currently investigating the cause to resolve it.
- Occasionally, the `ruamel.yaml` module may fail to install properly.

If you experience issues with `ruamel.yaml`, you can try reinstalling it with the following command:

```sh
# On Linux
python3 -m pip install --force ruamel.yaml

# On Windows
python -m pip install --force ruamel.yaml
```

This usually fixes the problem in most cases.

## 🤝 Collaboration

McDis-RCON is a project I developed autodidactically, without formal programming studies. Despite this, it has proven to be a useful tool for many people, so I decided to publish it and continue improving it over time.

If you'd like to contribute by adding new features, optimizing the code, or collaborating in any other way, I'd be happy to receive your help.

Join my Discord server:
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/xB9N38HBJY)

You can also contact me directly on Discord: **kassiulo**