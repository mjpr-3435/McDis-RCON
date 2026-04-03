from ..modules import *
from ..classes import McDisClient

class on_message(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command: Union[discord.app_commands.Command, discord.app_commands.ContextMenu]):
        await self.client.call_mdextras('on_app_command_completion', (interaction, command))
        
    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        await self.client.call_mdextras('on_audit_log_entry_create', (entry,))
        
    @commands.Cog.listener()
    async def on_automod_action(self, execution: discord.AutoModAction):
        await self.client.call_mdextras('on_automod_action', (execution,))
        
    @commands.Cog.listener()
    async def on_automod_rule_create(self, rule: discord.AutoModRule):
        await self.client.call_mdextras('on_automod_rule_create', (rule,))
        
    @commands.Cog.listener()
    async def on_automod_rule_delete(self, rule: discord.AutoModRule):
        await self.client.call_mdextras('on_automod_rule_delete', (rule,))
        
    @commands.Cog.listener()
    async def on_automod_rule_update(self, rule: discord.AutoModRule):
        await self.client.call_mdextras('on_automod_rule_update', (rule,))
        
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages : list[discord.Message]):
        await self.client.call_mdextras('on_bulk_message_delete', (messages,))
        
    @commands.Cog.listener()
    async def on_connect(self):
        await self.client.call_mdextras('on_connect')
        
    @commands.Cog.listener()
    async def on_disconnect(self):
        await self.client.call_mdextras('on_disconnect')
        
    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        await self.client.call_mdextras('on_error', (event, args, kwargs))
        
    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        await self.client.call_mdextras('on_guild_available', (guild,))
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_guild_channel_create', (channel,))
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_guild_channel_delete', (channel,))
        
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel: discord.abc.GuildChannel, last_pin: datetime):
        await self.client.call_mdextras('on_guild_channel_pins_update', (channel, last_pin))
        
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_guild_channel_update', (before, after))
        
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji]):
        await self.client.call_mdextras('on_guild_emojis_update', (guild, before, after))
        
    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild: discord.Guild):
        await self.client.call_mdextras('on_guild_integrations_update', (guild,))
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.client.call_mdextras('on_guild_join', (guild,))
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.client.call_mdextras('on_guild_remove', (guild,))
        
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        await self.client.call_mdextras('on_guild_role_create', (role,))
        
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        await self.client.call_mdextras('on_guild_role_delete', (role,))
        
    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        await self.client.call_mdextras('on_guild_role_update', (before, after))
        
    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild: discord.Guild, before: list[discord.GuildSticker], after: list[discord.GuildSticker]):
        await self.client.call_mdextras('on_guild_stickers_update', (guild, before, after))
        
    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild: discord.Guild):
        await self.client.call_mdextras('on_guild_unavailable', (guild,))
        
    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        await self.client.call_mdextras('on_guild_update', (before, after))
        
    @commands.Cog.listener()
    async def on_integration_create(self, integration: discord.Integration):
        await self.client.call_mdextras('on_integration_create', (integration,))
        
    @commands.Cog.listener()
    async def on_integration_update(self, integration: discord.Integration):
        await self.client.call_mdextras('on_integration_update', (integration,))
        
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        await self.client.call_mdextras('on_interaction', (interaction,))
        
    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        await self.client.call_mdextras('on_invite_create', (invite,))
        
    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        await self.client.call_mdextras('on_invite_delete', (invite,))
        
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        await self.client.call_mdextras('on_member_ban', (guild, user))
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.client.call_mdextras('on_member_join', (member,))
        
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.client.call_mdextras('on_member_remove', (member,))
        
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        await self.client.call_mdextras('on_member_unban', (guild, user))
        
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        await self.client.call_mdextras('on_member_update', (before, after))
        
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        await self.client.call_mdextras('on_message_delete', (message,))
        
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.client.call_mdextras('on_message_edit', (before, after))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.client.panel_interface(message)
        await self.client.upload_logic(message)
        await self.client.call_mdextras('on_message', (message,))
        
    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        await self.client.call_mdextras('on_presence_update', (before, after))
        
    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, channel: discord.abc.GuildChannel, last_pin: datetime):
        await self.client.call_mdextras('on_private_channel_pins_update', (channel, last_pin))
        
    @commands.Cog.listener()
    async def on_private_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_private_channel_update', (before, after))
        
    @commands.Cog.listener()
    async def on_raw_app_command_permissions_update(self, payload: discord.RawAppCommandPermissionsUpdateEvent):
        await self.client.call_mdextras('on_raw_app_command_permissions_update', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: discord.RawBulkMessageDeleteEvent):
        await self.client.call_mdextras('on_raw_bulk_message_delete', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_integration_delete(self, payload: discord.RawIntegrationDeleteEvent):
        await self.client.call_mdextras('on_raw_integration_delete', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        await self.client.call_mdextras('on_raw_member_remove', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        await self.client.call_mdextras('on_raw_message_edit', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await self.client.call_mdextras('on_raw_reaction_add', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_reaction_clear_emoji(self, payload: discord.RawReactionClearEmojiEvent):
        await self.client.call_mdextras('on_raw_reaction_clear_emoji', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, payload: discord.RawReactionClearEvent):
        await self.client.call_mdextras('on_raw_reaction_clear', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await self.client.call_mdextras('on_raw_reaction_remove', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_thread_delete(self, payload: discord.RawThreadDeleteEvent):
        await self.client.call_mdextras('on_raw_thread_delete', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_thread_member_remove(self, payload: discord.RawThreadMembersUpdate):
        await self.client.call_mdextras('on_raw_thread_member_remove', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_thread_update(self, payload: discord.RawThreadUpdateEvent):
        await self.client.call_mdextras('on_raw_thread_update', (payload,))
        
    @commands.Cog.listener()
    async def on_raw_typing(self, payload: discord.RawTypingEvent):
        await self.client.call_mdextras('on_raw_typing', (payload,))
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.User,discord.Member]):
        await self.client.call_mdextras('on_reaction_add', (reaction, user))
        
    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction: discord.Reaction):
        await self.client.call_mdextras('on_reaction_clear_emoji', (reaction,))
        
    @commands.Cog.listener()
    async def on_reaction_clear(self, message: discord.Message, reactions: list[discord.Reaction]):
        await self.client.call_mdextras('on_reaction_clear', (message, reactions))
        
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        await self.client.call_mdextras('on_reaction_remove', (reaction, user))
        
    @commands.Cog.listener()
    async def on_resumed(self):
        await self.client.call_mdextras('on_resumed')
        
    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        await self.client.call_mdextras('on_scheduled_event_create', (event,))
        
    @commands.Cog.listener()
    async def on_scheduled_event_delete(self, event: discord.ScheduledEvent):
        await self.client.call_mdextras('on_scheduled_event_delete', (event,))
        
    @commands.Cog.listener()
    async def on_scheduled_event_update(self, before: discord.ScheduledEvent, after:discord.ScheduledEvent):
        await self.client.call_mdextras('on_scheduled_event_update', (before, after))
        
    @commands.Cog.listener()
    async def on_scheduled_event_user_add(self, event: discord.ScheduledEvent, user: discord.User):
        await self.client.call_mdextras('on_scheduled_event_user_add', (event, user))
        
    @commands.Cog.listener()
    async def on_scheduled_event_user_remove(self, event: discord.ScheduledEvent, user: discord.User):
        await self.client.call_mdextras('on_scheduled_event_user_remove', (event, user))
        
    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id: int):
        await self.client.call_mdextras('on_shard_connect', (shard_id,))
        
    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id: int):
        await self.client.call_mdextras('on_shard_disconnect', (shard_id,))
        
    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id: int):
        await self.client.call_mdextras('on_shard_ready', (shard_id,))
        
    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id: int):
        await self.client.call_mdextras('on_shard_resumed', (shard_id,))

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type: str):
        await self.client.call_mdextras('on_socket_event_type', (event_type,))
        
    @commands.Cog.listener()
    async def on_socket_raw_receive(self, message: str):
        await self.client.call_mdextras('on_socket_raw_receive', (message,))
        
    @commands.Cog.listener()
    async def on_socket_raw_send(self, payload: Union[str,bytes]):
        await self.client.call_mdextras('on_socket_raw_send', (payload,))
        
    @commands.Cog.listener()
    async def on_stage_instance_create(self, stage_instance: discord.StageInstance):
        await self.client.call_mdextras('on_stage_instance_create', (stage_instance,))
        
    @commands.Cog.listener()
    async def on_stage_instance_delete(self, stage_instace: discord.StageInstance):
        await self.client.call_mdextras('on_stage_instance_delete', (stage_instace,))
        
    @commands.Cog.listener()
    async def on_stage_instance_update(self, before: discord.StageInstance, after: discord.StageInstance):
        await self.client.call_mdextras('on_stage_instance_update', (before, after))
        
    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        await self.client.call_mdextras('on_thread_create', (thread,))
        
    @commands.Cog.listener()
    async def on_thread_delete(self, thread: discord.Thread):
        await self.client.call_mdextras('on_thread_delete', (thread,))
        
    @commands.Cog.listener()
    async def on_thread_join(self, thread: discord.Thread):
        await self.client.call_mdextras('on_thread_join', (thread,))
        
    @commands.Cog.listener()
    async def on_thread_member_join(self, member: discord.ThreadMember):
        await self.client.call_mdextras('on_thread_member_join', (member,))
        
    @commands.Cog.listener()
    async def on_thread_member_remove(self, member: discord.ThreadMember):
        await self.client.call_mdextras('on_thread_member_remove', (member,))
        
    @commands.Cog.listener()
    async def on_thread_remove(self, thread: discord.Thread):
        await self.client.call_mdextras('on_thread_remove', (thread,))
        
    @commands.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        await self.client.call_mdextras('on_thread_update', (before, after))
        
    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        await self.client.call_mdextras('on_user_update', (before, after))
        
    @commands.Cog.listener()
    async def on_voice_server_update(self, data: dict):
        await self.client.call_mdextras('on_voice_server_update', (data,))
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        await self.client.call_mdextras('on_voice_state_update', (member, before, after))

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel):
        await self.client.call_mdextras('on_webhooks_update', (channel,))

    @commands.Cog.listener()
    async def on_typing(self, channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime):
        await self.client.call_mdextras('on_typing', (channel, user, when))

async def setup(client: McDisClient):
    await client.add_cog(on_message(client))

