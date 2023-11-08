
from plugins.RPG.Code.datahandling import Data
import filehandler

#The class for any misc item. also inherited by armor and weapon item types.
class Item:
    def __init__(self):

        #misc start of class items
        self.fileReader = filehandler.FileHandler(enablelogging=False, encoding="ascii")
        self.dataHandler = Data(self)

        #item stats
        class Strings:
            def __init__(self):
                self.name = ""
                self.typeItem = "" #anything here

        class Stats:
            def __init__(self):
                self.weight = 0.0
                self.uses = 0

        class Lists:
            def __init__(self):
                self.effects = {}

        class Bools:
            def __init__(self):
                self.isAuto = False

        self.bools = Bools()
        self.lists = Lists()
        self.strings = Strings()
        self.stats = Stats()



    async def load(self, filename):
        rawCharacterData = await self.fileReader.get_file_contents(filename)
        self.saveData = ""
        for attr in dir(self):

            if (not attr.startswith('__')) and (not callable(getattr(self, attr))and (not callable(getattr(self, attr)) and (not (attr == ("isLogging"))) and (not (attr == ("parent"))) and (not (attr == ("dataHandler"))) and (not (attr == ("playerInfo"))) and (not (attr == ("fileReader")))) and (not (attr == ("isLogging"))) and (not (attr == ("parent"))) and (not (attr == ("dataHandler"))) and (not (attr == ("playerInfo"))) and (not (attr == ("fileReader")))):
                #print("\nAttribute found in main class " + str(attr))
                try:
                    await self.dataHandler.fetch_data(attr, rawCharacterData)
                except Exception:
                #print("error: failed to find object " + str(attr) +" in class" )
                    pass

    async def get_effects(self):
        effectArgs = [0]
        for effect in self.lists.effects:
            effectArgs[0] = self.lists.effects[effect]



    async def save(self, filename):
        for attr in dir(self):

            if (not attr.startswith('__')) and (not callable(getattr(self, attr))and (not callable(getattr(self, attr)) and (not (attr == ("isLogging"))) and (not (attr == ("parent"))) and (not (attr == ("dataHandler"))) and (not (attr == ("playerInfo"))) and (not (attr == ("fileReader")))) and (not (attr == ("isLogging"))) and (not (attr == ("playerInfo"))) and (not (attr == ("parent"))) and (not (attr == ("dataHandler"))) and (not (attr == ("fileReader")))):
                # print("Attribute found in main class " + str(attr))
                try:
                    await self.dataHandler.save_data(attr)
                except Exception:
                    # print("error: failed to find object " + str(attr) +" in class" )
                    pass

                await self.fileReader.overwrite_file(self.dataHandler.saveData, filename)




#The armor class. inhereted from the item class
class Armor(Item):

    def __init__(self, amplification, duration):
        Item.__init__(self)
        # misc start of class items
        self.fileReader = filehandler.FileHandler(enablelogging=False, encoding="ascii")
        self.dataHandler = Data(self)

        # weapon stats
        class Strings:
            def __init__(self):
                self.name = ""
                self.type = ""  # anything here
                self.typeItem = "Armor"

        class Stats:
            def __init__(self):
                self.defense = 0
                self.durability = 0
                self.agility = 0
                self.weight = 0

        class Lists:
            self.weaknesses = {}
            self.strengths = {}
            self.repairMaterials = {}
            self.abilities = {}

        self.strings = Strings()
        self.stats = Stats()
        self.lists = Lists()


#The class object for weapons
class Weapon(Item):

    def __init__(self):
        Item.__init__(self)
        #misc start of class items
        self.fileReader = filehandler.FileHandler(enablelogging=False, encoding="ascii")
        self.dataHandler = Data(self)
        #weapon stats
        class Strings:
            def __init__(self):
                self.name = ""
                self.type = "" #melee or ranged
                self.typeItem = "Weapon"

        class Stats:
            def __init__(self):
                self.range = 0
                self.reach = float(0.0)
                self.damage = 0
                self.accuracy = float(0.001)
                self.meleeDam = 0
                self.critMult = float(0.001)
                self.critChance = float(0.001)
                self.clipSize = 0
                self.burstCount = 0

        class Lists:
            def __init__(self):
                #different damage types that the weapon does, and the percent damage it does for each type
                self.damTypes = {}
                self.damTypesMelee = {}
                #different ammo types the weapon takes
                self.ammoTypes = []

        class Bools:
            def __init__(self):
                self.isAuto = False

        self.bools = Bools()
        self.lists = Lists()
        self.strings = Strings()
        self.stats = Stats()