

from darklai import Darklai
from plugins import commandcore
import platform
import os
import dirs


bot = Darklai(dirs.get_directory(), dirs.pVar)
commands = commandcore.Commands(bot, dirs.get_directory(), dirs.pVar).populate()
bot.run('')
