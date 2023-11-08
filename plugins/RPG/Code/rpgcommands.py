

import plugins.RPG.Code.rpgcore
import discord
from plugins.RPG.Code import character
from plugins.RPG.Code import items


class RPGCommands:

    def __init__(self, directory, pVar):
        self.group = "RPG Commands"
        self.dir = directory
        self.pVar = pVar
        self.pDir = "RPG" + pVar

    def add_commands(self, bot):

        finfo = "This command will allow you to shoot at a target"
        fname = "target_practice"
        finput = []
        ftype = "on_message"


        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def target_practice(self, bot, message):
            print("looking in for RPG Target Practice: " + self.dir + self.pDir + "Characters" + self.pVar + str(message.author.id) + ".cdat")
            player = character.Character(self.dir + self.pDir + "Characters" + self.pVar + str(message.author.id) + ".cdat", self.dir, self.pVar)
            dummy = character.Character(self.dir + self.pDir + "Characters" + self.pVar + "practicedummy.cdat", self.dir, self.pVar)

            shootingRange = plugins.RPG.Code.rpgcore.RPG(self.dir,self.pVar)
            async def shooting():
                await player.load()
                await dummy.load()
                count = 0
                prevPlayerWep = player.lists.equippedItems["Weapon"]
                player.lists.equippedItems["Weapon"] = "Practice Rifle"
                if isinstance(player.lists.equippedItems["Ammo"], str):
                    player.lists.equippedItems["Ammo"] = {}
                await message.channel.send(
                                       player.strings.name + " Given a " + str(player.lists.equippedItems["Weapon"]))
                await player.get_weapon()
                originalAmmo = player.lists.equippedItems["Ammo"][player.weapon.lists.ammoTypes[0]]
                await shootingRange.give_ammo(player, player.weapon.lists.ammoTypes[0], 10)
                await message.channel.send( await player.load_weapon())

                while (dummy.nonModifiables.hp > 0) and (player.nonModifiables.hp > 0):
                    await message.channel.send( "What will you do " + str(
                        player.strings.name) + "? \n```" + "ACTIONS \nReload: reloads your weapon \n"  + "\nClip: " + str(player.nonModifiables.weaponClip) + "\n" + player.strings.ammoEquipped + ": " + str(player.lists.equippedItems["Ammo"][player.weapon.lists.ammoTypes[0]]) +  "\nStop: Stops the target practice\n Cancel: cancels an action \n\n" + " MOVEMENTS: \n Move (currently a one directional vector, like a duel)\n distance from target is "+ str(shootingRange.distance)+"m\n \nATTACKS: \n Ranged \n" + str(
                        await shootingRange.get_odds(player, dummy, "Ranged")) + "\n Melee \n" + str(
                        await shootingRange.get_odds(player, dummy, "Melee")) + " \n" + "```")
                    def check(m):
                        return m.author == message.author and m.channel == message.channel
                    msg = await bot.wait_for("message", check=check)
                    if msg.content.upper() == "MOVE":
                        await message.channel.send( "Move how many spaces " + str(
                            player.strings.name) + "? \n```" + "CURRENT DISTANCE FROM TARGET (in m) \n" + str(
                            shootingRange.distance) + "m" + "\nWEAPON REACH (in cm)\n" + str(
                            float(player.weapon.stats.reach) * 100.0) + "cm" + "\nWEAPON RANGE (in m)\n" + str(
                            player.weapon.stats.range) + "m" "```")
                        msg = await bot.wait_for("message", check=check)
                        try:
                            await message.channel.send( await shootingRange.move(player, int(msg.content)))
                        except Exception:
                            await message.channel.send( "Invalid input :LLLL")
                    elif msg.content.upper() == "STOP":
                        player.nonModifiables.hp = player.modifiables.hPMax
                        await player.update_non_modifiables()
                        dummy.nonModifiables.hp = dummy.modifiables.hPMax
                        player.nonModifiables.exp += 10 * count
                        await message.channel.send( player.strings.name + " Rewarded " + str(10*count) + " EXP for doing target practice! :D")
                        player.nonModifiables.hp = player.modifiables.hPMax
                        await message.channel.send(
                                               "Updated nonModifiables\n" + str(await player.update_non_modifiables()))
                        player.lists.equippedItems["Weapons"] = prevPlayerWep
                        player.lists.equippedItems["Ammo"].update({player.weapon.lists.ammoTypes[0]: originalAmmo})
                        dummy.nonModifiables.hp = dummy.modifiables.hPMax
                        await player.save()
                        return
                    elif msg.content.upper() == "CANCEL":
                        await message.channel.send( "Action canceled")
                        continue
                    elif msg.content.upper() == "RANGED":
                        await message.channel.send( "```" + await shootingRange.get_odds(player, dummy, "Ranged") + "```")
                        await message.channel.send( str(await shootingRange.attack_ranged(player, dummy, 1)))

                    elif msg.content.upper() == "MELEE":
                        await message.channel.send( "```" + await shootingRange.get_odds(player, dummy, "Melee") + "```")
                        await message.channel.send( str(await shootingRange.attack_melee(player, dummy)))
                    elif msg.content.upper() == "RELOAD":
                        await message.channel.send( await player.load_weapon())
                    else:
                        pass
                    count+=1

                player.nonModifiables.hp = player.modifiables.hPMax
                await message.channel.send( "Updated nonModifiables\n" + str(await player.update_non_modifiables()))
                player.lists.equippedItems["Weapons"] = prevPlayerWep
                dummy.nonModifiables.hp = dummy.modifiables.hPMax
                await player.save()
                return


            print(str(message.author.id))
            try:
                await player.load()
            except Exception:
                player.modifiables.attack = ""

            if player.modifiables.attack == "":
                await message.channel.send( "You need to make a character to do this. but you can use the example character for now :D")
                player = character.Character(self.dir + self.pDir + "Characters" + self.pVar +"examplecharacterfile.cdat", self.dir, self.pVar)
                await shooting()
            else:
                await shooting()

            if self.hugMode == True:
                await message.channel.send( "*Super hugs" + str(message.author) + "back*")



        finfo = "This command will display rpg information on a member"
        fname = "rpg_info"
        finput = ["member"]
        ftype = "on_message"


        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def rpg_info(self, bot, message, member):

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
            player = character.Character(self.dir + self.pDir + "Characters" + self.pVar + str(self.member.id) + ".cdat", self.dir, self.pVar)
            await player.load()
            if player.modifiables.attack == "":
                await message.channel.send( "This member has not made a character!")
            else:
                await player.get_info()
                #print(player.playerInfo)
                await message.channel.send( "Here's the info on "+ str(self.member) + "'s RPG file" + "```" + str(player.dataHandler.info) + "```")
            if self.hugMode == True:
                await message.channel.send( "*Super hugs" + str(message.author) + "back*")


        finfo = "This command will allow you to attack a specified member"
        fname = "attack"
        finput = ["member"]
        ftype = "on_message"


        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def attack(self, bot, message, member):
            async def begin(session, attacker, defender):
                await attacker.load()
                await defender.load()
                count = 0
                await attacker.get_weapon()
                await message.channel.send( await attacker.load_weapon())

                while (defender.nonModifiables.hp > 0) and (attacker.nonModifiables.hp > 0) and (session.actionpoints > 1):
                    await message.channel.send( "What will you do " + str(
                        attacker.strings.name) + "? \n```" + "ACTIONS \nReload: reloads your weapon \n" + "\nClip: " + str(
                        attacker.nonModifiables.weaponClip) + "\n" + attacker.strings.ammoEquipped + ": " + str(
                        attacker.lists.equippedItems["Ammo"][attacker.weapon.lists.ammoTypes[
                            0]]) + "\nStop: Stops the PvP session\n Cancel: cancels an action \n\n" + " MOVEMENTS: \n Move (currently a one directional vector, like a duel)\n distance from target is " + str(
                        session.distance) + "m\n \nATTACKS: \n Ranged \n" + str(
                        await session.get_odds(attacker, defender, "Ranged")) + "\n Melee \n" + str(
                        await session.get_odds(attacker, defender, "Melee")) + " \n" + "```")
                    def check(m):
                        return m.author == message.author and m.channel == message.channel
                    msg = await bot.wait_for("message", check=check)
                    if msg.content.upper() == "MOVE":
                        await message.channel.send( "Move how many spaces " + str(
                            attacker.strings.name) + "? \n```" + "CURRENT DISTANCE FROM TARGET (in m) \n" + str(
                            session.distance) + "m" + "\nWEAPON REACH (in cm)\n" + str(
                            float(attacker.weapon.stats.reach) * 100.0) + "cm" + "\nWEAPON RANGE (in m)\n" + str(
                            attacker.weapon.stats.range) + "m" "```")
                        def check(m):
                            return m.author == message.author and m.channel == message.channel
                        msg = await bot.wait_for("message", check=check)
                        try:
                            await message.channel.send(
                                                   await session.move(attacker, int(msg.content)))
                        except Exception:
                            await message.channel.send( "Invalid input :LLLL")
                    elif msg.content.upper() == "STOP":
                        attacker.nonModifiables.hp = attacker.modifiables.hPMax
                        await attacker.update_non_modifiables()
                        defender.nonModifiables.hp = defender.modifiables.hPMax
                        attacker.nonModifiables.exp += 10 * count
                        defender.nonModifiables.exp += 10 * count
                        if (attacker.nonModifiables.hp > defender.nonModifiables.hp):
                            await message.channel.send( attacker.strings.name + " Has won against " + defender.strings.name + "and was rewarded" + str(
                                10 * count) + " EXP!")
                        attacker.nonModifiables.hp = attacker.modifiables.hPMax
                        await message.channel.send(
                                               "Updated nonModifiables\n" + str(
                                                   await attacker.update_non_modifiables()))
                        defender.nonModifiables.hp = defender.modifiables.hPMax
                        await attacker.save()
                        return
                    elif msg.content.upper() == "CANCEL":
                        await message.channel.send( "Action canceled")
                        continue
                    elif msg.content.upper() == "RANGED":
                        await message.channel.send( "```" + await session.get_odds(attacker, defender,
                                                                                                     "Ranged") + "```")
                        await message.channel.send(
                                               str(await session.attack_ranged(attacker, defender, 1)))

                    elif msg.content.upper() == "MELEE":
                        await message.channel.send(
                                               "```" + await session.get_odds(attacker, defender, "Melee") + "```")
                        await message.channel.send(
                                               str(await session.attack_melee(attacker, defender)))
                    elif msg.content.upper() == "RELOAD":
                        await message.channel.send( await attacker.load_weapon())
                    else:
                        pass
                    count += 1

                attacker.nonModifiables.hp = attacker.modifiables.hPMax
                await message.channel.send(
                                       "Updated nonModifiables\n" + str(await attacker.update_non_modifiables()))
                defender.nonModifiables.hp = defender.modifiables.hPMax
                await attacker.save()
                await defender.save()
                return
            attacker = character.Character(self.dir + self.pDir + "Characters" + self.pVar + str(message.author.id) + ".cdat",self.dir, self.pVar)
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

            defender = character.Character(self.dir + self.pDir + "Characters" + self.pVar + str(self.member.id) + ".cdat", self.dir, self.pVar)
            await attacker.load()
            await defender.load()
            await defender.get_weapon()
            await attacker.get_weapon()
            if defender.modifiables.attack == "":
                await message.channel.send( "This member has not made a character!")
            elif self.member.id == message.author.id:
                await message.channel.send( "You can't battle yourself, silly")
                return
            else:
                await message.channel.send( "A CHALLENGER APPROACHES!!! " + str(attacker.strings.battleTheme))
                await attacker.save()
                await defender.save()
                print("data saved")

            if self.hugMode == True:
                await message.channel.send( "*Super hugs" + str(message.author) + "back*")


        finfo = "This command will allow you to create an rpg character"
        fname = "create_rpg_character"
        finput = []
        ftype = "on_message"

        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def create_rpg_character(self, bot, message):
            self.member = discord.Guild.get_member_named(message.guild, str(message.author))
            player = character.Character(self.dir + self.pDir + "Characters" + self.pVar + str(message.author.id) + ".cdat", self.dir, self.pVar)
            savecharacter = True

            async def start_creation():
                stats = ""
                setattr(player.nonModifiables, "level", 1)
                await player.update_non_modifiables()
                for attr in dir(player.strings):

                    if attr == "name":
                        await message.channel.send( "Name your character")
                        def check(m):
                            return m.author == message.author and m.channel == message.channel
                        msg = await bot.wait_for("message", check=check)
                        player.strings.name = msg.content

                    if attr == "race":
                        await message.channel.send( "What race is your character?")
                        def check(m):
                            return m.author == message.author and m.channel == message.channel
                        msg = await bot.wait_for("message", check=check)
                        player.strings.race = msg.content

                    if attr == "battleTheme":
                        await message.channel.send( "Give your character a battle theme (use a youtube link)")

                        def check(m):
                            return m.author == message.author and m.channel == message.channel

                        msg = await bot.wait_for("message", check=check)
                        player.strings.battleTheme = msg.content

                    else:
                        pass

                for attr in dir(player.measurements):
                    if (not attr.startswith('__')) and (not callable(getattr(player.measurements, attr))):
                        await message.channel.send( "Set the " + str(attr) + " of your character :V (in cm)")
                        def check(m):
                            return m.author == message.author and m.channel == message.channel
                        msg = await bot.wait_for("message", check=check)
                        try:
                            await message.channel.send(
                                                   str(await player.edit_stats(attr, str(msg.content))))
                        except Exception:
                            await message.channel.send(
                                                   "That input was invalid! :LLL. setting " + str(attr) + " to 100")
                            await player.edit_stats(attr, 100)


                for attr in dir(player.modifiables):
                    if (not attr.startswith('__')) and (not callable(getattr(player.modifiables, attr))):
                        await message.channel.send( "Set the variable for the " + str(
                            attr) + " stat. (type in +=stop to stop")

                        def check(m):
                            return m.author == message.author and m.channel == message.channel

                        msg = await bot.wait_for("message", check=check)
                        if str(msg.content).upper() == "+=STOP":
                            await message.channel.send( "Would you like to save your data? +=yes or +=no")
                            def check(m):
                                return m.author == message.author and m.channel == message.channel
                            msg = await bot.wait_for("message", check=check)
                            if str(msg.content).upper() == "+=YES":
                                await player.save()
                                await message.channel.send(
                                                       "Character data for " + str(self.member) + " saved! :D")
                            else:
                                await message.channel.send(
                                                       "Character data for " + str(self.member) + " not saved :C")
                                savecharacter = False
                                return
                        else:
                            try:
                                await message.channel.send( str(await player.edit_stats(attr, str(msg.content))))
                            except Exception:
                                await message.channel.send(
                                                       "That input was invalid! :LLL. setting " + str(attr) + " to 0. you can edit this value later by entering the command edt_rpg_stat")
                                await player.edit_stats(attr, 0)
                            stats += (str(await player.get_stat(attr)) + "\n")

                await message.channel.send("Your current stats:" +"```" + stats + "```")


            if await player.load() == True:
                await message.channel.send("You already have a character, would you like to reset it and make a new one :/ (+=yes for yes and +=no for no)")
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await bot.wait_for("message", check=check)
                if str(msg.content).upper() == "+=YES":
                    await start_creation()
                    pass
                else:
                    return
            else:
                await start_creation()

            if self.member == None:
                return

            if savecharacter == False:
                return
            else:
                await player.save()
                await message.channel.send(
                                   "Character data for " + str(self.member) + " saved! :D")
                return


        finfo = "This command will allow you to edit stats and values for your rpg character"
        fname = "edit_rpg_stat"
        finput = ["statname", "value"]
        ftype = "on_message"

        @bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        async def edit_rpg_stat(self, bot, message, statname, value):
            self.member = discord.Guild.get_member_named(message.guild, str(message.author))
            player = character.Character(self.dir + self.pDir + "Characters" + self.pVar + str(message.author.id) + ".cdat", self.dir, self.pVar)
            if (await player.load() == False):
                await bot.send_message(message.channel, "You have not created an rpg character! do =create_rpg_character to create one! :V")
                return
            await player.load()
            try:
                await bot.send_message(message.channel, str(await player.edit_stats(str(statname), int(value))))
                await player.save()
            except Exception:
                await bot.send_message(message.channel,
                                       "Stat " + str(
                                           statname) + " is either invalid or your input " + str(value) + " is invalid")
                return

        #finfo = "This command will allow you to select an item to use"
        #fname = "select_item"
        #finput = ["item"]
        #ftype = "on_message"

        #@bot.core.add_command(finfo=finfo, fname=fname, finput=finput, ftype=ftype)
        # The command to give a user a specific role
        #async def select_item(self, bot, message, item):
            #self.member = discord.Guild.get_member_named(message.guild, str(message.author))
           #player = character.Character("C:\\Users\\Alex\\PycharmProjects\\DARKAi v2\\RPG\\Characters\\" + str(message.author.id) + ".cdat")
            #if (await player.load() == False):
                #await bot.send_message(message.channel, "You have not created an rpg character! do =create_rpg_character to create one! :V")
                #return
            #await player.load()
            #try:
                #await bot.send_message(message.channel, str(await player.edit_stats(str(), int(value))))
                #await player.save()
            #except Exception:
                #await bot.send_message(message.channel,
                                       #"Stat " + str(
                                           #statname) + " is either invalid or your input " + str(value) + " is invalid")
                #return
