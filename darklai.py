from decorators import command

import discord
import logging
import asyncio
import os
import datetime
import plugins.core
import filehandler
import sys
import codecs

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class Darklai(discord.Client):
    def __init__(self, directory, pVal, enablelogging = True,  *args, **kwargs):
        super().__init__(intents=discord.Intents.all())
        self.core = plugins.core.Core(directory, pVal)
        self.fileHandler = filehandler.FileHandler()

        self.msgAuthor = ""
        self.msgContent = ""
        self.msgChannel = ""
        self.msgServer = ""
        self.isSummoned = False
        self.isBanned = False
        self.bannedMember = discord.Member
        self.unapprovedMembersFile = "UnapprovedMembers.txt"
        self.encoding = "utf-8"
        self.unapprovedMembersList = []
        self.lastMemberApproved = ""


    #def run(self, *args):
        #self.loop.run_until_complete(self.start(*args))

    async def on_ready(self):
        await self.fileHandler.log_message("Darklai is ready", 0)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        pass

    async def _on_message(self, message):
        if message.author.id != self.darklai.user.id:
            for command_name, func in self.commands.items():
                await func(message)
        await self.on_message(message)

    #every time a message is sent, darklai saves the content of it for later
    async def on_message(self, message):
        self.msgAuthor = message.author
        self.msgChannel = message.channel
        self.msgServer = message.guild
        self.msgContent = message.content
        self.unapprovedMembersList = []
        await self.fileHandler.log_message("MESSAGE SENT\n" + "USER: " + str(self.msgAuthor.id) + "\n" +"CHANNEL: " + str(self.msgChannel) + "\n" + "SERVER: " + str(self.msgServer) + "\n", 1)
        if message.content == "boop" or message.content == "bap" or message.content == "Boop" or message.content == "Bap" or message.content == "BOOP" or message.content == "BAP":
            await self.send_message("Boops " + "<@!" + message.author.id + "> 's snooter back :3")
        if message.content.upper() == "DORMS MOMENT":
            with open('dorms_moment.jpeg', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

        if "discord.gg" in message.content:
            await self.purge_from( limit=int(1))
            await self.send_message( "NOU, bad bad bad! nou sevar links <@!" + message.author.id + "> >:LLLLLLLLLLLLLLLLLLLLLLLL")

        if str(message.channel.type) == "private":
            if str(message.content).find('=') == 0 or str(message.content).find("@269304629307637761"):
                self.isSummoned = True
                await self.core.run_on_message_plugins(self, message)
            return
        if message.author.__class__ != discord.Member:
            return

        if str(message.content).find('=') == 0 or str(message.content).find("@269304629307637761"):
            self.isSummoned = True
            await self.core.run_on_message_plugins(self, message)
        else:
            self.isSummoned = False
            #print(str(self.msgAuthor))
        if message.content == "HOWDY DOODY":
            await self.delete_message(message)
            return

        #Find out what users still need to be approved
        if message.author != discord.Guild.get_member(message.guild, "269304629307637761"):
            self.membersList = await self.fileHandler.get_file_contents(self.unapprovedMembersFile)
            #print(str(self.membersList))

            #For every member in the unapproved members raw data, split apart the member name and time
            for i in range(0,len(self.membersList)):
                self.unapprovedMembersList.append(str(self.membersList[i]).split(":::"))
                #print(str(self.unapprovedMembersList))

            #For every element in the unapproved members list
            for i in range(0, len(self.unapprovedMembersList)):
                self.membersList = self.unapprovedMembersList[i]
                #print("Length of member List" + str(len(self.unapprovedMembersList)))
                #print("Unaproved member list" + str(self.unapprovedMembersList))
                if len(self.membersList) == 2:
                    for i in range(0, len(self.membersList)):
                        if len(self.membersList) != 2:
                            return
                        self.memberStartTime = datetime.datetime.strptime(self.membersList[1], "%Y-%m-%d %H:%M:%S.%f")
                        self.memberName = str(self.membersList[0])
                        #print("member time " + str(self.memberStartTime))
                        #print("member list " + str(self.membersList))
                        #print("member name " + str(self.memberName))
                        self.endTime = datetime.datetime.now()
                        self.deltaTime = self.endTime - self.memberStartTime
                        self.minutesPassed = int(self.deltaTime.total_seconds() / 60)
                        print(str(self.minutesPassed))

                        #If the minutes passed is greater then 60 mintes, give them the server approved role
                        if self.minutesPassed > 60 and self.membersList[0] != self.lastMemberApproved:
                            self.lastMemberApproved = self.membersList[0]
                            self.memberObj = discord.Guild.get_member(message.guild, self.memberName)
                            print ("Member " + str(self.memberObj) + str(self.memberName))
                            await self.send_message( "I have approved " + str(
                                self.memberObj.name) + " because they have been on the " + str(
                                message.guild) + " server for " + str(self.minutesPassed) + " minutes! :D")
                            try:
                                await self.send_message(self.memberObj, "Psst, you can post stuff in other channels on the " + str(message.guild) + " server now! :D. Waiting for " + str(self.minutesPassed) + " minutes has paid off. yay! :DDD *Throws party* https://www.youtube.com/watch?v=0hUUgxXzsrc")
                            except:
                                one =1
                            await self.core.give_role(self, message, self.memberName, "Server_Approved✓", isautomated = True)
                            await self.send_message( "Can I have pets now? o3o")



                            # Find out if the user was unapproved and remove them from the log
                            await self.fileHandler.get_file_contents(self.unapprovedMembersFile)
                            self.membersListData = []
                            for i in range(0, len(self.fileHandler.dataList)):
                                self.membersListData.append(self.fileHandler.dataList[i].split(":::"))
                            #print(str(self.membersListData))

                            with open(self.unapprovedMembersFile, 'w', encoding=self.encoding) as file:
                                i3 = 0
                                try:
                                    for line in self.membersListData:
                                        if str(self.membersListData[line]) == str(self.membersList):
                                            file.write(line)
                                        i3 +=1
                                except Exception:
                                    pass
                                #update the member List
                                self.membersList = await self.fileHandler.get_file_contents(self.unapprovedMembersFile)
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_message_delete(self, message):
        await self.fileHandler.log_message(
            "MESSAGE DELETED\n" + "USER: " + str(message.author.id) + "\n" + "CHANNEL: " + str(message.channel) + "\n" + "SERVER: " + str(message.guild) + "\n",
            1)
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_member_join(self, member):
        await self.fileHandler.log_message("MEMBER JOINED\n" + "USER: " + str(member.id) + "\n",1)
        await self.send_message(member, " Welcome to EAD " + str(member) + " ! " + " :D Be sure you read and understand the rules :T " + " https://www.youtube.com/watch?v=DpQw3WLP3E4")

        #Adds a new member to the unapproved member's list
        now = datetime.datetime.now()
        self.memberStartTime = now
        await self.fileHandler.append_to_file((str(member.id) + ":::" + str(self.memberStartTime)),self.unapprovedMembersFile)
        pass



    async def on_member_remove(self, member):
        await self.fileHandler.log_message("MEMBER LEFT\n" + "USER: " + str(member.id) + "\n", 1)


        #Find out if the user was unapproved and remove them from the log
        await self.fileHandler.get_file_contents(self.unapprovedMembersFile)
        self.membersList = [0]
        for i in range(0, len(self.fileHandler.dataList)):
            self.membersList.append(self.fileHandler.dataList[i].split(":::"))
        print(str(self.membersList))

        with open(self.unapprovedMembersFile, 'w', encoding=self.encoding) as file:
            i = 0
            for line in self.membersList:
                if self.membersList[i] == str(member.id):
                    file.write(line)
                i+= 1
        #print("Member string" + str(member) + str(self.bannedMember))
       #if (str(self.bannedMember.id) == str(member.id)) or (self.isBanned == True):
            #print("MEMBER NOT GOODBYED " + str(member) + str(self.bannedMember))
            #self.isBanned = False
            #pass
        #elif (self.isBanned == False) or (str(self.bannedMember.id) != str(member.id)):
            #await self.send_message(member.server, "Aww, it's a shame to see " + str(
                #member) + " leave." + " :C " + " https://www.youtube.com/watch?v=92eo1hSAgTA")
        pass

    async def on_member_ban(self, member):
        await self.fileHandler.log_message("MEMBER BANNED\n" + "USER: " + str(member.id) + "\n", 1)
        await self.send_message(member.guild, "TO THE MOOOOOOOOOOOOON WITH " + str(
            member) + " BEEEYATCH!!! https://www.youtube.com/watch?v=VvqGnkJth08")
        self.bannedMember = member
        print("Member banned string " + str(member.id) + str(self.bannedMember.id))
        self.isBanned = True
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

    async def on_member_unban(self, member):
        await self.fileHandler.log_message("MEMBER UNBANNED\n" + "USER: " + str(member.id) + "\n", 1)
        pass

    async def on_typing(self, channel, user, when):
        pass



