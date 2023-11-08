


#Handles all of the data in the data files
class Data():
    def __init__(self, parent):
        self.saveData = ""
        self.info = ""
        self.parent = parent


    async def save_data(self, dataset):
        dataset = getattr(self.parent, dataset)
        isDoNot = False
        for attr in dir(dataset):
            if not attr.startswith('__') and not callable(getattr(dataset, attr)) and not isinstance(getattr(dataset, attr), dict) and not isinstance(getattr(dataset, attr), list):
                try:
                    if (str(attr) == "isLogging") or (str(attr) == "fileReader") or (str(attr) == "saveData") or (str(attr) == "playerInfo"):
                        #print("no, BAD")
                        pass
                    else:
                        if isDoNot == True:
                            pass
                        else:
                            self.saveData += attr.capitalize() + "= " + str(getattr(dataset, attr)) + "\n"
                except Exception:
                    if (str(attr) != "isLogging") and (str(attr) != "fileReader") and (str(attr) != "saveData") and (str(attr) != "playerInfo"):
                        #print("ERROR variable could not be found for " + attr)
                        pass

            elif (isinstance(getattr(dataset, attr), dict) or isinstance(getattr(dataset, attr), list)) and (not attr.startswith('__')) and (not callable(getattr(dataset, attr))):
                #print("List or dictionary " + str(attr) + " found.")

                if (getattr(dataset, attr) != {}) and (getattr(dataset, attr) != []):
                    i = 0
                    conStr = ""
                    for k in getattr(dataset, attr):# k = ( +' +  Hands + ' + , + Red Gloves + ) + ,
                        if str(attr) != "equippedItems":
                            if i >= 1:
                                keyStr = "(" + "'" + str(k) + "'" + "," + str(getattr(dataset, attr)[k]) + ") "
                            else:
                                keyStr = "(" + "'" + str(k) + "'" + "," + str(getattr(dataset, attr)[k]) + ") "
                            conStr = conStr.replace(") ", "), ")
                            conStr += keyStr
                            i += 1

                        elif str(attr) == "equippedItems":
                                try:
                                    if isinstance((getattr(dataset, attr)[k]), dict):
                                        conStr = ""
                                        for k2 in getattr(dataset, attr)[k]:
                                            #print("Check if this is not alpha " + str(k2))
                                            if i >= 1 and not str(k2).isalpha():
                                                #print("this is not alpha " + str(k2))
                                                keyStr = "(" + "'" + str(k2) + "'" + "," + str(getattr(dataset, attr)[k][k2]) + ") "
                                                #print("Keystring " + str(keyStr))
                                                conStr += keyStr
                                                conStr = conStr.replace(") ", "), ")
                                            elif not str(k2).isalpha():
                                                #print("this is not alpha " + str(k2))
                                                keyStr = "(" + "'" + str(k2) + "'" + "," + str(getattr(dataset, attr)[k][k2]) + ") "
                                                #print("Keystring " + str(keyStr))
                                                conStr += keyStr
                                                conStr = conStr.replace(") ", "), ")
                                        if conStr.endswith("), "):
                                            conStr = conStr[:-2]
                                        #print("Con String " + str(conStr))
                                        self.saveData += k.capitalize() + "= " + str(conStr) + "\n"
                                    else:
                                        k.give_me_dat_sweet_sweet_error_so_this_program_can_run_like_butter_on_a_warm_summer_day()
                                        #continue
                                except Exception:
                                    try:
                                        if isinstance((getattr(dataset, attr)[k]), dict):
                                            conStr = ""
                                            for i in range(0,len(getattr(dataset, attr)[k])):
                                                keyStr = "(" + "'" + str(getattr(dataset, attr)[k][i]) + "'" + ") "
                                                conStr += keyStr
                                                conStr = conStr.replace(") ", "), ")
                                            if conStr.endswith("), "):
                                                conStr = conStr[:-2]
                                            self.saveData += k.capitalize() + "= " + str(conStr) + "\n"
                                            #continue
                                        else:
                                            conStr = ""
                                            self.saveData += k.capitalize() + "= " + str(getattr(dataset, attr)[k]) + "\n"

                                    except Exception:
                                        print("Error Saving " + str(k))

                                    #except Exception :
                                        pass
                    if conStr.endswith("), "):
                        conStr = conStr[:-2]
                    if attr == "equippedItems":
                        pass
                    else:
                        self.saveData += attr.capitalize() + "= " + str(conStr) + "\n"


        self.saveData.replace("Playerinfo= ", "")
        #print("Save data \n" + str(self.saveData))
        pass


    async def fetch_data(self, dataset, rawdata):

        dataset = getattr(self.parent, dataset)
        self.info = ""
        for attr in dir(dataset):
            data = 0
            isNotFound = False

            if (not attr.startswith('__')) and (not callable(getattr(dataset, attr)) and (str(attr) != "playerInfo")):
                #print("attribute " + str(attr) + " found")
                try:
                    line = [i for i, s in enumerate(rawdata) if attr.upper() + "=" in s.upper()][0]
                    data = rawdata[line].rsplit("= " or " = " or " =")[-1]
                except Exception:
                    #print("error")
                    isNotFound = True
                if isNotFound== False and (getattr(dataset, attr) != {}) and (getattr(dataset, attr) != []):
                    if isinstance(getattr(dataset, attr), int) and ((str(data) != "False") and (str(data) != "True")):
                        setattr(dataset, attr, int(data))
                        continue
                    elif isinstance(getattr(dataset, attr), float):
                        setattr(dataset, attr, float(data))
                        continue
                    elif isinstance(getattr(dataset, attr), str):
                        setattr(dataset, attr, str(data))
                        continue
                    elif isinstance(getattr(dataset, attr), bool):
                        setattr(dataset, attr, data)
                        continue
                    #print("Raw Data = " + str(data))

                    #print(str((getattr(dataset, attr) != [])))

                elif (isinstance(getattr(dataset, attr), dict)) or (isinstance(getattr(dataset, attr), list)):
                    isNotFound = False
                    listOrDict = getattr(dataset, attr)
                    dataDict = {}
                    dataList = []
                try:
                    if (getattr(dataset, attr) != {}) and (getattr(dataset, attr) != []):

                        for k in getattr(dataset, attr):
                            listOrDict = getattr(dataset, attr)
                            dataDict = {}
                            dataList = []

                            try:
                                line = [i for i, s in enumerate(rawdata) if k.upper() in s.upper()][0]
                                data = rawdata[line].rsplit("= " or " = " or " =")[-1]


                                if data.startswith("("):

                                    data = data.split(")")
                                    for p in data:
                                        if p.startswith("("):
                                            p = p.replace("(", '')
                                        p = p.replace(",(", '')
                                        p = p.replace(", (", '')
                                        p = p.replace(" ,(", '')
                                        p = p.replace("'", '')
                                        p = p.rsplit(',')
                                        if len(p) <= 1:
                                            if p[0] != '':
                                                #print(str(p[0]))
                                                dataList.append(str(p[0]))
                                            if dataDict == {}:
                                                data = dataList
                                        elif len(p) > 1:
                                            for i in range(len(p)):
                                                if i % 2 == 0:
                                                    dataDict.update({str(p[i]): str(p[i - 1])})
                                                    data = dataDict
                                listOrDict[k] = data

                            except Exception:
                                isNotFound = True
                                #print("ERROR key could not be found for " + str(k))
                            data = listOrDict
                        setattr(dataset, attr, data)
                    else:
                        if data.startswith("("):
                            data = data.split(")")
                            for p in data:
                                if p.startswith("("):
                                    p = p.replace("(", '')
                                p = p.replace(",(", '')
                                p = p.replace(", (", '')
                                p = p.replace(" ,(", '')
                                p = p.replace("'", '')
                                p = p.split(',')
                                if len(p) <= 1:
                                    if p[0] != '':
                                        #print(str(p[0]))
                                        dataList.append(str(p[0]))
                                    if dataDict == {}:
                                        data = dataList
                                elif len(p) > 1:
                                    for i in range(len(p)):
                                        if i % 2 == 0:
                                            dataDict.update({str(p[i]): str(p[i - 1])})
                                            data = dataDict
                                #print(str(data))
                    setattr(dataset, attr, data)
                except Exception:
                    isNotFound = True
                    if attr != "playerInfo" and (isNotFound == False):
                        print("Failed Data = " + str(data))
                        setattr(dataset, attr, str(data))

                    else:
                        pass
                        #print(str(data))
                #print("End Data = " + str(data))
                #print("Attribute " + str(attr) + " Found on line " + str(line) + " Set to " + str(
                #getattr(dataset, attr)))
                self.info += str(attr) + "= " + str(getattr(dataset, attr)) + "\n"
                #except Exception:
                    #print("an error has occured")