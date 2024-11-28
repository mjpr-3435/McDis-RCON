from ..modules import *
from ..classes import *
from ..utils import *

class FlaskView             (discord.ui.View):
    def __init__(self, client: McDisClient):
        super().__init__(timeout = None)
        self.client = client

        self.add_item(UpdateButton              (self.client))
        self.add_item(StateButton               (self.client))
        self.add_item(TemporaryLinksButton       (self.client))
        self.add_item(OneTimeLinksButton        (self.client))
        self.add_item(CleanLinksButton        (self.client))

class UpdateButton          (discord.ui.Button):
    def __init__(self, client: McDisClient):
        super().__init__(label = emoji_update, style=discord.ButtonStyle.gray)
        self.view: FlaskView

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed = FlaskEmbed(self.view.client),
            view = FlaskView(self.view.client)
        )

class StateButton           (discord.ui.Button):
    def __init__(self, client: McDisClient):
        label = 'Close' if client.flask.is_running else 'Run'
        super().__init__(label = label, style = discord.ButtonStyle.gray)
        self.view: FlaskView

    async def callback(self, interaction: discord.Interaction):
        if not self.view.client.flask.is_running:
            await interaction.response.defer()
            await self.view.client.flask.start()
            if not self.view.client.flask.is_running: return

            self.label = 'Close' if self.view.client.flask.is_running else 'Run'

            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = FlaskEmbed(self.view.client),
                view = self.view
            )
        else:
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                shutdown_link = self.view.client.flask.shutdown_link(interaction.user)

                await confirmation_interaction.response.edit_message(
                    content = f'[Click on here to stop Flask.]({shutdown_link})',
                    embed = None,
                    view = None)
                
                while self.view.client.flask.is_running:
                    await asyncio.sleep(0.5)

                self.label = 'Close' if self.view.client.flask.is_running else 'Run'
                await confirmation_interaction.followup.edit_message(
                    message_id = interaction.message.id,
                    embed = FlaskEmbed(self.view.client),
                    view = self.view
                )

                await confirmation_interaction.followup.edit_message(
                    message_id = confirmation_interaction.message.id,
                    content = '✔ Flask was succesfully closed.'
                )

            await confirmation_request(
                self.view.client._('Are you sure you want to close Flask? Closing it while a file is being downloaded will block McDis\'s thread. '
                                    'Please ensure no files are being downloaded before proceeding.'), 
                on_confirmation = on_confirmation, 
                interaction = interaction
            )

class TemporaryLinksButton   (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label =  'Temporary' if client.flask.temporary_links else 'Persistent'
        super().__init__(label = label, style=discord.ButtonStyle.gray)
        self.view: FlaskView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.flask.temporary_links = not self.view.client.flask.temporary_links

        self.label = 'Temporary' if self.view.client.flask.temporary_links else 'Persistent'
        await interaction.response.edit_message(
            embed = FlaskEmbed(self.view.client),
            view = self.view)

class OneTimeLinksButton    (discord.ui.Button):
    def __init__(self, client : McDisClient):
        label = 'Single-Use' if client.flask.one_time_links else 'Multi-Use'
        super().__init__(label = label, style=discord.ButtonStyle.gray)
        self.view: FlaskView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.flask.one_time_links = not self.view.client.flask.one_time_links

        self.label = 'Single-Use' if self.view.client.flask.one_time_links else 'Multi-Use'
        await interaction.response.edit_message(
            embed = FlaskEmbed(self.view.client),
            view = self.view)

class CleanLinksButton      (discord.ui.Button):
    def __init__(self, client : McDisClient):
        super().__init__(label = 'Clean Links', style=discord.ButtonStyle.red)
        self.view: FlaskView

    async def callback(self, interaction: discord.Interaction):
        self.view.client.flask.clean_active_links()

        await interaction.response.edit_message(
            embed = FlaskEmbed(self.view.client),
            view = self.view)

class FlaskEmbed            (discord.Embed):
    def __init__(self, client: McDisClient):
        super().__init__(title = f'> Flask', colour=embed_colour)
        self.client = client

        self._add_description()
        self._add_status_field()
        self._add_links_field()

    def _add_description(self):
        flask_console_id = next(
                filter(lambda thread: thread.name == 'Console Flask', self.client.panel.threads),
                None
            ).id
        
        self.add_field(inline = True, name = '', value=
            self.client._('Flask allows you to download files larger than 5 MB. '
                         'When you request a file, Flask generates a link that allows you to download it.')
                         + f'\n\n<#{flask_console_id}>'
        )

    def _add_status_field(self):
        ip = truncate(str(self.client.config['Flask']['IP']), 20)
        port = str(self.client.config['Flask']['Port'])
        state = 'Running' if self.client.flask.is_running else 'Closed'
        state_uses = 'Single-Use' if self.client.flask.one_time_links else 'Multi-Use'
        state_time = 'Temporary' if self.client.flask.temporary_links else 'Persistent'

        self.add_field(inline = True, name = '', value=
            '`• IP:                     '[:-len(ip)] + ip + '`\n'
            '`• Port:                   '[:-len(port)] + port + '`\n'
            '`• State:                  '[:-len(state)] + state + '`\n'
            '`• Links:                  '[:-len(state_uses)] + state_uses + '`\n'
            '`• Links:                  '[:-len(state_time)] + state_time + '`\n'
        )

    def _add_links_field(self):
        content = ''
        links = self.client.flask.active_downloads
        for id, data in links.items():
            user = data['user']
            file = truncate(data['file'], 48)
            link = f'http://{self.client.config["Flask"]["IP"]}:{self.client.config["Flask"]["Port"]}/file_request?id={id}'
            dummy = f'User :: {user}\nFile :: {file}\n{link}\n\n'
            if len(content + dummy) > 1000: break
            content += dummy

        self.add_field(inline = False, name = self.client._('**Active Links:**'), value = '' if not content else f'```asciidoc\n{content}```')
