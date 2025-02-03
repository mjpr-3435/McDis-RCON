# McDis-RCON

McDis-RCON is a Python application that allows you to relay the console of a Minecraft server to Discord, facilitating remote and efficient management through a Discord bot.

## ✨ Features

- **Support for English and Spanish**
- **Process Control**: Easily start, stop, restart, and terminate servers.
- **Console Relay**: View and interact with the server console directly from Discord.
- **Backup System**: Automatically creates backups for added security.
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
pip install mcdis_rcon
```

## ⚙️ Configuration

After installing **McDis-RCON**, run the following command in the folder where you want to store your server files:

```sh
mcdis init
```

This will create the `md_config.yml` file, which allows you to configure the settings. After that, use:

```sh
mcdis run
```

In this repository, inside the **`examples/my_setup`** folder, you'll find an example of how I have McDis-RCON set up for my personal use.

Within this folder, the files inside **`.mdaddons`** or **`*/.mdplugins`** do not have content. However, in **`examples/mdplugins`**, you'll find the latest version of the plugins I use. As for the **mdplugin**: **`events`**, which adds an event system based on the console output, you can modify or create your own based on your needs.

📌 **Coming Soon**: I will publish a more comprehensive documentation and also integrate the full guide in McDis's panel.

## 🚧 Known Issues

McDis-RCON has been tested over several months on six servers. Although it is stable, there are a few known minor issues:

- In very rare cases, one of the consoles may freeze. This issue has only been reported on one of the six servers and occurs very infrequently. I am currently investigating the cause to resolve it.
- Occasionally, the `ruamel.yaml` module may fail to install properly.

If you experience issues with `ruamel.yaml`, you can try reinstalling it with the following command:

```sh
# On Linux
python3 -m pip install --force-reinstall ruamel.yaml

# On Windows
python -m pip install --force-reinstall ruamel.yaml
```

This usually fixes the problem in most cases.

McDis-RCON is still under development, but its main features are already well implemented.

## 🤝 Collaboration

McDis-RCON is a project I developed autodidactically, without formal programming studies. Despite this, it has proven to be a useful tool for many people, so I decided to publish it and continue improving it over time.

If you'd like to contribute by adding new features, optimizing the code, or collaborating in any other way, I'd be happy to receive your help.

Join my Discord server:
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/xB9N38HBJY)

You can also contact me directly on Discord: **kassiulo**