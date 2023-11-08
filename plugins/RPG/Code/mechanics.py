import math
import random

# The class to calculate attack damage dealt with accordance to the players stats for defense.
class Defense():
    def __init__(self, attacker, defender, rawDamage):
        self.character = defender
        self.attacker = attacker
        self.rawDamage = rawDamage
        self.damageFinal = 0

    #gets the net damage a player deals to another player
    async def get_damage(self):
        self.damageMult = self.character.modifiables. defense/ 2
        if self.damageMult < 1:
            self.damageFinal = self.rawDamage
        else:
            self.damageFinal = round(self.rawDamage / self.damageMult)
        if self.damageFinal < self.character.nonModifiables.hp:
            self.character.nonModifiables.hp = self.character.nonModifiables.hp - self.damageFinal
            setattr(self.character.nonModifiables, "hp", self.character.nonModifiables.hp)
            self.actualDamageStr = self.character.strings.name + " Has lost " + str(self.damageFinal) + " HP"
            self.actualDamageStr += "\n" + self.character.strings.name + ": " + str \
                (int(self.character.nonModifiables.hp)) + "/" + str(self.character.modifiables.hPMax) + "HP"
        elif self.damageFinal >= self.character.nonModifiables.hp:
            self.character.nonModifiables.hp = 0
            self.actualDamageStr = self.character.strings.name + " has been defeated!" + "\n" + str \
                (int(self.character.nonModifiables.hp)) + "/" + str(self.character.modifiables.hPMax) + "HP"
            self.actualDamageStr += "\n" + str \
                (round(self.character.nonModifiables.expTotal / 3, 0)) + " EXP rewarded to " + str \
                (self.attacker.strings.name)
            self.attacker.nonModifiables.exp = int \
                (int(self.attacker.nonModifiables.exp) + int(round(self.character.nonModifiables.expTotal / 3, 0)))
            await self.attacker.update_non_modifiables()
            await self.attacker.save()
        return self.actualDamageStr


