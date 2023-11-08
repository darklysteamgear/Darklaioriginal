
import discord
import logging
import asyncio
import random
import math
import filehandler
import datetime
from os import walk
from plugins.RPG.Code.datahandling import Data
from plugins.RPG.Code.items import Item
from plugins.RPG.Code.items import Weapon


# The class object for characters
class Character:
    def __init__(self, filename, directory, pVar):

        # misc start of class items
        self.fileReader = filehandler.FileHandler(enablelogging=False, encoding="ascii")
        self.dataHandler = Data(self)
        self.weapon = Weapon()
        self.selectedItem = Item()
        self.updateItem = Item()
        self.pVar = pVar
        self.isLogging = True
        self.fileName = filename
        self.dir = directory + "RPG" + self.pVar
        print("RPG directory" + self.dir)

        # player strings
        class Strings:
            def __init__(self):
                self.name = "None"
                self.race = "None"
                self.battleTheme = "None"
                self.ammoEquipped = "None"

        # player modifiable stats
        class Modifiables:
            def __init__(self):
                self.hPMax = 10
                self.attack = 0
                self.defense = 0
                self.stealth = 0
                self.agility = 0
                self.luck = 0
                self.accuracy = 0
                self.weightCap = 10

        # Non player modifiable stats
        class NonModifiables:
            def __init__(self):
                self.hp = 0
                self.level = 1
                self.exp = 0
                self.eXPMax = 100
                self.expTotal = 0
                self.weightTotal = 0.0
                self.availablePoints = 10
                self.totalPoints = 10
                self.weaponClip = 0

        # player length, width and height (in cm)
        class Measurements:
            def __init__(self):
                self.length = 0
                self.width = 0
                self.height = 0

        # player inventory
        class Lists:
            def __init__(self):
                self.inventory = {}

                # player equipped items
                self.equippedItems = {
                    "Head": "None",
                    "Body": "None",
                    "Hands": "None",
                    "Lhand": "None",
                    "Rhand": "None",
                    "Weapon": "Fists",
                    "Feet": "None",
                    "Ammo": {},
                    "Misc": []
                }

                # player lists
                self.abilities = {}
                self.activeEffects = {}

        # booleans
        class CharBooleans:
            def __init__(self):
                self.isBleedout = False
                self.godMode = False
                self.isParalyzed = False
                self.isCrippled = False
                self.isOverweight = False

        # Start up all of the classes
        self.bools = CharBooleans()
        self.lists = Lists()
        self.strings = Strings()
        self.modifiables = Modifiables()
        self.nonModifiables = NonModifiables()
        self.measurements = Measurements()

    async def get_weapon(self):
        self.weaponName = self.lists.equippedItems["Weapon"]
        await self.weapon.load(
            self.dir +"Weapons" + self.pVar + str(self.weaponName) + ".wep")

    async def load_weapon(self):
        if self.weapon.strings.type == "Melee":
            self.nonModifiables.weaponClip = 100
            self.strings.ammoEquipped = "None"
            await self.get_weapon()
            return
        for ammo in self.lists.equippedItems["Ammo"]:

            for ammo2 in self.weapon.lists.ammoTypes:
                # print(self.weapon.lists.ammoTypes)
                # print("needed ammo: " + ammo2)
                if (self.strings.ammoEquipped != ammo2) and (self.nonModifiables.weaponClip != 0) and (
                    self.strings.ammoEquipped != ammo):
                    self.lists.equippedItems[self.strings.ammoEquipped] = float(
                        1 - float(1 / self.nonModifiables.weaponClip))
                    # self.strings.ammoEquipped = ammo
                    # print(self.lists.equippedItems[self.strings.ammoEquipped])
                if ammo == ammo2:
                    if self.strings.ammoEquipped == ammo2:
                        print(":P")

                    self.strings.ammoEquipped = ammo
                    self.lists.equippedItems["Ammo"][ammo2] = float(self.lists.equippedItems["Ammo"][ammo2])
                    # print("Equipped item ammo: " + str(self.lists.equippedItems["Ammo"][ammo2]))
                    self.nonModifiables.weaponClip = float(self.nonModifiables.weaponClip)
                    self.nonModifiables.weaponClip = (float(self.lists.equippedItems["Ammo"][ammo2]) + 1) - float(
                        self.lists.equippedItems["Ammo"][ammo2])
                    if float(self.lists.equippedItems["Ammo"][ammo2]) < 0:
                        self.nonModifiables.weaponClip = 0
                        # print("Weapon clip: " + str(self.nonModifiables.weaponClip))
                        # if 0.0 < self.nonModifiables.weaponClip < 1.0:
                        # self.nonModifiables.weaponClip -=1
                        # self.lists.equippedItems["Ammo"][ammo2] -= float(self.nonModifiables.weaponClip)
                        # print("equipped items ammo: " + str(self.lists.equippedItems["Ammo"][ammo2]))
                        # print("Clip: " + str(self.nonModifiables.weaponClip))
                        # print("Equipped Items String:" + str(self.lists.equippedItems))
                        # return("Reloaded. Clip: " + str(self.nonModifiables.weaponClip))

                    if self.nonModifiables.weaponClip == 1.0:
                        self.lists.equippedItems["Ammo"][ammo2] -= self.nonModifiables.weaponClip
                        self.nonModifiables.weaponClip = self.weapon.stats.clipSize
                        # print("equipped items ammo: " + str(self.lists.equippedItems["Ammo"][ammo2]))
                        # print("Clip: " + str(self.nonModifiables.weaponClip))
                        # print("Equipped Items String:" + str(self.lists.equippedItems))
                        return ("Reloaded. Clip: " + str(self.nonModifiables.weaponClip))

                    elif 0.0 < self.nonModifiables.weaponClip < 1.0:
                        self.lists.equippedItems["Ammo"][ammo2] -= self.nonModifiables.weaponClip
                        self.nonModifiables.weaponClip *= float(self.weapon.stats.clipSize)
                        # print("equipped items ammo: " + str(self.lists.equippedItems["Ammo"][ammo2]))
                        # print("Clip: " + str(self.nonModifiables.weaponClip))
                        # print("Equipped Items String:" + str(self.lists.equippedItems))
                        return ("Reloaded. Clip: " + str(self.nonModifiables.weaponClip))

                    else:
                        self.lists.equippedItems["Ammo"].pop(ammo2)
                        return ("No more bullets")
        return ("OUT OF AMMO FOR THIS WEAPON")
        # print("Equipped Items String:" + str(self.lists.equippedItems))
        # self.nonModifiables.weaponClip = self.weapon.stats.clipSize

    async def select_item(self, itemname):
        if itemname in self.lists.inventory:
            await self.selectedItem.load(
                self.dir + "Items" + self.pVar + str(itemname) + ".itm")
            self.selectedItem.stats.weight = float(self.lists.inventory[itemname]) * self.selectedItem.stats.weight
            # print(itemname)

    async def select_weapon(self, itemname):
        if itemname in self.lists.inventory:
            await self.selectedItem.load(
                self.dir + "Weapon" + self.pVar + str(itemname) + ".wep")
            self.selectedItem.stats.weight = float(self.lists.inventory[itemname]) * self.selectedItem.stats.weight
            # print(itemname)

    async def select_armor(self, itemname):
        if itemname in self.lists.inventory:
            await self.selectedItem.load(
                self.dir + "Armor" + self.pVar + str(itemname) + ".arm")
            self.selectedItem.stats.weight = float(self.lists.inventory[itemname]) * self.selectedItem.stats.weight
            # print(itemname)

    async def update_weight(self):
        self.nonModifiables.weightTotal = 0
        for item in self.lists.inventory:
            await self.updateItem.load(self.dir + "Items" + self.pVar + str(item) + ".itm")
            self.updateItem.stats.weight = float(self.lists.inventory[item]) * self.updateItem.stats.weight
            self.nonModifiables.weightTotal += self.updateItem.stats.weight
        if self.nonModifiables.weightTotal > self.modifiables.weightCap:
            self.bools.isOverweight = True
        else:
            self.bools.isOverweight = False

    async def use_item(self):
        returnStr = ''
        if self.selectedItem.strings.typeItem.upper() == "FOOD":
            for effect in self.selectedItem.lists.effects:
                effectAbility = effect.split(" ")
                if effectAbility[0].upper() == "RESTORE":

                    adder = int(getattr(self.nonModifiables, effectAbility[1]))
                    adder += int(self.selectedItem.lists.effects[effect])
                    print(str((float(self.nonModifiables.hp))) + " " + str((int(self.modifiables.hPMax))))
                    if (int(self.nonModifiables.hp)) >= (int(self.modifiables.hPMax)):
                        returnStr = (
                        "item " + self.selectedItem.strings.name + " not used because HP is already maxed!")
                        print("stuff and things")
                        return returnStr
                    if adder >= int(self.modifiables.hPMax):
                        setattr(self.nonModifiables, effectAbility[1], self.modifiables.hPMax)
                        self.lists.inventory[str(self.selectedItem.strings.name)] = float(
                            self.lists.inventory[str(self.selectedItem.strings.name)])
                        self.lists.inventory[str(self.selectedItem.strings.name)] -= 1 / float(
                            self.selectedItem.stats.uses)
                        returnStr = ("item " + self.selectedItem.strings.name + " used. HP maxed.") + (
                        "\nYour HP: " + str(self.nonModifiables.hp) + "/" + str(self.modifiables.hPMax))
                    else:
                        setattr(self.nonModifiables, effectAbility[1], adder)
                        self.lists.inventory[str(self.selectedItem.strings.name)] = float(
                            self.lists.inventory[str(self.selectedItem.strings.name)])
                        self.lists.inventory[str(self.selectedItem.strings.name)] -= 1 / float(
                            self.selectedItem.stats.uses)
                        returnStr = ("item " + self.selectedItem.strings.name + " used ") + (
                        "\nYour HP: " + str(self.nonModifiables.hp) + "/" + str(self.modifiables.hPMax))
            if float(self.lists.inventory[str(self.selectedItem.strings.name)]) <= 0:
                self.lists.inventory.pop(self.selectedItem.strings.name)
                self.selectedItem = Item()
                returnStr += ("item used up")
        return returnStr

    async def load(self):
        rawCharacterData = await self.fileReader.get_file_contents(self.fileName)
        for attr in dir(self):

            if (not attr.startswith('__')) and (not callable(getattr(self, attr)) and (not (attr == ("fileName"))) and (
            not (attr == ("equippedAmmo"))) and (not (attr == ("updateItem"))) and (
            not (attr == ("selectedItem"))) and (not (attr == ("weapon"))) and (not (attr == ("isLogging"))) and (
            not (attr == ("dataHandler"))) and (not (attr == ("playerInfo"))) and (not (attr == ("fileReader")))):
                # print(" LOAD Attribute found in main class " + str(attr))
                try:
                    await self.dataHandler.fetch_data(attr, rawCharacterData)
                except Exception:
                    # print("LOAD error: failed to find object " + str(attr) +" in class" )
                    pass

    # edit stat values for the character object
    async def edit_stats(self, attrname, value):
        if (hasattr(self.modifiables, attrname)):
            getattr(self.modifiables, attrname)
            await self.update_non_modifiables()
            limit = self.nonModifiables.availablePoints
            totalP = self.nonModifiables.totalPoints
            if (limit >= int(value)) and (totalP + int(value) >= 0):
                if attrname == "hPMax" or attrname == "weightCap":
                    adder = getattr(self.modifiables, attrname)
                    value = int(value) * 10 + int(adder)
                else:
                    adder = getattr(self.modifiables, attrname)
                    value = int(value) + int(adder)
                setattr(self.modifiables, attrname, int(value))

                await self.update_non_modifiables()
                reply = ("added " + str(value) + " to " + str(attrname) + " and this stat is now " + (
                    str(getattr(self.modifiables, attrname))) + ". you have " + (
                             str(getattr(self.nonModifiables,
                                         "availablePoints")) + " Stat points available") + " and a total of " + str(
                    getattr(self.nonModifiables, "totalPoints")) + " stat points invested into " + str(
                    getattr(self.strings, "name")))
                return reply
            elif ((limit < int(value)) or (limit + int(value) < 0)):
                reply = "sorry you cannot do that"
                return reply

        if (hasattr(self.strings, attrname)):
            setattr(self.strings, attrname, str(value))
            reply = (
            "replaced original string with " + str(value) + " inside of " + str(attrname) + " and this stat is now " + (
                str(getattr(self.strings, attrname))))
            return reply

        if (hasattr(self.measurements, attrname)):
            setattr(self.measurements, attrname, int(value))
            reply = ("replaced original measurement with " + str(value) + " inside of " + str(
                attrname) + " and this stat is now " + (
                         str(getattr(self.measurements, attrname))))
            return reply
        else:
            return

    # Gets the player's stats for a given attribute in the main class
    async def get_stat(self, attrname):
        if hasattr(self.modifiables, attrname):
            return str(str(attrname) + " = " + str(getattr(self.modifiables, attrname)))
        if hasattr(self.nonModifiables, attrname):
            return str(str(attrname) + " = " + str(getattr(self.nonModifiables, attrname)))
        if hasattr(self.strings, attrname):
            return str(str(attrname) + " = " + str(getattr(self.strings, attrname)))
        if hasattr(self.lists, attrname):
            return str(str(attrname) + " = " + str(getattr(self.lists, attrname)))
        if hasattr(self.measurements, attrname):
            return str(str(attrname) + " = " + str(getattr(self.measurements, attrname)))
        if hasattr(self.bools, attrname):
            return str(str(attrname) + " = " + str(getattr(self.bools, attrname)))
        else:
            return "Nothing found"

    async def get_info(self):
        self.dataHandler.info = ''
        for attr in dir(self):
            if (not attr.startswith('__')) and (not callable(getattr(self, attr)) and (not (attr == ("fileName"))) and (
            not (attr == ("equippedAmmo"))) and (not (attr == ("updateItem"))) and (
            not (attr == ("selectedItem"))) and (not (attr == ("weapon"))) and (not (attr == ("isLogging"))) and (
            not (attr == ("dataHandler"))) and (not (attr == ("playerInfo"))) and (not (attr == ("fileReader")))):
                # print("Attribute found in main class " + str(attr))
                try:
                    dataset = getattr(self, attr)
                    for attr2 in dir(dataset):
                        if (not attr2.startswith('__')) and (not callable(getattr(self, attr)) and (
                        not (attr == ("fileName"))) and (not (attr == ("equippedAmmo"))) and (
                        not (attr == ("updateItem"))) and (not (attr == ("selectedItem"))) and (
                        not (attr == ("weapon"))) and (not (attr == ("dataHandler"))) and (
                        not (attr2 == ("isLogging"))) and (not (attr2 == ("playerInfo"))) and (
                        not (attr2 == ("fileReader")))):
                            if await self.get_stat(attr2) != "Nothing found":
                                self.dataHandler.info += str(await self.get_stat(attr2)) + "\n"
                except Exception:
                    # print("error: failed to find object " + str(attr) +" in class" )
                    pass
        return self.dataHandler.info

    # edit stat values for the character object
    async def update_non_modifiables(self):
        outputString = ""
        newInt = 2
        for attr2 in dir(self.modifiables):
            if (not attr2.startswith('__')) and (not callable(getattr(self.modifiables, attr2))):
                try:
                    new = getattr(self.modifiables, attr2)
                    if attr2 == "hPMax" or attr2 == "weightCap":
                        new = int(new) / 10
                    newInt += int(new)
                    setattr(self.nonModifiables, "totalPoints", int(newInt))
                    # print("Attribute 2 = " + str(attr2))

                except Exception:
                    # print("ERROR IN UPDATE NONMODIFIABLES")
                    pass
        for attr in dir(self.nonModifiables):
            if (not attr.startswith('__')) and (not callable(getattr(self.nonModifiables, attr))):

                # print("Attribute 1= " + str(attr))

                if attr == "exp":
                    outputString = ""
                    while self.nonModifiables.exp >= self.nonModifiables.eXPMax:
                        expvar = pow(self.nonModifiables.level, 2) * 100
                        self.nonModifiables.eXPMax = expvar
                        self.nonModifiables.level += 1
                        self.nonModifiables.expTotal += self.nonModifiables.eXPMax
                        self.nonModifiables.exp = self.nonModifiables.exp - self.nonModifiables.eXPMax
                        outputString = "You leveled up to level " + str(self.nonModifiables.level) + "!"
                        continue

                elif attr == "eXPMax":
                    outputString = ""
                    expvar = pow(self.nonModifiables.level, 2) * 100
                    setattr(self.nonModifiables, "eXPMax", expvar)
                    exptotvar = 0
                    exptot = self.nonModifiables.expTotal
                    for i in range(0, self.nonModifiables.level):
                        exptotvar += (pow(i, 2) * 100)
                        # print("total exp " + str(exptotvar))
                    level = self.nonModifiables.level
                    # print("exp total subtracted "+ str(((exptotvar - (pow(self.nonModifiables.level-1, 2) * 100)))))
                    while (exptot > exptotvar):
                        if ((exptotvar - (pow(level - 1, 2) * 100)) <= exptot < (exptotvar)):
                            return

                        level += 1
                        exptotvar += pow(level, 2) * 100
                        self.nonModifiables.level += 1
                        outputString = "You leveled up to level " + str(self.nonModifiables.level) + "!"
                        self.nonModifiables.eXPMax = exptotvar
                        # print(outputString)

        setattr(self.nonModifiables, "availablePoints",
                ((int(self.nonModifiables.level) * 5) + 12) - self.nonModifiables.totalPoints)
        return outputString

    async def save(self):
        for attr in dir(self):

            if (not attr.startswith('__')) and (
                                            not callable(getattr(self, attr)) and (not (attr == ("equippedAmmo"))) and (
                                    not (attr == ("updateItem"))) and (not (attr == ("selectedItem"))) and (
                            not (attr == ("weapon"))) and (not (attr == ("isLogging"))) and (
                    not (attr == ("dataHandler"))) and (not (attr == ("playerInfo"))) and (
            not (attr == ("fileReader")))):
                # print("SAVE Attribute found in main class " + str(attr))
                try:
                    await self.dataHandler.save_data(attr)
                except Exception:
                    # print("SAVE error: failed to find object " + str(attr) +" in class" )
                    pass

                await self.fileReader.overwrite_file(self.dataHandler.saveData, self.fileName)
        self.dataHandler = Data(self)
