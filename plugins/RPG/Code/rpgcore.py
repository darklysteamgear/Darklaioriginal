
import asyncio
import random
from os import walk
from plugins.RPG.Code import mechanics
from plugins.RPG.Code import items
from plugins.RPG.Code import character


class RPG():

    def __init__(self, directory, pVar):
        self.data = 0
        self.distance = 50
        self.pVar = pVar
        self.dir = directory

    async def give_random_weapon(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.dir + "Weapons" + self.pVar):
            f.extend(filenames)
        randnum = random.randint(0,len(f)-1)
        randweapon = f[randnum].split (".wep", -1)

        return(str(randweapon[0]))

    async def give_random_ammo(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.dir + "Weapons" + self.pVar):
            f.extend(filenames)
        randnum = random.randint(0,len(f)-1)
        randweapon = f[randnum].split (".wep", -1)

        return(str(randweapon[0]))


    async def give_ammo(self, player, ammotype, rounds):
        if ammotype in player.lists.equippedItems["Ammo"]:
            rounds = float(player.lists.equippedItems["Ammo"][ammotype]) + float(rounds)
            print("Rounds " + str(rounds))
        player.lists.equippedItems["Ammo"].update({ammotype: float(rounds)})
        player.lists.equippedItems["Ammo"].update({ammotype:float(rounds)})
        print("Rounds " + str(rounds))
        return



    async def move(self, player, movement):
        agility = player.modifiables.agility
        move_spaces = agility + 1
        if -move_spaces <= movement <= move_spaces:
            if movement + move_spaces < 0:
                self.distance = 0
            else:
                self.distance += movement
        elif move_spaces > movement >= 0:
            self.distance += move_spaces
        else:
            self.distance -= move_spaces
        self.returnStr = ("Moved to a distance of " + str(self.distance) + "m from target.")
        return self.returnStr



    async def get_odds(self, attacker, defender, damtype):
        await attacker.get_weapon()
        await defender.get_weapon()
        self.fight = mechanics.Accuracy(attacker, defender, damtype)
        self.fight.distance = self.distance
        if damtype.upper() == "MELEE" or attacker.weapon.strings.type.upper() == "MELEE":
            self.fight.wrange = attacker.weapon.stats.reach
            self.fight.wdamage = attacker.weapon.stats.meleeDam
            print(self.fight.wrange)
            await self.fight.get_hit_accuracy()
            await self.fight.get_cover_chance()
            await self.fight.get_accuracy_odds()
        elif damtype.upper() == "RANGED":
            await self.fight.get_hit_accuracy()
            await self.fight.get_cover_chance()
            await self.fight.get_accuracy_odds()
        return self.fight.accMess


    async def attack_ranged(self, attacker, defender, timesfired):
        isDoneFiring = False
        if attacker.weapon.strings.type.upper() == "MELEE":
            returnStr = ("you cannot shoot this weapon")
            return returnStr
        self.finalDamToDef = 0
        self.finalDamToSelf = 0
        if timesfired > int(attacker.nonModifiables.weaponClip):
            timesfired = int(attacker.nonModifiables.weaponClip)
        if int(attacker.nonModifiables.weaponClip <= 0):
            self.returnStr = ("WEAPON OUT OF AMMO. RELOAD!")
            return self.returnStr
        if int(attacker.weapon.stats.burstCount) <= timesfired:
            timesfired = attacker.weapon.stats.burstCount
        for i in range(0,timesfired):
            attacker.nonModifiables.weaponClip = int(attacker.nonModifiables.weaponClip)
            await self.fight.get_damage()
            attacker.nonModifiables.weaponClip -= 1
            #print("attacker ammo: " + str(attacker.nonModifiables.weaponClip))
            try:
                if self.fight.defend.character.strings.name != attacker.strings.name:
                    self.finalDamToDef += self.fight.defend.damageFinal
                else:
                    self.finalDamToSelf += self.fight.defend.damageFinal
            except Exception:
                pass
            isDoneFiring = True
        if isDoneFiring == True:
            if timesfired == 1:
                self.returnStr = self.fight.userDamageMessage
                return self.returnStr
            self.returnStr = ("Damage to " + str(self.fight.defender.strings.name) + "= " + str(self.finalDamToDef))
            self.returnStr +=("\nDamage to " + str(self.fight.attacker.strings.name) + "= " + str(self.finalDamToSelf))
            self.returnStr +=("\n" + str(self.fight.attacker.strings.name) + "'s HP: " + str(attacker.nonModifiables.hp) + "/" + str(attacker.modifiables.hPMax))
            self.returnStr +=("\n" + str(self.fight.defender.strings.name) + "'s HP: " + str(defender.nonModifiables.hp) + "/" + str(defender.modifiables.hPMax))
            self.returnStr += ("\nTotal shots fired: " + str(timesfired))
            return self.returnStr


    async def attack_melee(self, attacker, defender):
        await attacker.get_weapon()
        await defender.get_weapon()
        self.fight.wrange = attacker.weapon.stats.reach
        self.fight.distance = 0.3
        print(self.fight.wrange)
        await self.fight.get_damage()
        self.fight.wdamage = attacker.weapon.stats.meleeDam
        self.returnStr = self.fight.userDamageMessage
        return self.returnStr


    async def new_weapon(self,weaponName):
        null= "null"














