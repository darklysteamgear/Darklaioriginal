
import discord


#The moderation commands
class ModCommands:
    def __init__(self, directory, pVar):
        self.group = "Moderation Commands"
        self.dir = directory
        self.pVar = pVar

    def add_commands(self, bot):



        finfo = "this command gives the user a role"
        fname = "give_role"
        finput = ["member", "role"]
        ftype = "on_message"


        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def give_role(self, bot, message, member, role, isautomated = False):
            self.member = discord.Guild.get_member_named(message.guild, str(member))

            if self.member == None:
                memberCheck = str(member)
                member = member.split('!', 1)[-1]
                if str(member) == str(memberCheck):
                    member = member.split('@', 1)[-1]
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

            if (self.member.guild_permissions.administrator == True):
                hasReqRole = True

            if (isautomated == True):
                hasReqRole = True

            # For every role in the user's roles, check for the appropriate role
            for r in self.member.roles:

                if r.id in self.roleList:
                    hasRole = True

            # Check to make sure that they have the required things
            if hasReqRole == True and hasRole == False:
                try:
                    await bot.add_roles(self.member, self.role)
                    await message.channel.send( "I have given " + str(self.member) + " the role :D!!!")
                except discord.Forbidden:
                    await message.channel.send( "I don't have perms to add that role. :/.")

            elif hasReqRole == True and hasRole == True:
                try:
                    await message.channel.send( str(self.member) + " You already have that role :V")
                except discord.Forbidden:
                    await message.channel.send( "I don't have perms to add that role. :/.")

            elif hasReqRole == False and hasRole == True:
                try:
                    await message.channel.send( "You cannot give that role! You butt :LLL")
                except discord.Forbidden:
                    await message.channel.send( "I don't have perms to add that role. :/.")
            else:
                try:
                    await message.channel.send( "NOU U cannot do that :VVVVV")
                except discord.Forbidden:
                    await message.channel.send( "I don't have perms to add that role. :/.")
            if self.hugMode == True:
                await message.channel.send( "*Hugs you tightly ^.^*")
            return

        finfo = "this command gives the user information about a specified user"
        fname = "member_information"
        finput = ["member"]
        ftype = "on_message"


        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def member_information(self, bot, message, member):
            self.member = discord.Guild.get_member_named(message.guild, str(member))

            if self.member == None:
                memberCheck = str(member)
                member = member.split('!', 1)[-1]
                if str(member) == str(memberCheck):
                    member = member.split('@', 1)[-1]
                member = member.split('>', 1)
                member = member[0]
                self.member = discord.Guild.get_member(message.guild, member)

            if self.member == None:
                return

            roleList = []
            permsList = []

            for i in range (0,len(self.member.roles)):
                roleList.append(str(self.member.roles[i]))

            if self.member.guild_permissions.administrator == True:
                permsList.append("Is an admin")

            if self.member.guild_permissions.ban_members == True:
                permsList.append("Can ban members")

            if self.member.guild_permissions.kick_members == True:
                permsList.append("Can kick members")

            roles = str(roleList)
            user = await bot.get_user_info(member)
            avatar = str(user.avatar_url)
            roleCount = str(len(self.member.roles))
            voice = str(self.member.voice.voice_channel)
            joined = str(self.member.joined_at)
            status = str(self.member.status)
            game = str(self.member.game)
            guild = str(self.member.guild)
            nick = str(self.member.nick)

            highestRole = str(self.member.top_role)
            permissions = str(permsList)
            memberInfoStr = ""

            memberInfoStr += "Here's full information on the user " + str(member) + ",Or " + str(self.member) + ". Why do I keep doing this?\n\n```" + "Roles: " + roles + "\n\nTotal Amount of roles: " + roleCount + "\n\nVoice Status: " + voice + "\n\nDate Joined: " + joined + "```"
            memberInfoStr2 = "```Current Status: " + status + "\n\nGame Currently Playing: " + game + "\n\nCurrent Server: " + server + "\n\nNickname: " + nick + "\n\nHighest Role: " + highestRole + "\n\nServer Permissions: " + permissions + "```"
            memberInfoStr3 = avatar
            await message.channel.send( memberInfoStr3)
            await message.channel.send( memberInfoStr)
            await message.channel.send( memberInfoStr2)

        finfo = "This command will delete messages after a certain point."
        fname = "delete_messages"
        finput = ["messagestodelete"]
        ftype = "on_message"


        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def delete(self, bot, message, messagestodelete):
            if message.author.guild_permissions.administrator == True:
                await message.channel.send( "Terminating messages. hehe, that's a funny word ^.^")
                def is_me(m):
                    return m.author == bot.user

                def is_not_me(m):
                    return m.author != bot.user

                await bot.purge_from( limit=int(messagestodelete))
                if int(messagestodelete) > 20:
                    fire = '''
                                ,.   (   .      )        .      "
                               ("     )  )'     ,'        )  . (`     '`         )  )  .   (`   '`     )
                             .; )  ' (( (" )    ;(,     ((  (  ;)  "  )"       / )   (;)  "   )"     / ) (
                             _"., ,._'_.,)_(..,( . )_  _' )_') (. _..( '..   ) \(_)/ (. _..( '..   ) \(_)/
                             '''
                    await message.channel.send( "```" + fire + "```")
                    await message.channel.send( "AAAAAAAAAAAAAHAHAHAHAHAHAAHHAHAHAAHAHA!!!!!!!! >:D")
                    await message.channel.send( "https://cdn.discordapp.com/attachments/189193410245165056/353745551675621376/Darklys_flamethrower.png")
                    await bot.purge_from( limit=int(messagestodelete), check=is_not_me)
                    await message.channel.send( "Burned " + str(messagestodelete) + " messages... I think.")
                    await bot.purge_from( limit=int(6), check=is_me)
                    self.hugMode = False
                else:
                    await bot.purge_from( limit=int(messagestodelete))
                    await message.channel.send( "Deleted " + str(messagestodelete) + " message(s)")
                    await bot.purge_from( limit=int(1), check=is_me)

            else:
                await message.channel.send( "I'm sorry " + str(message.author) + " but you cannot do that :C. here, have a cookie instead *gives you a cookie*")
                if self.hugMode == True:
                    await message.channel.send( "*Tackle hugs then snuggles you* error: overwheming affection detected.")