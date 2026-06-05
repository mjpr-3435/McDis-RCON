import discord

from ..modules import *

InteractionCallback = Callable[[discord.Interaction[Any]], object]


def isAdmin(member: discord.Member) -> bool:
    return member.guild_permissions.administrator


async def thread(
    name: str, channel: discord.TextChannel, *, public: bool = False
) -> discord.Thread:
    async for archived_thread in channel.archived_threads():
        await archived_thread.edit(archived=False)

    existing_thread = next(filter(lambda x: x.name == name, channel.threads), None)

    if existing_thread:
        return existing_thread

    if not public:
        new_thread = await channel.create_thread(name=name.strip())
        return new_thread

    else:
        message = await channel.send('_')
        public_thread = await channel.create_thread(name=name.strip(), message=message)
        await message.delete()
        return public_thread


async def confirmation_request(
    description: str,
    *,
    on_confirmation: InteractionCallback | None = None,
    on_reject: InteractionCallback | None = None,
    interaction: discord.Interaction[Any] | None = None,
    channel: discord.TextChannel | None = None,
    ephemeral: bool = True,
) -> None:

    class confirmation_views(discord.ui.View):
        def __init__(self) -> None:
            super().__init__(timeout=None)

        @discord.ui.button(label='✔', style=discord.ButtonStyle.gray)
        async def proceed_button(
            self, interaction: discord.Interaction[Any], button: discord.ui.Button[Any]
        ) -> None:
            if not on_confirmation:
                await interaction.response.edit_message(delete_after=0)
                return

            if inspect.iscoroutinefunction(on_confirmation):
                await on_confirmation(interaction)
            else:
                on_confirmation(interaction)

        @discord.ui.button(label='✖', style=discord.ButtonStyle.red)
        async def reject_button(
            self, interaction: discord.Interaction[Any], button: discord.ui.Button[Any]
        ) -> None:
            if not on_reject:
                await interaction.response.edit_message(delete_after=0)
                return

            if inspect.iscoroutinefunction(on_reject):
                await on_reject(interaction)
            else:
                on_reject(interaction)

    if interaction:
        await interaction.response.send_message(
            embed=discord.Embed(description=description, colour=embed_colour),
            view=confirmation_views(),
            ephemeral=ephemeral,
        )

    elif channel:
        await channel.send(
            embed=discord.Embed(description=description, colour=embed_colour),
            view=confirmation_views(),
        )
