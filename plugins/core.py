from decorators import command

import discord
import logging
import asyncio
from plugins.ai import aicore

#The core commands for Darklai
class Core:
    def __init__(self, directory, pVar):
        self.roleList = ""
        self.bot = None
        self.message = None
        self.command = {
            "info":"null",
            "name":"null",
            "input":[],
            "type":"null",
            "func":"null",
        }
        self.commandList = {}
        self.groups = {
        }
        self.hugMode = False
        self.pVar = pVar
        self.pDir = "RPG" + pVar
        self.dir = directory + pVar +"plugins" + pVar
        print(self.dir)

    #Display information and a list of commands
    async def display_help(self,bot, message):
        self.helpString = " My name is DARKLAI... I am currently in version 0.0.3 Alpha.\n"+ "I am currently still under heavy development by Darkly SteamGear :/ \n"+ "Here's a list of some of my commands :DDD:```\n"
        for key in self.commandList.keys():
            command = self.commandList.get(key)
            commandFunc = command.get("func")
            commandInfo = command.get("info")
            commandName = command.get("name")
            commandArgs = command.get("input")
            commandType = command.get("type")

            self.helpString += str(key) + "|| input = (" + str(commandArgs) + "): " + str(commandInfo) + "\n"
        self.helpString += '``` If you are still having trouble, remember, I only read commands that start with = and inputs that start with " :/, like this :=get_role "@user "Bot :D.'
        await message.channel.send( str(self.helpString))

    def populate_command_database(self):
        for key in self.commandList.keys():
            self.command = self.commandList.get(key)
            self.commandType = self.command.get("type")


            print(str(self.command))
            

    #The command to give a user a specific role
    async def give_role(self, bot, message, member, role, isautomated = False):

        self.member = discord.Guild.get_member_named(message.guild, member)

        if self.member == None:
            member = member.split('!', 1)[-1]
            member = member.split('>', 1)
            member = member[0]
            self.member = discord.Guild.get_member(message.guild, member)

        if self.member == None:
            return

        self.role = str(role)
        print("Member " + str(self.member))
        self.serverMainRoles = message.guild.roles
        self.roleList = [discord.utils.get(self.serverMainRoles, name=self.role).id]
        self.role = discord.utils.get(self.serverMainRoles, name=self.role)
        hasReqRole = False
        hasRole = False

        #For every role in the user's roles, check for the appropriate role
        if (self.member.guild_permissions.administrator == True):
            hasReqRole = True

        if (isautomated == True):
            hasReqRole = True

        for r in self.member.roles:
            if r.id in self.roleList:
                hasRole = True

        #Check to make sure that they have the required things
        if hasReqRole == True and hasRole == False:
            try:
                await bot.add_roles(self.member, self.role)
                await message.channel.send( "I have given you the role! :D")
            except discord.Forbidden:
                await message.channel.send( "I don't have perms to add that role. :/.")

        elif hasReqRole == True and hasRole == True:
            try:
                await message.channel.send( "You Already have that role :V")
            except discord.Forbidden:
                await message.channel.send( "I don't have perms to add that role. :/.")

        elif hasReqRole == False and hasRole == True:
            try:
                await message.channel.send( "You cannot have that role!")
            except discord.Forbidden:
                await message.channel.send( "I don't have perms to add that role. :/.")
        else:
            try:
                await message.channel.send( "You cannot have that role! :LLL")
            except discord.Forbidden:
                await message.channel.send( "I don't have perms to add that role. :/.")
        return


    #Run all the on_message plugins
    async def run_on_message_plugins(self, bot, message):
            self.bot = bot
            self.message = message
            #self.rolelist = [discord.utils.get(message.guild.roles)]
            if str(message.content).find("@269304629307637761") != -1:
                self.commandIn = str(message.content).split("@269304629307637761>",1)[-1]
                self.commandIn = self.commandIn.split()
                try:
                    self.userInputTwo = self.commandIn[2]
                except Exception:
                    self.userInputTwo = "Null"
                    pass

                try:
                    self.userInput = self.commandIn[1]
                except Exception:
                    self.userInput = "Null"
                    pass
                self.commandIn = self.commandIn[0]
                print(self.commandIn)
                print(self.userInput)
                print(self.userInputTwo)
                #TODO: Create AI core
                try:
                    aiCore = aicore.AiCore()
                    await aicore.run_ai(self.string, self.member)
                except Exception:
                    await message.channel.send( "AI IS NOT READY")
            elif str(message.content).find('=') == False:
                print(message.content)
                self.commandIn = str(message.content).split("=",1)[-1]
                self.commandIn = self.commandIn.split(' "')

                try:
                    self.userInputTwo = self.commandIn[2]
                except Exception:
                    self.userInputTwo = "Null"
                    pass

                try:
                    self.userInput = self.commandIn[1]
                except Exception:
                    self.userInput = "Null"
                    pass
                self.commandIn = self.commandIn[0]
                print(self.commandIn)
                print(self.userInput)
                print(self.userInputTwo)
                await self.run_command(self.commandIn)
                #await message.channel.send( "Prototype Unit 0001 is ready to accept programming")

    #add a command to the bot
    def add_command(self,finfo,fname,finput,ftype, group = "default"):
        self.command = {
            "info": "null",
            "name": "null",
            "input": [],
            "type": "null",
            "func": "null",
        }
        def new_command(ffunc):
            self.command["info"] = finfo
            self.command["name"] = fname
            self.command["input"] = finput
            self.command["type"] = ftype
            self.command["func"] = ffunc
            self.commandList[ffunc.__name__] = self.command
            new_command.all = self.command
            return ffunc
        return new_command

    #Find and execute the desired command from the database
    async def run_command(self, command):
        #All of the commands
        for key in self.commandList.keys():
            self.command = self.commandList.get(key)
            self.commandFunc = self.command.get("func")
            self.commandInfo = self.command.get("info")
            self.commandName = self.command.get("name")
            self.commandArgs = self.command.get("input")

            if len(self.commandArgs) == 0 and key == str(command):
                await self.commandFunc(self, self.bot, self.message)
                return

            if len(self.commandArgs) == 1 and key == str(command):
                await self.commandFunc(self, self.bot, self.message, self.userInput)
                return

            if len(self.commandArgs) == 2 and key == str(command):
                await self.commandFunc(self, self.bot, self.message, self.userInput, self.userInputTwo)
                return

            else:
                pass

        else:
            await self.message.channel.send("No command called " + str(command) + " found. ;~;. here, I'll give you some help :D" )
            await self.display_help(self.bot, self.message)

        #elif command  == "give_role":
            #if self.userInput =="Null":
                #await self.message.channel.send(self. "ERROR: NO USER INPUT DETECTED")
                #return
            #else:
                #await self.give_role(self.bot, self.message, self.userInputTwo, self.userInput)


if __name__ =="__main__":
    core = Core("lol")
    finfo = "this command prints hello world to the screen"
    fname = "hello_world"
    finput = 0
    ftype = "on_message"
    @core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
    async def say_hello():
        print('hello world')





    print(str(core.run_command("give_role")))
    #print(str(core.commandList))
    #print(str(core.commandList.get("say_hello",0)))
    #print(str(core.commandList.get("dumb_shit",0)))