#class to calculate the player's accuracy in accordance to their stats and other data
class Accuracy():
    def __init__(self, attChar, defChar, wtype):
        self.attacker = attChar
        self.defender = defChar
        self.weapon = self.attacker.weapon
        #print(self.attacker.modifiables.accuracy)
        self.accuracy = int(self.attacker.modifiables.accuracy)
        self.luck = int(self.attacker.modifiables.luck)
        self.attack = int(self.attacker.modifiables.attack)
        self.agility = int(self.attacker.modifiables.agility)
        self.targlength = int(self.defender.measurements.length)
        self.targheight = int(self.defender.measurements.height)
        self.targwidth = int(self.defender.measurements.width)
        self.wcritchance = self.weapon.stats.critChance
        self.wrange = int(self.weapon.stats.range)
        self.wdamage = int(self.weapon.stats.damage)
        self.waccuracy = float(self.weapon.stats.accuracy)
        self.wcritMultiplier = float(self.weapon.stats.critMult)
        self.wType= wtype
        #print(self.weapon.dataHandler.info)
        self.covlength = 0
        self.covheight = 0
        self.covwidth = 0
        self.wangle = 23
        self.distance = 100
        self.nameOfTarget = self.defender.strings.name

        #chances to miss hit crit and minicrit
        self.miss = 0
        self.hit = 0
        self.miniCrit = 0
        self.crit = 0

        self.hitAcc = 0
        self.critChance = 0
        self.coverBonus = 0
        self.dodgeBonus = 0

        self.isFlanked = False


    #Gets the chance a player has to take cover
    async def get_cover_chance(self):


        xdirection = (self.covlength * math.cos(math.radians(self.wangle))* math.cos(math.radians(10)))
        ydirection = (self.covheight * math.sin(math.radians(10)))
        zdirection = (self.covwidth * math.sin(math.radians(self.wangle))* math.cos(math.radians(10)))
        xdirection = xdirection/(self.targlength * math.cos(math.radians(self.wangle)) * math.cos(math.radians(10)) + 1)
        ydirection = ydirection/(self.targheight * math.sin(math.radians(10)) + 1)
        zdirection = zdirection/(self.targwidth * math.sin(math.radians(self.wangle))* math.cos(math.radians(10)) + 1)

        xdirection = pow(xdirection,2)
        ydirection = pow(ydirection,2)
        zdirection = pow(zdirection,2)
        if xdirection > 1:
            xdirection = 1

        elif xdirection < -1:
            xdirection = -1

        if ydirection > 1:
            ydirection = 1

        elif ydirection < -1:
            ydirection = -1

        if zdirection > 1:
            zdirection = 1

        elif zdirection < -1:
            zdirection = -1

        if 0 <= self.wangle <= 90:
            if xdirection < 0:
                xdirection *= -1
            if ydirection < 0:
                ydirection *= -1
            if zdirection < 0:
                zdirection *= -1

        if 90 < self.wangle <= 180:
            if xdirection < 0:
                xdirection *= -1
            if ydirection < 0:
                ydirection *= -1
            if zdirection < 0:
                zdirection *= -1

        if 180 < self.wangle <= 270:
            if xdirection > 0:
                xdirection *= -1
            if ydirection > 0:
                ydirection *= -1
            if zdirection > 0:
                zdirection *= -1

        if 270 < self.wangle <= 360:
            if xdirection > 0:
                xdirection *= -1
            if ydirection > 0:
                ydirection *= -1
            if zdirection > 0:
                zdirection *= -1

        self.covlengthDiff = self.covlength - self.targlength
        self.covheightDiff = self.covheight - self.targheight
        self.covwidthDiff = self.covwidth - self.targwidth
        compare = self.covlengthDiff
        for i in range(0,2):
            if self.covwidthDiff < compare:
                self.coverBonus = zdirection
                compare = self.covwidthDiff
            if self.covheightDiff < compare:
                self.coverBonus = ydirection
                compare = self.covheightDiff
            if self.covlengthDiff <= compare:
                self.coverBonus = xdirection
                compare = self.covlengthDiff

        if self.coverBonus < 0:
            self.coverBonus *=-1
            self.coverBonus = round(pow(self.coverBonus, (1 / 2)) *100, 0)
            self.coverBonus *= -1
        else:
            self.coverBonus = round(pow(self.coverBonus, (1 / 2))*100,0)
        #print("Cover 1 x " + str(xdirection))
        #print("Cover 1 y " + str(ydirection))
        #print("Cover 1 z " + str(zdirection))
        self.coverMessage = ("Cover Bonus " + str(self.coverBonus))
        if self.coverBonus < 0:
            #print("Flanked!")
            self.isFlanked = True

    #gets the hit accuracy of an object.
    async def get_hit_accuracy(self):
        if self.wType.upper() == "RANGED":
            if self.distance >= self.wrange:
                nZeros = len(str(self.distance))
                num = (pow(self.luck+self.accuracy,nZeros))
                print("Numerator " + str(num))
                denom = ((self.distance)*pow(10,nZeros - 1))
                while num > denom:
                    num = num*pow(10,-1)
                    #print("Numerator " + str(num))
                #print("Denominator " + str(denom))
                self.hitAcc = round(num/denom,5)
                self.hitAcc = round(self.hitAcc*100 * self.waccuracy,0)
                #print("Hit accuracy " + str(self.hitAcc))

            else:
                nZeros = len(str(self.wrange))
                deltaNZeros = len(str(self.wrange)) - len(str(self.distance))
                self.hitAcc = round((1-((self.distance)/(pow(self.accuracy,nZeros-1) + self.wrange))),4)
                #print(str(self.hitAcc))
                area = (self.targlength * self.targwidth * self.targheight)
                #print("area " + str(area))
                value1 = (pow(self.wrange, 3) - (self.wrange * self.distance)) + 1
                #print ("Value 1 " + str(value1))
                denom = round((pow(value1,(1/(2))) *100),4)
                #print("Denominator " + str(denom))
                numDivDenom = round(area/denom, 4)
                #print("Numerator / Denominator " + str(numDivDenom))
                if numDivDenom > 1:
                    self.hitAcc = 100.0
                    #print("Hit accuracy " + str(self.hitAcc))
                else:
                    #print("Numerator / Denominator " + str(numDivDenom))
                    numDivDenom = numDivDenom*(self.wrange*pow(10,-nZeros + 1))
                    if numDivDenom > 1:
                        numDivDenom = numDivDenom*.08
                    #print("Numerator / Denominator " + str(numDivDenom))
                    subtractOne = round(1 - numDivDenom,4)
                    if subtractOne < 0:
                        isNegative = True
                        subtractOne = subtractOne*-1
                    #print("Minus one " + str(subtractOne))
                    powOfAcc = round(pow(subtractOne,(self.accuracy + deltaNZeros/2)),6)
                    #print("To the power of accuracy " + str(powOfAcc))
                    self.hitAcc *= (1-powOfAcc)
                    if self.hitAcc < 0:
                        isNegative = True
                        self.hitAcc = self.hitAcc*-1
                    #print("Hit accuracy " + str(self.hitAcc))
                    self.hitAcc *= self.waccuracy
                    self.hitAcc *= 100
                    self.hitAcc = round(self.hitAcc, 0)
                    #print("Hit accuracy " + str(self.hitAcc))
        elif self.wType.upper() == "MELEE":
            if self.wrange < self.distance:
                self.hitAcc = 0
                return
            if self.wrange > self.distance:
                volume = self.targheight * self.targlength * self.targwidth
                #Physics! density = mass/volume
                density = ((self.defender.modifiables.weightCap + self.defender.modifiables.defense) * 100) / volume
                self.hitAcc = (((self.wrange * 100) * density * self.defender.modifiables.agility)/((self.agility + self.attack) + self.accuracy))
                if self.hitAcc == 0.0:
                    self.hitAcc = 1.0
                elif self.hitAcc > 1:
                    self.hitAcc = 0.2
                else:
                    self.hitAcc = 1 - self.hitAcc
                self.hitAcc *= 100
                print("Melee hit accuracy " + str(self.hitAcc))


    #gets the accuracy odds
    async def get_accuracy_odds(self):
        self.adder = 0
        try:
            self.hitChance = round((self.hitAcc - (((self.hitAcc * (self.coverBonus*.01)) + (self.hitAcc * self.dodgeBonus))/(self.hitAcc)) * self.hitAcc),0)
        except ZeroDivisionError:
            self.hitChance = 0
        if self.wType.upper() == "MELEE":
            self.luck = int(round((self.agility/2) + (self.attack/2),1))
        print("Current hit percent chance calculated " + str(self.hitChance))
        self.miss = 100 - self.hitChance
        self.scratch = round(((1/4)*self.hitChance) - ((self.hitChance * self.luck)/100),0)
        if self.scratch < 0:
            self.adder = round(self.scratch)
            self.scratch = 0
        self.critChance = (self.wcritchance * self.luck)
        self.hit = round(self.hitChance - (self.scratch + (3*self.critChance *self.hitChance)))
        if self.hit < 0:
            self.adder += self.hit
            self.hit = 1

        self.miniCritChance = (1 - (self.critChance))
        self.miniCritAdder = round(self.miniCritChance * self.adder,0)
        self.miniCrit = round(self.miniCritChance * 2 * (self.critChance * self.hitChance),0)
        self.critAdder = round((1 - self.miniCritChance) * self.adder,0)
        self.crit = (self.hitChance - (self.scratch + self.hit + self.miniCrit))
        if self.miniCrit < 0:
            self.miniCrit = 0
            self.crit = self.hitAcc - (self.scratch + self.hit)
        if self.crit < 0:
            self.miniCrit -= 1
            self.crit = 1

        self.accMess = ("Critical weapon hit chance " + str((self.critChance * 100)) + "%")
        self.accMess += ("\nHit percentage " + str(self.hitChance) + "%")
        self.accMess += ("\nMiss chance " + str(self.miss) + "%")
        self.accMess += ("\nScratch chance " + str(self.scratch) + "%")
        self.accMess += ("\nHit chance " + str(self.hit) + "%")
        self.accMess += ("\nMini critical chance " + str(self.miniCrit) + "%")
        self.accMess += ("\nCritical chance " + str(self.crit) + "%")
        #print("All added " + str(self.crit + self.hit + self.miniCrit + self.scratch))

        self.missRange = self.miss
        self.scratchRange = self.miss + self.scratch
        self.hitRange = self.scratchRange + self.hit
        self.miniCritRange = self.hitRange + self.miniCrit
        self.critRange = self.miniCritRange + self.crit

        if self.wType.upper() == "MELEE":
            self.luck = self.attacker.modifiables.luck

    async def get_damage(self):
        #print("Miss range " + str(self.missRange))
        #print("Scratch range " + str(self.scratchRange))
        #print("Hit range " + str(self.hitRange))
        #print("Mini crit range " + str(self.miniCritRange))
        #print("Critical range " + str(self.critRange))
        if self.wType.upper() == "MELEE":
            self.scratchStr = "grazed"
            self.hitStr = "whacked"
            self.miniCritStr = "bashed"
            self.critStr = "clobbered"
            self.superCritStr = "completely demolished"
        else:
            self.scratchStr = "scratched"
            self.hitStr = "hit"
            self.miniCritStr = "did mini-critical damage to"
            self.critStr = "did critical damage to"
            self.superCritStr = "did super critical damage to"

        userRoll = random.randint(-10,100+(round(self.accuracy/3,0)))

        if self.missRange/4 <= userRoll <= self.missRange:
            self.userDamageMessage = ("Got a " + str(userRoll) + " and missed")
            self.damage = 0
            self.playerHurt = "None"

        elif self.missRange <= userRoll <= self.scratchRange:
            self.damage = round(((userRoll)/self.scratchRange)* (self.wdamage + self.attack),0)
            self.playerHurt = self.defender
            self.userDamageMessage = ("Got a " + str(userRoll) + " and " + str(self.scratchStr) + " " + self.nameOfTarget +  " for " + str(self.damage) + " points of hp damage")

        elif self.scratchRange <= userRoll <= self.hitRange:
            self.damage = round(((userRoll)/self.hitRange)*(self.wdamage + self.attack) + self.wdamage + self.attack,0)
            self.playerHurt = self.defender
            self.userDamageMessage = ("Got a " + str(userRoll) + " and " + str(self.hitStr) + " " + self.nameOfTarget + " for " + str(self.damage) + " points of hp damage")

        elif self.hitRange <= userRoll <= self.miniCritRange:
            self.damage = round(self.wcritMultiplier*((userRoll)/self.miniCritRange)*(self.wdamage + self.attack),0)
            self.playerHurt = self.defender
            self.userDamageMessage = ("Got a " + str(userRoll) + " and " + str(self.miniCritStr) + " " + self.nameOfTarget + " for " + str(self.damage) + " points of hp damage")

        elif self.miniCritRange <= userRoll <= self.critRange:
            self.damage = round(self.wcritMultiplier*((userRoll)/(self.critRange/1.5))*(self.wdamage + self.attack) + self.wdamage + self.attack,0)
            self.playerHurt = self.defender
            self.userDamageMessage = ("Got a " + str(userRoll) + " and "+ str(self.critStr) + " " + self.nameOfTarget + " for " + str(self.damage) + " points of hp damage!")

        elif self.critRange < userRoll:
            self.damage = round(self.wcritMultiplier*((userRoll)/(self.miniCritRange*.75))*(self.wdamage + self.attack) + self.wdamage + self.attack,0)
            self.playerHurt = self.defender
            self.userDamageMessage = ("Your luck proceeds you. You got a " + str(userRoll) + " and " + str(self.superCritStr) + " " + self.nameOfTarget + " for " + str(self.damage) + " points of hp damage!!! DAMN SON")

        else:
            if userRoll - self.luck <= -5:
                self.damage = round(-(self.wdamage + self.attack)*.5, 0)
                self.playerHurt = self.attacker
                self.userDamageMessage = ("Got a " + str(userRoll) + " and luck is on your side today! you regenerated " + str(-self.damage) + " points of hp!")

            else:
                self.damage = round((self.wdamage + self.attack)/2,0)
                self.playerHurt = self.attacker
                self.userDamageMessage = ("Got a " + str(userRoll) + " and messed up! you hit yourself for " + str(self.damage) + " points of hp damage!")

        if self.isFlanked == True:
            self.userFlankMessage = ("The target has been flanked!")

        if self.playerHurt == "None":
            return
        self.defend = Defense(self.attacker, self.playerHurt,  self.damage)
        self.userDamageMessage += "\n" + str(await self.defend.get_damage())
