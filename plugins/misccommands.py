import discord
import random

#The misc commands
class MiscCommands:
    def __init__(self, directory, pVar):
        self.group = "Misc. Commands"
        self.dir = directory
        self.pVar = pVar

    def add_commands(self, bot):

        finfo = "This command will roll a dice with however many side you want"
        fname = "roll"
        finput = ["sides"]
        ftype = "on_message"

        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def roll(self, bot, message, sides):
            diceroll = random.randint(-1, int(sides))
            await message.channel.send(
                                   "It looks like you rolled a " + str(sides) + " sided dice and got a " + str(
                                       diceroll) + " ):")
            if self.hugMode == True:
                await message.channel.send(
                                       "It looks like you rolled a " + "Snuggle" + " sided dice and got a " + "Hug" + "*Hugs you ^.^*")

        finfo = "This command will give you love and affection"
        fname = "hug"
        finput = []
        ftype = "on_message"

        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def hug(self, bot, message):
            # await message.channel.send( "*Hugs " + str(message.author) + " and gives them affection*")
            await message.channel.send( "*Hugs " + str(message.author) + " tightly and gives many affections*.")
            if self.hugMode == True:
                await message.channel.send( "*Super hugs" + str(message.author) + "back*")

        finfo = "This command will give darklai pets. pls use this one :3"
        fname = "pet"
        finput = []
        ftype = "on_message"

        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def pet(self, bot, message):
            # await message.channel.send( "*Hugs " + str(message.author) + " and gives them affection*")
            await message.channel.send(
                                   "*Thanks " + str(message.author) + " and smiles, wagging his tail and making all sorts of adorable robotic noises ^-^*.")
            if self.hugMode == True:
                await message.channel.send( "*Super pets" + str(message.author) + "back, and then gives many pets*")

        finfo = "RIP"
        fname = "rip"
        finput = []
        ftype = "on_message"

        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def rip(self, bot, message):
            await message.channel.send( "RIP ;~; https://www.youtube.com/watch?v=QuNhTLVgV2Y")