if __name__ == "__main__":
    darkly = character.Character("\\DARKAi v2\\plugins\\RPG\\Characters\\examplecharactersave.cdat")
    dummy = character.Character("\\DARKAi v2\\plugins\\RPG\\Characters\\practicedummy.cdat")
    RPGame = RPG()
    weapon = items.Weapon()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(darkly.load())
    loop.run_until_complete(dummy.load())
    loop.run_until_complete(darkly.get_weapon())
    loop.run_until_complete(darkly.get_info())
    print(darkly.weapon.dataHandler.info)
    #loop.run_until_complete(darkly.edit_stats("maxHP", 2))
    print(darkly.dataHandler.info)
    print(weapon.dataHandler.info)
    loop.run_until_complete(darkly.select_item("Darkly Mallows"))
    loop.run_until_complete(darkly.get_info())
    print("Item name= " + str(darkly.selectedItem.stats.weight))
    loop.run_until_complete(darkly.update_weight())
    print(darkly.nonModifiables.weightTotal)
    print(loop.run_until_complete(darkly.use_item()))
    darkly.lists.equippedItems["Weapon"] = ("Dragonov")
    print(darkly.lists.equippedItems["Weapon"])
    loop.run_until_complete(darkly.get_weapon())
    print(darkly.weapon.strings.type)
    print(loop.run_until_complete(RPGame.give_ammo(darkly, "Sniper Rounds", "30")))
    #accuracy = Accuracy(darkly, dummy)
    if darkly.nonModifiables.weaponClip == 0:
        print(loop.run_until_complete(darkly.load_weapon()))
    RPGame.distance = 0.5
    print(loop.run_until_complete(RPGame.get_odds(darkly, dummy, "melee")))
    print(loop.run_until_complete(RPGame.attack_melee(darkly, dummy)))
    loop.run_until_complete(darkly.update_non_modifiables())
    #print("Final equippeditems" + str(darkly.lists.equippedItems))


    #loop.run_until_complete(dummy.save())




    #loop.run_until_complete(accuracy.get_hit_accuracy())
    #loop.run_until_complete(accuracy.get_cover_chance())
    #loop.run_until_complete(accuracy.get_accuracy_odds())
    #loop.run_until_complete(accuracy.get_damage())
    #print(accuracy.userDamageMessage)
    loop.run_until_complete(dummy.save())
    print("Saved")
    loop.run_until_complete(darkly.save())

