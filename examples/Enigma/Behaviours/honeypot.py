import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

class Honeypot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.honeypot_channel_id = 1328768828242530355
        self.notification_channel_id = 1328518237167685753

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id == self.honeypot_channel_id:
            try:
                time_limit = datetime.now(timezone.utc) - timedelta(days=1)

                def is_recent(msg):
                    return msg.author == message.author and msg.created_at > time_limit

                deleted_messages = await message.channel.purge(limit=100, check=is_recent)

                await message.author.ban(reason="Write in the honeypot channel")

                notification_channel = self.bot.get_channel(self.notification_channel_id)
                if notification_channel:
                    await notification_channel.send(
                        f"{message.author.mention} was banned by the honeypot."
                    )
            except Exception as e:
                print(f"Error al manejar la informacion {message.author}: {e}")


async def setup(client: commands.Bot):
    await client.add_cog(Honeypot(client))
