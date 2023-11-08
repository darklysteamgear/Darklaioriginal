import inspect
import logging

logs = logging.getLogger('discord')


class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""

        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class Plugin(object, metaclass=PluginMount):

    is_global = False
    fancy_name = None

    def __init__(self, darklai):
        self.darklai = darklai
        self.commands = {}
        self.bg_tasks = {}

        for name, member in inspect.getmembers(self):
            # registering commands
            if hasattr(member, '_is_command'):
                self.commands[member.__name__] = member
            # registering bg_tasks
            if hasattr(member, '_bg_task'):
                self.bg_tasks[member.__name__] = member
                self.darklai.loop.create_task(member())
        logs.info("Registered {} commands / {} bg tasks".format(
            len(self.commands),
            len(self.bg_tasks)
        ))

    async def on_ready(self):
        pass

    async def _on_message(self, message):
        if message.author.id != self.darklai.user.id:
            for command_name, func in self.commands.items():
                await func(message)
        await self.on_message(message)

    async def on_message(self, message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_message_delete(self, message):
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_guild_join(self, guild):
        pass

    async def on_guild_update(self, before, after):
        pass

    async def on_guild_role_create(self, guild, role):
        pass

    async def on_guild_role_delete(self, guild, role):
        pass

    async def on_guild_role_update(self, guild, role):
        pass

    async def on_voice_state_update(self, before, after):
        pass

    async def on_member_ban(self, member):
        pass

    async def on_member_unban(self, member):
        pass

    async def on_typing(self, channel, user, when):
        pass
