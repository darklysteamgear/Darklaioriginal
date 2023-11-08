from plugins.rpg.Code.datahandling import Data
import filehandler

#The effect class, for handling effects
class Effect:

    def __init__(self, amplification, duration):
        # misc start of class items
        self.fileReader = filehandler.FileHandler(enablelogging=False, encoding="ascii")
        self.dataHandler = Data(self)

        # weapon stats
        class Strings:
            def __init__(self):
                self.name = ""
                self.type = ""  # anything here

        class Stats:
            def __init__(self):
                self.amp = amplification
                self.dur = duration

        class Lists:
            self.baseChanges = {}

        self.strings = Strings()
        self.stats = Stats()

    async def load(self, filename):
        rawCharacterData = await self.fileReader.get_file_contents(filename)
        self.saveData = ""
        for attr in dir(self):

            if (not attr.startswith('__')) and (
                                not callable(getattr(self, attr)) and (not (attr == ("isLogging"))) and (
                        not (attr == ("parent"))) and (not (attr == ("dataHandler"))) and (
                not (attr == ("playerInfo"))) and (not (attr == ("fileReader")))):
                # print("\nAttribute found in main class " + str(attr))
                try:
                    await self.dataHandler.fetch_data(attr, rawCharacterData)
                except Exception:
                    # print("error: failed to find object " + str(attr) +" in class" )
                    pass