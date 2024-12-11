"""
self._load_addons(reload = True)
msg = self._('✔ Addons reloaded.')
msg += ''.join([f'\n   • {os.path.basename(str(x.__file__))}' for x in self.addons])

response = await message.channel.send(
    self._(msg))
await response.delete(delay = 5)
"""