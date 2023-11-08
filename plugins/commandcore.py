import discord
from plugins.misccommands import MiscCommands
from plugins.modcommands import ModCommands
from plugins.misccommands import MiscCommands
from plugins.RPG.Code.rpgcommands import RPGCommands

class Commands:
    def __init__(self, bot, directory, pVar):
        self.bot = bot
        self.dir = directory
        self.pVar = pVar
        isRan = True

    def populate(self):
        misccommands = MiscCommands(self.dir, self.pVar)
        modcommands = ModCommands(self.dir, self.pVar)
        rpgcommands = RPGCommands(self.dir, self.pVar)
        misccommands.add_commands(self.bot)
        modcommands.add_commands(self.bot)
        rpgcommands.add_commands(self.bot)
        return