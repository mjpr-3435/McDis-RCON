from ..modules import *
from ..classes import *
from ..utils import *

class FlaskView             (discord.ui.View):
    def __init__(self, client: McDisClient):
        super().__init__(timeout = None)
        self.client = client

        self.add_item(UpdateButton      (self.client))
        self.add_item(StateButton       (self.client))

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

            self.label = 'Close' if self.view.client.flask.is_running else 'Run'

            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                embed = FlaskEmbed(self.view.client),
                view = self.view
            )
        else:
            async def on_confirmation(confirmation_interaction: discord.Interaction):
                await confirmation_interaction.response.edit_message(delete_after=0)
                await self.view.client.flask.stop()

                self.label = 'Close' if self.view.client.flask.is_running else 'Run'
                await confirmation_interaction.followup.edit_message(
                    message_id = interaction.message.id,
                    embed = FlaskEmbed(self.view.client),
                    view = self.view
                )

            await confirmation_request(
                self.view.client._('Are you sure you want to close Flask? Closing it while a file is being downloaded will block McDis\'s thread. '
                                    'Please ensure no files are being downloaded before proceeding.'), 
                on_confirmation = on_confirmation, 
                interaction = interaction
            )

class FlaskEmbed            (discord.Embed):
    def __init__(self, client: McDisClient):
        super().__init__(title = f'> Flask', colour=embed_colour)
        self.client = client

        self._add_description()
        self._add_status_field()

    def _add_description(self):
        self.add_field(inline = True, name = '', value=
            self.client._('Flask allows you to download files larger than 5 MB. '
                         'When you request a file, Flask generates a one-time-use link that is valid for 60 seconds.')
        )

    def _add_status_field(self):
        ip = str(self.client.config['Flask']['IP'])
        port = str(self.client.config['Flask']['Port'])
        state = 'Running' if self.client.flask.is_running else 'Closed'

        self.add_field(inline = True, name = '', value=
            f'`'
            f'• IP:                     '[:-len(ip)] + ip + '\n'
            f'• Port:                   '[:-len(port)] + port + '\n'
            f'• State:                  '[:-len(state)] + state + '\n'
            f'`'
        )
